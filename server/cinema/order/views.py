from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from .models import Order
from .serializers import OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from showing.models import Showing

class OrderViewSet(ModelViewSet):
    """
    ViewSet for managing user-specific orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve only orders belonging to the logged-in user.
        """
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        Associate the logged-in user with the order before saving.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Ensure only the owner can update the order.
        """
        order = self.get_object()
        if order.user != self.request.user:
            raise PermissionDenied("You are not allowed to update this order.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Ensure only the owner can delete the order.
        """
        if instance.user != self.request.user:
            raise PermissionDenied("You are not allowed to delete this order.")
        instance.delete()

    # @permission_classes([AllowAny])
    # @action(detail=False, methods=['get'], url_path='booked-seats/(?P<showing_id>[^/.]+)', )
    @action(detail=False, methods=['get'], url_path='booked-seats/(?P<showing_id>[^/.]+)', permission_classes=[AllowAny])
    def booked_seats(self, request, showing_id=None):
        """
        Get all booked seats for a specific movie showing by showing ID.
        """

        # Now, filter orders using the UUID of the showing
        movie_orders = Order.objects.filter(showing=showing_id)

        # Extract only seat lists
        booked_seats = []
        for order in movie_orders:
            booked_seats.extend(order.seats) 

        return Response({"booked_seats": booked_seats}, status=status.HTTP_200_OK)
