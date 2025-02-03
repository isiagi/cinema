from django.db import models
from django.utils.timezone import now
import uuid
from user.models import User
from showing.models import Showing

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE, related_name="orders")
    seats = models.JSONField()
    eats = models.JSONField()
    total_price = models.FloatField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order by {self.user.email} for {self.showing.movie.title}"
