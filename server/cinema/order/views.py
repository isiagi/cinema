# views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
import requests
from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import json
import logging
from .models import Order
from rest_framework import viewsets

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def flutterwave_webhook(request):
    """
    Handle Flutterwave webhook notifications for payment verification
    """
    secret_hash = settings.FLUTTERWAVE_SECRET_HASH
    signature = request.headers.get("verifi-hash")

    if not signature or signature != secret_hash:
        logger.warning("Invalid webhook signature received")
        return HttpResponse(status=401)

    try:
        payload = json.loads(request.body)
        logger.info(f"Received Flutterwave webhook: {payload}")

        # Handle the webhook event
        event_type = payload.get('event')
        if event_type == 'charge.completed':
            transaction_id = payload.get('data', {}).get('id')
            status = payload.get('data', {}).get('status')
            tx_ref = payload.get('data', {}).get('tx_ref')

            if status == 'successful':
                # Find and update corresponding order
                try:
                    order = Order.objects.get(payment_reference=tx_ref)
                    order.payment_status = 'completed'
                    order.transaction_id = transaction_id
                    order.save()
                    logger.info(f"Order {order.id} payment completed successfully")
                except Order.DoesNotExist:
                    logger.error(f"Order not found for tx_ref: {tx_ref}")
            else:
                logger.warning(f"Payment not successful for tx_ref: {tx_ref}")

        return HttpResponse(status=200)

    except json.JSONDecodeError:
        logger.error("Invalid JSON payload received")
        return HttpResponse(status=400)
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return HttpResponse(status=500)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def initiate_payment(self, amount, phone_number, provider):
        """
        Initiate mobile money payment with Flutterwave
        """
        try:
            tx_ref = f"tx-{timezone.now().timestamp()}"
            payload = {
                "tx_ref": tx_ref,
                "amount": amount,
                "currency": "UGX",
                "country": "UG",
                "phone_number": phone_number,
                "network": provider,
                "email": self.request.user.email,
                "fullname": f"isiagi",
                "redirect_url": f"http://localhost:3000/payment-callback"
            }

            response = requests.post(
                "https://api.flutterwave.com/v3/charges?type=mobile_money_uganda",
                json=payload,
                headers={
                    "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
                    "Content-Type": "application/json",
                }
            )

            if response.status_code != 200:
                logger.error(f"Flutterwave payment initiation failed: {response.text}")
                raise ValidationError("Payment initiation failed")

            return response.json(), tx_ref

        except requests.RequestException as e:
            logger.error(f"Payment request failed: {str(e)}")
            raise ValidationError("Payment service unavailable")

    def create(self, request, *args, **kwargs):
        try:
            # First validate the order data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            payment_data = request.data.get('payment', {})
            if not all([
                payment_data.get('phone_number'),
                payment_data.get('provider'),
                request.data.get('total_price')
            ]):
                raise ValidationError("Missing payment information")

            # Initiate payment
            payment_response, tx_ref = self.initiate_payment(
                amount=request.data.get('total_price'),
                phone_number=payment_data.get('phone_number'),
                provider=payment_data.get('provider')
            )

            if payment_response.get('status') != 'success':
                raise ValidationError("Payment initiation failed")

            # Create order with pending payment status
            order = serializer.save(
                user=request.user,
                payment_status='pending',
                payment_reference=tx_ref  # Store tx_ref for webhook matching
            )

            response_data = {
                'order': serializer.data,
                'payment': {
                    'transaction_id': payment_response.get('data', {}).get('id'),
                    'status': 'pending',
                    'instructions': payment_response.get('meta', {}).get('authorization', {})
                }
            }

            return Response(response_data, status=status.HTTP_202_ACCEPTED)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Order creation failed: {str(e)}")
            return Response(
                {'error': 'Order creation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )