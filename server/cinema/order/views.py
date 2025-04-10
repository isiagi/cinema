# views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
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
    logger.error("**************** WEBHOOK DEBUG START ****************")
    logger.error(f"Request Method: {request.method}")
    
    signature = request.headers.get("verif-hash")
    if not signature:
        signature = request.META.get("HTTP_VERIF_HASH")
    
    if signature != settings.FLUTTERWAVE_SECRET_HASH:
        logger.error(f"Signature mismatch:")
        logger.error(f"Received: {signature}")
        logger.error(f"Expected: {settings.FLUTTERWAVE_SECRET_HASH}")
        return HttpResponse("Invalid signature", status=401)

    try:
        payload = json.loads(request.body)
        logger.error(f"Webhook payload: {payload}")
        
        tx_ref = payload.get('txRef')
        status = payload.get('status')
        
        try:
            order = Order.objects.get(payment_reference=tx_ref)
            
            if status == 'successful':
                order.payment_status = 'completed'
                order.save()
                logger.error(f"Order {order.id} payment completed successfully")
            elif status in ['failed', 'cancelled']:
                # Delete the order if payment failed or was cancelled
                logger.error(f"Deleting order {order.id} due to {status} payment")
                order.delete()
            
            return HttpResponse("Webhook processed successfully", status=200)
                
        except Order.DoesNotExist:
            logger.error(f"Order not found for tx_ref: {tx_ref}")
            return HttpResponse("Order not found", status=404)
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON Decode Error: {str(e)}")
        return HttpResponse("Invalid JSON", status=400)
    except Exception as e:
        logger.error(f"Webhook Processing Error: {str(e)}")
        return HttpResponse(status=500)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

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
                "email": "tB0m1@example.com",
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
                payment_status= payment_response.get('status'),
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
        
    @action(detail=False, methods=['get'], url_path='booked-seats/(?P<showing_id>[^/.]+)')
    def booked_seats(self, request, showing_id=None):
        movie_orders = Order.objects.filter(showing_id=showing_id)

        booked_seats = []
        for order in movie_orders:
            booked_seats.extend(order.seats)
        return Response({"booked_seats": booked_seats}, status=status.HTTP_200_OK)