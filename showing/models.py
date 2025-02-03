from django.db import models
from django.utils.timezone import now
import uuid
from movies.models import Movie

class Showing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showings", to_field="id")
    date = models.DateField()
    time = models.TimeField()
    price = models.FloatField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movie.title} - {self.date} at {self.time}"
