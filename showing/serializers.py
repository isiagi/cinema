from rest_framework import serializers
from .models import Showing

class ShowingSerializer(serializers.ModelSerializer):
    movie_title = serializers.ReadOnlyField(source='movie.title')  # Include the movie title in the response

    class Meta:
        model = Showing
        fields = ['id', 'movie', 'movie_title', 'date', 'time', 'price', 'created_at', 'updated_at']
