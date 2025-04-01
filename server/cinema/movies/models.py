from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

# Create your models here.
class Movie(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        RELEASED = 'Released', 'Released'
        COMING_SOON = 'Coming Soon', 'Coming Soon'
        CANCELLED = 'Cancelled', 'Cancelled',
        NOW_SHOWING = 'Now Showing', 'Now Showing'


    id = models.SlugField(primary_key=True, max_length=255, unique=True, editable=False)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    longDescription = models.TextField()
    image = CloudinaryField('image', blank=True, null=True, resource_type='image')
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    actor = models.JSONField()
    duration = models.CharField(max_length=500)
    highlight = models.CharField(max_length=500)
    size = models.CharField(max_length=300)
    language = models.CharField(max_length=300)
    releaseDate = models.DateField(null=True, blank=True)
    director = models.CharField(max_length=1000)
    trailerUrl = models.CharField(max_length=1000)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)


    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = slugify(self.title)  # Generate a slug from title if not set
        super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return self.title