from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user-specific orders.
    """
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve only orders belonging to the authenticated user.
        """
        if not self.request.user.is_authenticated:
            return Order.objects.none()
        
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

    @action(detail=False, methods=['get'], url_path='user-orders/(?P<user_id>[^/.]+)')
    def user_orders(self, request, user_id=None):
        """
        Retrieve orders for a specific user.
        """
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=401)
        
        user_orders = Order.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = self.get_serializer(user_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='booked-seats/(?P<showing_id>[^/.]+)')
    # @permission_classes([AllowAny])
    def booked_seats(self, request, showing_id=None):
        """
        Get all booked seats for a specific movie showing by showing ID.
        """
        # Fetch orders for the given showing ID
        movie_orders = Order.objects.filter(showing_id=showing_id)

        # Extract only seat lists
        booked_seats = []
        for order in movie_orders:
            booked_seats.extend(order.seats) 

        return Response({"booked_seats": booked_seats}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='can-delete')
    def can_delete(self, request, pk=None):
        """
        Check if the user can delete the order.
        """
        order = get_object_or_404(Order, pk=pk)
        
        can_delete = request.user.is_superuser or request.user.is_staff or order.user == request.user

        return Response({"can_delete": can_delete}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        """
        Ensure only the owner, admin, or staff can delete the order.
        """
        user = self.request.user
        
        if user.is_staff or user.is_superuser or instance.user == user:
            instance.delete()
        else:
            raise PermissionDenied("You are not allowed to delete this order.")
    
        
