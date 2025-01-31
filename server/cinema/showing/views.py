from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Showing
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ShowingSerializer
from rest_framework.exceptions import PermissionDenied


class ShowingViewSet(ModelViewSet):
    """
    ViewSet for managing movie showings.
    """
    queryset = Showing.objects.all().order_by('date', 'time')
    serializer_class = ShowingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'], url_path='movie/(?P<movie_id>[^/.]+)')
    def showings_by_movie(self, request, movie_id=None):
        """
        Custom endpoint to get all showings for a given movie.
        """
        showings = Showing.objects.filter(movie=movie_id)
        serializer = self.get_serializer(showings, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Allow only authenticated users to create showings.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Restrict updates to the user who created the showing (if applicable).
        """
        showing = self.get_object()
        # Example: Add logic to check ownership if needed
        serializer.save()

    def perform_destroy(self, instance):
        """
        Restrict deletion to authenticated users (additional checks can be added).
        """
        instance.delete()

    def show_showing_for_a_movie_based_on_movieId(self, movie):
        """
        Return all showings for a given movie.
        """
        return Showing.objects.filter(movie=movie)
    
