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
import logging

logger = logging.getLogger(__name__)


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
            payload = {
                "tx_ref": f"tx-{timezone.now().timestamp()}",
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
                    "Authorization": f"Bearer FLWSECK_TEST-0e7756b790368aec82c444801b5cdfbd-X",
                    "Content-Type": "application/json",
                }
            )

            if response.status_code != 200:
                logger.error(f"Flutterwave payment initiation failed: {response.text}")
                raise ValidationError("Payment initiation failed")

            return response.json()

        except requests.RequestException as e:
            logger.error(f"Payment request failed: {str(e)}")
            raise ValidationError("Payment service unavailable")

    def verify_payment(self, transaction_id):
        """
        Verify payment status with Flutterwave
        """
        try:
            response = requests.get(
                f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify",
                headers={
                    "Authorization": f"Bearer FLWSECK-bdcb6f1354bae4f976fba2086b2af753-194ec5052bfvt-X"
                }
            )

            if response.status_code != 200:
                logger.error(f"Payment verification failed: {response.text}")
                return False

            data = response.json()
            return data.get('status') == 'successful'

        except requests.RequestException as e:
            logger.error(f"Payment verification request failed: {str(e)}")
            return False

    def create(self, request, *args, **kwargs):
        try:
            payment_data = request.data.get('payment', {})
            if not all([
                payment_data.get('phone_number'),
                payment_data.get('provider'),
                request.data.get('total_price')
            ]):
                raise ValidationError("Missing payment information")

            # Ensure the user is assigned before creating the order
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)  # Explicitly set user

            payment_response = self.initiate_payment(
                amount=request.data.get('total_price'),
                phone_number=payment_data.get('phone_number'),
                provider=payment_data.get('provider')
            )

            if payment_response.get('status') != 'success':
                raise ValidationError("Payment initiation failed")
            
            print(payment_response)

            request.data['payment_reference'] = payment_response['status']

            response_data = {
                'order': serializer.data,
                'payment': {
                    'transaction_id': payment_response['status'],
                    'status': 'pending',
                    'instructions': payment_response.get('meta', {}).get('authorization', {})
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Order creation failed: {str(e)}")
            return Response(
                {'error': 'Order creation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @action(detail=True, methods=['post'])
    def verify_order_payment(self, request, pk=None):
        """
        Verify payment status for an order
        """
        order = self.get_object()

        print(order.payment_reference)
        
        if not order.payment_reference:
            return Response(
                {'error': 'No payment reference found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment_verified = self.verify_payment(order.payment_reference)
        
        if payment_verified:
            order.payment_status = 'completed'
            order.save()
            return Response({'status': 'Payment verified'})
        
        return Response(
            {'error': 'Payment verification failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


    @action(detail=False, methods=['get'], url_path='booked-seats/(?P<showing_id>[^/.]+)')
    def booked_seats(self, request, showing_id=None):
        movie_orders = Order.objects.filter(showing_id=showing_id)

        booked_seats = []
        for order in movie_orders:
            booked_seats.extend(order.seats)
        return Response({"booked_seats": booked_seats}, status=status.HTTP_200_OK)