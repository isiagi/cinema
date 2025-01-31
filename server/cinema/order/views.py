from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Order
from .serializers import OrderSerializer

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
