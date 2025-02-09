# models.py
from django.db import models
from django.contrib.auth import get_user_model
import uuid

class Order(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    showing = models.ForeignKey('showing.Showing', on_delete=models.CASCADE)
    seats = models.JSONField()  # Store as JSON array
    eats = models.JSONField(null=True, blank=True)  # Store as JSON object
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']