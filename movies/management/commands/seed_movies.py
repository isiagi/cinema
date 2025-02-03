from django.core.management.base import BaseCommand
from movies.models import Movie
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seed database with sample movies'

    def handle(self, *args, **kwargs):
        movies = [
            {
                "title": "Inception",
                "description": "A mind-bending thriller",
                "longDescription": "Dom Cobb is a skilled thief...",
                "image": "https://m.media-amazon.com/images/M/MV5BMjExMjkwNTQ0Nl5BMl5BanBnXkFtZTcwNTY0OTk1Mw@@._V1_.jpg",
                "rating": 8.8,
                "actor": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"],
                "duration": "2h 28m",
                "highlight": "Sci-Fi Thriller",
                "size": "large",
                "language": "English",
                "releaseDate": "2010-07-16",
                "director": "Christopher Nolan",
                "trailerUrl": "https://www.youtube.com/watch?v=YoHD9XEInc0",
                "status": "Available"
            },
            {
                "title": "The Dark Knight",
                "description": "Batman vs Joker",
                "longDescription": "Batman faces Joker in Gotham...",
                "image": "https://m.media-amazon.com/images/S/pv-target-images/e9a43e647b2ca70e75a3c0af046c4dfdcd712380889779cbdc2c57d94ab63902.jpg",
                "rating": 9.0,
                "actor": ["Christian Bale", "Heath Ledger"],
                "duration": "2h 32m",
                "highlight": "Superhero Thriller",
                "size": "small",
                "language": "English",
                "releaseDate": "2008-07-18",
                "director": "Christopher Nolan",
                "trailerUrl": "https://www.youtube.com/watch?v=EXeTwQWrcwY",
                "status": "Available"
            },
            {
                "title": "Interstellar",
                "description": "A journey beyond the stars",
                "longDescription": "A group of explorers travel through a wormhole...",
                "image": "https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
                "rating": 8.6,
                "actor": ["Matthew McConaughey", "Anne Hathaway"],
                "duration": "2h 49m",
                "highlight": "Sci-Fi Adventure",
                "size": "small",
                "language": "English",
                "releaseDate": "2014-11-07",
                "director": "Christopher Nolan",
                "trailerUrl": "https://www.youtube.com/watch?v=Rvns5DaW-ug",
                "status": "Available"
            },
            {
                "title": "Avengers: Endgame",
                "description": "The final battle against Thanos",
                "longDescription": "The Avengers assemble to undo Thanos' snap...",
                "image": "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_FMjpg_UX1000_.jpg",
                "rating": 8.4,
                "actor": ["Robert Downey Jr.", "Chris Evans"],
                "duration": "3h 2m",
                "highlight": "Superhero Action",
                "size": "small",
                "language": "English",
                "releaseDate": "2019-04-26",
                "director": "Anthony Russo, Joe Russo",
                "trailerUrl": "https://www.youtube.com/watch?v=BKviRM0KF2A",
                "status": "Available"
            },
            {
                "title": "Titanic",
                "description": "A tragic love story",
                "longDescription": "A love story set on the doomed ship...",
                "image": "https://m.media-amazon.com/images/M/MV5BYzYyN2FiZmUtYWYzMy00MzViLWJkZTMtOGY1ZjgzNWMwN2YxXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
                "rating": 7.9,
                "actor": ["Leonardo DiCaprio", "Kate Winslet"],
                "duration": "3h 14m",
                "highlight": "Romance Drama",
                "size": "smalll",
                "language": "English",
                "releaseDate": "1997-12-19",
                "director": "James Cameron",
                "trailerUrl": "https://www.youtube.com/watch?v=I7c1etV7D7g&t=5s",
                "status": "Available"
            },
            {
                "title": "The Matrix",
                "description": "A cyberpunk action thriller",
                "longDescription": "A hacker discovers the reality is a simulation...",
                "image": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fencrypted-tbn0.gstatic.com%2Fimages%3Fq%3Dtbn%3AANd9GcR5DoFtShSmClflZ0RzBj9JBMweU5IUVBCeEbbLeV2XPlCnTKNi&psig=AOvVaw30H88ts3Auvm3_jsbQ3OBw&ust=1738418109827000&source=images&cd=vfe&opi=89978449&ved=0CBAQjRxqFwoTCNDaiqOOoIsDFQAAAAAdAAAAABAE",
                "rating": 8.7,
                "actor": ["Keanu Reeves", "Laurence Fishburne"],
                "duration": "2h 16m",
                "highlight": "Sci-Fi Action",
                "size": "large",
                "language": "English",
                "releaseDate": "1999-03-31",
                "director": "The Wachowskis",
                "trailerUrl": "https://www.youtube.com/watch?v=d-wBjHZRSJA",
                "status": "Available"
            },
            {
                "title": "Forrest Gump",
                "description": "Life is like a box of chocolates",
                "longDescription": "The story of a man who influences history...",
                "image": "https://m.media-amazon.com/images/M/MV5BNDYwNzVjMTItZmU5YS00YjQ5LTljYjgtMjY2NDVmYWMyNWFmXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
                "rating": 8.8,
                "actor": ["Tom Hanks", "Robin Wright"],
                "duration": "2h 22m",
                "highlight": "Drama",
                "size": "small",
                "language": "English",
                "releaseDate": "1994-07-06",
                "director": "Robert Zemeckis",
                "trailerUrl": "https://www.youtube.com/watch?v=bLvqoHBptjg",
                "status": "Available"
            },
            {
                "title": "Joker",
                "description": "A psychological thriller",
                "longDescription": "A failed comedian turns to crime...",
                "image": "https://m.media-amazon.com/images/M/MV5BNzY3OWQ5NDktNWQ2OC00ZjdlLThkMmItMDhhNDk3NTFiZGU4XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
                "rating": 8.5,
                "actor": ["Joaquin Phoenix", "Robert De Niro"],
                "duration": "2h 2m",
                "highlight": "Crime Drama",
                "size": "small",
                "language": "English",
                "releaseDate": "2019-10-04",
                "director": "Todd Phillips",
                "trailerUrl": "https://www.youtube.com/watch?v=2mNOqRHdVzY",
                "status": "Available"
            },
            {
                "title": "Shutter Island",
                "description": "A psychological mystery",
                "longDescription": "A detective investigates a mental hospital...",
                "image": "https://m.media-amazon.com/images/M/MV5BN2FjNWExYzEtY2YzOC00YjNlLTllMTQtNmIwM2Q1YzBhOWM1XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
                "rating": 8.1,
                "actor": ["Leonardo DiCaprio", "Mark Ruffalo"],
                "duration": "2h 18m",
                "highlight": "Mystery Thriller",
                "size": "small",
                "language": "English",
                "releaseDate": "2010-02-19",
                "director": "Martin Scorsese",
                "trailerUrl": "https://www.youtube.com/watch?v=v8yrZSkKxTA",
                "status": "Available"
            },
            {
                "title": "The Shawshank Redemption",
                "description": "A story of hope and friendship",
                "longDescription": "A banker is imprisoned and finds redemption...",
                "image": "https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@._V1_.jpg",
                "rating": 9.3,
                "actor": ["Tim Robbins", "Morgan Freeman"],
                "duration": "2h 22m",
                "highlight": "Drama",
                "size": "small",
                "language": "English",
                "releaseDate": "1994-09-23",
                "director": "Frank Darabont",
                "trailerUrl": "https://www.youtube.com/watch?v=PLl99DlL6b4",
                "status": "Available"
            }
        ]

        for movie_data in movies:
            movie, created = Movie.objects.get_or_create(
                id=slugify(movie_data['title']),
                defaults=movie_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added movie: {movie.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Movie already exists: {movie.title}"))
