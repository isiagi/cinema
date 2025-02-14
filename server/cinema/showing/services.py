from datetime import datetime, timedelta
from typing import List
from django.utils import timezone
from .models import Showing, Movie

class ShowingService:
    """Service class to handle showing-related operations"""
    
    @staticmethod
    def generate_weekly_schedule(
        movie_id: str,
        start_date: datetime.date,
        daily_times: List[str] = None,
        weeks: int = 1
    ) -> List[Showing]:
        """
        Generate a weekly schedule of showings for a movie.
        
        Args:
            movie_id: UUID of the movie
            start_date: Starting date for the schedule
            daily_times: List of showing times (default: ['14:00', '17:00', '20:00'])
            weeks: Number of weeks to generate schedule for
        
        Returns:
            List of created Showing instances
        """
        if daily_times is None:
            daily_times = ['14:00', '17:00', '20:00']
            
        movie = Movie.objects.get(id=movie_id)
        showings = []
        
        # Generate showings for the specified number of weeks
        for week in range(weeks):
            # For each day in the week
            for day in range(7):
                current_date = start_date + timedelta(days=day + (week * 7))
                
                # Create showings for each time slot
                for time_str in daily_times:
                    time_obj = datetime.strptime(time_str, '%H:%M').time()
                    
                    # Check if showing already exists
                    if not Showing.objects.filter(
                        movie=movie,
                        date=current_date,
                        time=time_obj
                    ).exists():
                        showing = Showing.objects.create(
                            movie=movie,
                            date=current_date,
                            time=time_obj
                        )
                        showings.append(showing)
        
        return showings

    @staticmethod
    def bulk_delete_future_showings(movie_id: str) -> int:
        """
        Delete all future showings for a movie.
        
        Args:
            movie_id: UUID of the movie
            
        Returns:
            Number of deleted showings
        """
        today = timezone.now().date()
        return Showing.objects.filter(
            movie_id=movie_id,
            date__gte=today
        ).delete()[0]

    @staticmethod
    def get_showing_schedule(
        movie_id: str,
        start_date: datetime.date = None,
        end_date: datetime.date = None
    ) -> List[dict]:
        """
        Get the schedule of showings for a movie within a date range.
        
        Args:
            movie_id: UUID of the movie
            start_date: Start date for filtering (default: today)
            end_date: End date for filtering (default: week from start_date)
            
        Returns:
            List of showings grouped by date
        """
        if start_date is None:
            start_date = timezone.now().date()
        if end_date is None:
            end_date = start_date + timedelta(days=7)
            
        showings = Showing.objects.filter(
            movie_id=movie_id,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date', 'time')
        
        schedule = {}
        for showing in showings:
            date_str = showing.date.strftime('%Y-%m-%d')
            if date_str not in schedule:
                schedule[date_str] = []
            schedule[date_str].append({
                'id': showing.id,
                'time': showing.time.strftime('%H:%M'),
                'price': showing.price,
                'includes_3d_glasses': showing.includes_3d_glasses,
                'includes_popcorn': showing.includes_popcorn
            })
            
        return schedule