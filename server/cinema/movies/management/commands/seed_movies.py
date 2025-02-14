from django.core.management.base import BaseCommand
from movies.models import Movie
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seed database with sample movies'

    def handle(self, *args, **kwargs):
        movies = [
    {
        "title": "Moana",
        "description": "An adventurous teenager sails out on a daring mission to save her people",
        "longDescription": "Three thousand years ago, the greatest sailors in the world voyaged across the vast Pacific Ocean, discovering the many islands of Oceania. But then, for a millennium, their voyages stopped – and no one knows why. Throughout the small island of Motunui, nestled in the heart of the Pacific, Moana, the strong-willed daughter of Chief Tui, has always been drawn to the ocean despite her father's explicit rules forbidding anyone from venturing beyond the reef. When her island faces a devastating ecological crisis, with coconuts rotting and fish becoming scarce, Moana learns about an ancient curse caused by the Demigod Maui stealing the heart of Te Fiti, the mother island. Against her father's wishes but with her grandmother's blessing and the ocean's guidance, Moana embarks on an epic journey across the Pacific to find Maui and restore the heart of Te Fiti. Along the way, she must navigate treacherous waters, face fearsome monsters including the giant crab Tamatoa, and discover her own identity as a wayfinder, all while racing against time to save her people and their way of life. Her journey becomes not just a mission to save her island, but a voyage of self-discovery, legacy, and the rekindling of her people's ancient traditions.",
        "image": "https://m.media-amazon.com/images/M/MV5BMjI4MzU5NTExNF5BMl5BanBnXkFtZTgwNzY1MTEwMDI@._V1_.jpg",
        "rating": 7.6,
        "actor": ["Auli'i Cravalho", "Dwayne Johnson"],
        "duration": "1h 47m",
        "highlight": "Animated Adventure",
        "size": "large",
        "language": "English",
        "releaseDate": "2016-11-23",
        "director": "Ron Clements, John Musker",
        "trailerUrl": "https://www.youtube.com/watch?v=LKFuXETZUsI",
        "status": "Now_Showing"
    },
    {

        "title": "Captain America: Brave New World",
        "description": "Political involvement in the Avengers' affairs causes a rift between Captain America and Iron Man",
        "longDescription": "Following the catastrophic events in Sokovia and Lagos, which resulted in massive civilian casualties despite the Avengers' intervention, the United Nations prepares to pass the Sokovia Accords – a legal framework that would establish a UN panel to oversee and control the Avengers. This controversial decision splinters the team into opposing factions, led by Steve Rogers (Captain America) and Tony Stark (Iron Man). Steve Rogers believes the Avengers should remain free to defend humanity without government interference, fearing that politics and bureaucracy could prevent them from helping when needed most. Tony Stark, haunted by his role in creating Ultron and the subsequent destruction, supports oversight, seeing it as a necessary step to ensure accountability. The situation becomes even more complex when Steve's old friend Bucky Barnes, the Winter Soldier, is framed for a terrorist bombing at the UN meeting in Vienna where the Accords are to be ratified. As Captain America fights to protect his friend from a worldwide manhunt, more heroes are drawn into the conflict. Black Panther, seeking revenge for his father's death in the bombing, joins Stark's pro-Accords faction, while Falcon, Scarlet Witch, and others align with Rogers. The conflict escalates into an all-out civil war between former allies, culminating in a devastating battle at a German airport and a more personal, brutal confrontation when a dark secret about Tony's parents is revealed. The film explores themes of friendship, loyalty, responsibility, and the price of revenge, while questioning whether freedom or security should be prioritized in an increasingly dangerous world.",
        "image": "https://res.cloudinary.com/isiagi/image/upload/v1738801024/m4st2smiuudiql3rjadq.jpg",

        "rating": 7.8,
        "actor": ["Chris Evans", "Robert Downey Jr."],
        "duration": "2h 27m",
        "highlight": "Superhero Action",
        "size": "small",
        "language": "English",
        "releaseDate": "2016-05-06",
        "director": "Anthony Russo, Joe Russo",
        "trailerUrl": "https://www.youtube.com/watch?v=1pHDWnXmK7Y",

        "status": "Coming_Soon"

    },
    {
        "title": "Mufasa: The Lion King",
        "description": "The origin story of Mufasa, the legendary Lion King",
        "longDescription": "Before he became the legendary Lion King, Mufasa's story was one of struggle, brotherhood, and destiny. Born into a pride during a time of great upheaval in the African savanna, young Mufasa and his brother Taka (later known as Scar) face numerous challenges that will shape their divergent paths. The film explores their early years, revealing how Mufasa's natural leadership abilities and strong moral compass began to emerge, while his brother's resentment and ambition slowly consumed him. Through the guidance of Rafiki, a young mandrill shaman, Mufasa learns the delicate balance of ruling with both strength and compassion. The story delves deep into the complex dynamics of the pride lands, showing how Mufasa forms crucial alliances with other animals, including his first encounters with Zazu, who becomes his loyal majordomo. As drought and danger threaten the pride lands, Mufasa must step up to protect his family and territory from rival lions and hyenas, while dealing with his brother's growing jealousy and darkness. The narrative also explores Mufasa's journey to understand the concept of the Circle of Life, his first love, and the events that led to his eventual marriage to Sarabi. Through trials, victories, and heartbreaking betrayals, we witness the transformation of a young lion into the wise and powerful king who would later guide his son Simba. The film also reveals the origins of many of the pride lands' most important traditions and the deep-rooted conflicts that would eventually lead to the events of The Lion King. This epic tale combines themes of family, responsibility, betrayal, and the weight of destiny, all set against the backdrop of the majestic African wilderness.",
        "image": "https://res.cloudinary.com/isiagi/image/upload/v1738801026/t9vztgetn74d0suovsny.jpg",
        "rating": 8.2,
        "actor": ["Aaron Pierre", "Kelvin Harrison Jr."],
        "duration": "2h 10m",
        "highlight": "Animated Drama",
        "size": "small",
        "language": "English",
        "releaseDate": "2024-12-20",
        "director": "Barry Jenkins",

        "trailerUrl": "https://www.youtube.com/watch?v=o17MF9vnabg",

        "status": "Now_Showing"
    },
    # {
    #     "title": "Mufasa: The Lion King",
    #     "description": "The origin story of Mufasa, the legendary Lion King",
    #     "longDescription": "Before he became the legendary Lion King, Mufasa's story was one of struggle, brotherhood, and destiny. Born into a pride during a time of great upheaval in the African savanna, young Mufasa and his brother Taka (later known as Scar) face numerous challenges that will shape their divergent paths. The film explores their early years, revealing how Mufasa's natural leadership abilities and strong moral compass began to emerge, while his brother's resentment and ambition slowly consumed him. Through the guidance of Rafiki, a young mandrill shaman, Mufasa learns the delicate balance of ruling with both strength and compassion. The story delves deep into the complex dynamics of the pride lands, showing how Mufasa forms crucial alliances with other animals, including his first encounters with Zazu, who becomes his loyal majordomo. As drought and danger threaten the pride lands, Mufasa must step up to protect his family and territory from rival lions and hyenas, while dealing with his brother's growing jealousy and darkness. The narrative also explores Mufasa's journey to understand the concept of the Circle of Life, his first love, and the events that led to his eventual marriage to Sarabi. Through trials, victories, and heartbreaking betrayals, we witness the transformation of a young lion into the wise and powerful king who would later guide his son Simba. The film also reveals the origins of many of the pride lands' most important traditions and the deep-rooted conflicts that would eventually lead to the events of The Lion King. This epic tale combines themes of family, responsibility, betrayal, and the weight of destiny, all set against the backdrop of the majestic African wilderness.",
    #     "image": "https://res.cloudinary.com/isiagi/image/upload/v1738801026/t9vztgetn74d0suovsny.jpg",
    #     "rating": 8.2,
    #     "actor": ["Aaron Pierre", "Kelvin Harrison Jr."],
    #     "duration": "2h 10m",
    #     "highlight": "Animated Drama",
    #     "size": "large",
    #     "language": "English",
    #     "releaseDate": "2024-12-20",
    #     "director": "Barry Jenkins",
    #     "trailerUrl": "https://www.youtube.com/watch?v=N8UxL_YD5H8",
    #     "status": "Coming_Soon"
    # },
    # {
    #     "title": "Moana",
    #     "description": "An adventurous teenager sails out on a daring mission to save her people",
    #     "longDescription": "Three thousand years ago, the greatest sailors in the world voyaged across the vast Pacific Ocean, discovering the many islands of Oceania. But then, for a millennium, their voyages stopped – and no one knows why. Throughout the small island of Motunui, nestled in the heart of the Pacific, Moana, the strong-willed daughter of Chief Tui, has always been drawn to the ocean despite her father's explicit rules forbidding anyone from venturing beyond the reef. When her island faces a devastating ecological crisis, with coconuts rotting and fish becoming scarce, Moana learns about an ancient curse caused by the Demigod Maui stealing the heart of Te Fiti, the mother island. Against her father's wishes but with her grandmother's blessing and the ocean's guidance, Moana embarks on an epic journey across the Pacific to find Maui and restore the heart of Te Fiti. Along the way, she must navigate treacherous waters, face fearsome monsters including the giant crab Tamatoa, and discover her own identity as a wayfinder, all while racing against time to save her people and their way of life. Her journey becomes not just a mission to save her island, but a voyage of self-discovery, legacy, and the rekindling of her people's ancient traditions.",
    #     "image": "https://m.media-amazon.com/images/M/MV5BMjI4MzU5NTExNF5BMl5BanBnXkFtZTgwNzY1MTEwMDI@._V1_.jpg",
    #     "rating": 7.6,
    #     "actor": ["Auli'i Cravalho", "Dwayne Johnson"],
    #     "duration": "1h 47m",
    #     "highlight": "Animated Adventure",
    #     "size": "small",
    #     "language": "English",
    #     "releaseDate": "2016-11-23",
    #     "director": "Ron Clements, John Musker",
    #     "trailerUrl": "https://www.youtube.com/watch?v=LKFuXETZUsI",
    #     "status": "Now_Showing"
    # },

    # {
    #     "title": "Captain America: Civil War",
    #     "description": "Political involvement in the Avengers' affairs causes a rift between Captain America and Iron Man",
    #     "longDescription": "Following the catastrophic events in Sokovia and Lagos, which resulted in massive civilian casualties despite the Avengers' intervention, the United Nations prepares to pass the Sokovia Accords – a legal framework that would establish a UN panel to oversee and control the Avengers. This controversial decision splinters the team into opposing factions, led by Steve Rogers (Captain America) and Tony Stark (Iron Man). Steve Rogers believes the Avengers should remain free to defend humanity without government interference, fearing that politics and bureaucracy could prevent them from helping when needed most. Tony Stark, haunted by his role in creating Ultron and the subsequent destruction, supports oversight, seeing it as a necessary step to ensure accountability. The situation becomes even more complex when Steve's old friend Bucky Barnes, the Winter Soldier, is framed for a terrorist bombing at the UN meeting in Vienna where the Accords are to be ratified. As Captain America fights to protect his friend from a worldwide manhunt, more heroes are drawn into the conflict. Black Panther, seeking revenge for his father's death in the bombing, joins Stark's pro-Accords faction, while Falcon, Scarlet Witch, and others align with Rogers. The conflict escalates into an all-out civil war between former allies, culminating in a devastating battle at a German airport and a more personal, brutal confrontation when a dark secret about Tony's parents is revealed. The film explores themes of friendship, loyalty, responsibility, and the price of revenge, while questioning whether freedom or security should be prioritized in an increasingly dangerous world.",
    #     "image": "https://m.media-amazon.com/images/M/MV5BMjQ0MTgyNjAxMV5BMl5BanBnXkFtZTgwNjUzMDkyODE@._V1_.jpg",
    #     "rating": 7.8,
    #     "actor": ["Chris Evans", "Robert Downey Jr."],
    #     "duration": "2h 27m",
    #     "highlight": "Superhero Action",
    #     "size": "small",
    #     "language": "English",
    #     "releaseDate": "2016-05-06",
    #     "director": "Anthony Russo, Joe Russo",
    #     "trailerUrl": "https://www.youtube.com/watch?v=o17MF9vnabg&t=3s",
    #     "status": "Now_Showing"
    # },

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