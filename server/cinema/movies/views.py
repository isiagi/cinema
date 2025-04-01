from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import cloudinary
import cloudinary.uploader
from rest_framework.exceptions import ValidationError


class MovieViewSet(ModelViewSet):
    """
    ViewSet for managing movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticatedOrReadOnly])
    def get_movie(self, request, pk=None):
        """
        Fetch a single movie based on its ID.
        """
        movie = self.get_object()
        serializer = self.get_serializer(movie)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticatedOrReadOnly])
    def by_status(self, request):
        """
        Get movies filtered by status.
        Example usage: /movies/by_status/?status=Released
        """
        status = request.query_params.get("status")
        if not status:
            return Response({"error": "Status parameter is required"}, status=400)
        
        movies = Movie.objects.filter(status=status)
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

     # Remove the created_by parameter if not in model
    def create(self, request, *args, **kwargs):
        movie_data = request.data

        # Ensure image is provided in request.FILES
        image_file = request.FILES.get('image')
        if not image_file:
            raise ValidationError({"image": "Image file is required."})

        # Try uploading the image to Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(image_file)
            movie_data['image'] = upload_result['url']
        except Exception as e:
            raise ValidationError({"image": f"Image upload failed: {str(e)}"})

        # Validate and save the movie data
        serializer = self.get_serializer(data=movie_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=201)
    
        

    def perform_update(self, serializer):
        serializer.save()  # Remove the updated_by parameter if not in model

    def perform_destroy(self, instance):
        instance.delete()  # Simplify if fields don't exist
