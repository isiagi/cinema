from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class MovieViewSet(ModelViewSet):
    """
    ViewSet for managing movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticatedOrReadOnly])
    def get_movie(self, request, pk=None):
        """
        Fetch a single movie based on its ID.
        """
        movie = self.get_object()
        serializer = self.get_serializer(movie)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Restrict movie creation to authenticated users.
        """
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """
        Restrict movie updates to the user who created the movie.
        """
        movie = self.get_object()
        if movie.created_by != self.request.user:
            raise PermissionDenied("You are not allowed to update this movie.")
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """
        Restrict movie deletion to the user who created the movie.
        """
        if instance.created_by != self.request.user:
            raise PermissionDenied("You are not allowed to delete this movie.")
        instance.deleted_by = self.request.user
        instance.save()
        instance.delete()
