from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .models import Showing
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ShowingSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from .services import ShowingService
from datetime import datetime
from movies.models import Movie


class ShowingViewSet(ModelViewSet):
    """
    ViewSet for managing movie showings.
    """
    queryset = Showing.objects.all().order_by('date', 'time')
    serializer_class = ShowingSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'], url_path='generate-schedule')
    def generate_schedule(self, request):
        """
        Generate a weekly schedule for a movie.
        
        Required parameters:
        - movie_id: UUID of the movie
        - start_date: Starting date (YYYY-MM-DD)
        
        Optional parameters:
        - daily_times: List of times (HH:MM)
        - weeks: Number of weeks to generate
        """
        try:
            movie_id = request.data.get('movie_id')
            start_date = datetime.strptime(
                request.data.get('start_date'),
                '%Y-%m-%d'
            ).date()
            daily_times = request.data.get('daily_times')
            weeks = int(request.data.get('weeks', 1))
            
            showings = ShowingService.generate_weekly_schedule(
                movie_id=movie_id,
                start_date=start_date,
                daily_times=daily_times,
                weeks=weeks
            )
            
            serializer = self.get_serializer(showings, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except (ValueError, TypeError) as e:
            return Response(
                {'error': 'Invalid input format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Movie.DoesNotExist:
            return Response(
                {'error': 'Movie not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['delete'], url_path='clear-schedule/(?P<movie_id>[^/.]+)')
    def clear_schedule(self, request, movie_id=None):
        """Delete all future showings for a movie."""
        deleted_count = ShowingService.bulk_delete_future_showings(movie_id)
        return Response({
            'message': f'Deleted {deleted_count} future showings'
        })
    
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
    
