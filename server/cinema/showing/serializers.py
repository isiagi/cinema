from rest_framework import serializers
from .models import Showing

class ShowingSerializer(serializers.ModelSerializer):
    movie_title = serializers.ReadOnlyField(source='movie.title')  # Include the movie title in the response
    movie_img = serializers.ReadOnlyField(source='movie.image')

    class Meta:
        model = Showing
        fields = ['id', 'movie', 'movie_title', 'date', 'time', 'price', 'created_at', 'movie_img', 'updated_at', 'includes_3d_glasses', 'includes_popcorn']
