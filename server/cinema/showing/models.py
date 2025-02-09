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
    includes_3d_glasses = models.BooleanField(default=False)
    includes_popcorn = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Set pricing and add-ons based on the day of the week
        if self.date.weekday() == 0:  # Monday
            self.price = 10000
            self.includes_3d_glasses = True
            self.includes_popcorn = False
        elif self.date.weekday() == 1:  # Tuesday and Wednesday
            self.price = 15000
            self.includes_3d_glasses = True
            self.includes_popcorn = True
        elif self.date.weekday() == 2:  # Wednesday
            self.price = 30000
            self.includes_3d_glasses = True
            self.includes_popcorn = False
        elif self.date.weekday() == 3:  # Thursday
            self.price = 12000
            self.includes_3d_glasses = True
            self.includes_popcorn = False
        elif self.date.weekday() in [4, 5, 6]:  # Friday, Saturday, Sunday
            self.price = 15000
            self.includes_3d_glasses = True
            self.includes_popcorn = False
        
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.price

    def __str__(self):
        return f"{self.movie.title} - {self.date} at {self.time}"