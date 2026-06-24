"""
Idempotent seed command.  Run via: python manage.py seed

Inserts exactly 10 rows in each entity table:
  Genre (10) · Director (10) · Actor (10) · Movie (10) · Review (10)

All FK and M2M relations are explicit — no randomness, fully reproducible.
Re-running is safe; get_or_create prevents duplicates.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from catalog.models import Actor, Director, Genre, Movie, Review

# ---------------------------------------------------------------------------
# 10 Genres
# ---------------------------------------------------------------------------
GENRES: list[str] = [
    "Action",           # 1
    "Drama",            # 2
    "Science Fiction",  # 3
    "Crime",            # 4
    "Thriller",         # 5
    "Comedy",           # 6
    "Adventure",        # 7
    "Romance",          # 8
    "Horror",           # 9
    "Animation",        # 10
]

# ---------------------------------------------------------------------------
# 10 Directors  (birth_date, bio, Wikimedia portrait URL)
# ---------------------------------------------------------------------------
DIRECTORS: list[dict] = [
    {
        "name": "Christopher Nolan",
        "birth_date": "1970-07-30",
        "bio": (
            "British-American filmmaker celebrated for cerebral, nonlinear narratives. "
            "Known for the Dark Knight trilogy, Inception, Interstellar, and Oppenheimer."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/xuAIuYSmsUzKlUMBFGVZaWsY3DZ.jpg",
    },
    {
        "name": "Steven Spielberg",
        "birth_date": "1946-12-18",
        "bio": (
            "American director and producer widely regarded as one of the most influential filmmakers "
            "in history. Directed Jaws, E.T., Schindler's List, and Saving Private Ryan."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/tZxcg19YQ3e8fJ0pOs7hjlnmmr6.jpg",
    },
    {
        "name": "Quentin Tarantino",
        "birth_date": "1963-03-27",
        "bio": (
            "American filmmaker known for stylised violence, sharp dialogue, and nonlinear storytelling. "
            "Works include Pulp Fiction, Kill Bill, Inglourious Basterds, and Django Unchained."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/1gjcpAa99FAOWGnrUvHEXXsRs7o.jpg",
    },
    {
        "name": "Martin Scorsese",
        "birth_date": "1942-11-17",
        "bio": (
            "American filmmaker associated with gritty crime dramas and psychological character studies. "
            "Directed Goodfellas, Taxi Driver, The Departed, and The Wolf of Wall Street."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/g3DjfKsgZQWZiw30I20hZVk1oMX.jpg",
    },
    {
        "name": "Greta Gerwig",
        "birth_date": "1983-08-04",
        "bio": (
            "American actress and filmmaker who transitioned from indie darling to Hollywood heavyweight. "
            "Directed Lady Bird, Little Women, and the record-breaking Barbie (2023)."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/91v5Mw1e7rsUiO4pj8o3h0KSukb.jpg",
    },
    {
        "name": "Denis Villeneuve",
        "birth_date": "1967-10-03",
        "bio": (
            "Canadian filmmaker acclaimed for visually immersive science fiction and thrillers. "
            "Directed Arrival, Blade Runner 2049, Sicario, and the Dune saga."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/433lXlkdMGXzrpwnKM4Ul1sln15.jpg",
    },
    {
        "name": "James Cameron",
        "birth_date": "1954-08-16",
        "bio": (
            "Canadian filmmaker and deep-sea explorer best known for record-breaking blockbusters. "
            "Directed The Terminator, Aliens, Titanic, and Avatar."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/9NAZnTjBQ9WcXAQEzZpKy4vdQto.jpg",
    },
    {
        "name": "David Fincher",
        "birth_date": "1962-08-28",
        "bio": (
            "American filmmaker recognised for his meticulous visual style and dark subject matter. "
            "Directed Se7en, Fight Club, The Social Network, and Gone Girl."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/tpEczFclQZeKAiCeKZZ0adRvtfz.jpg",
    },
    {
        "name": "Ridley Scott",
        "birth_date": "1937-11-30",
        "bio": (
            "British filmmaker with a decades-long career spanning science fiction, historical epics, "
            "and crime dramas. Directed Alien, Blade Runner, Gladiator, and The Martian."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/zABJmN9opmqD4orWl3KSdCaSo7Q.jpg",
    },
    {
        "name": "Alfonso Cuarón",
        "birth_date": "1961-11-28",
        "bio": (
            "Mexican filmmaker known for his long takes and technical innovation. "
            "Directed Y Tu Mamá También, Children of Men, Gravity, and Roma."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/gaHhrzPfxfc3cbQLkDt54gtP3n1.jpg",
    },
]

# ---------------------------------------------------------------------------
# 10 Actors
# ---------------------------------------------------------------------------
ACTORS: list[dict] = [
    {
        "name": "Leonardo DiCaprio",
        "birth_date": "1974-11-11",
        "bio": (
            "American actor and film producer known for his versatility and intense method performances. "
            "Oscar winner for The Revenant; also known for Inception, Titanic, and The Departed."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/wo2hJpn04vbtmh0B9utCFdsQhxM.jpg",
    },
    {
        "name": "Cillian Murphy",
        "birth_date": "1976-05-25",
        "bio": (
            "Irish actor celebrated for piercing blue eyes and chameleonic range. "
            "Oscar winner for Oppenheimer; also known for Inception and Peaky Blinders."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/dm6V24NjjvjMiCtbMkc8Y2WPm2e.jpg",
    },
    {
        "name": "Tom Hanks",
        "birth_date": "1956-07-09",
        "bio": (
            "American actor and filmmaker, two-time Academy Award winner for Philadelphia and Forrest Gump. "
            "One of the most beloved actors in Hollywood history."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/xndWFsBlClOJFRdhSt4NBwiPq2o.jpg",
    },
    {
        "name": "Christian Bale",
        "birth_date": "1974-01-30",
        "bio": (
            "British-American actor famous for extreme physical transformations for roles. "
            "Oscar winner for The Fighter; known for American Psycho, Batman Begins, and The Dark Knight."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/7Pxez9J8fuPd2Mn9kex13YALrCQ.jpg",
    },
    {
        "name": "Margot Robbie",
        "birth_date": "1990-07-02",
        "bio": (
            "Australian actress and producer who broke through in The Wolf of Wall Street. "
            "Known for I, Tonya, Once Upon a Time in Hollywood, and the blockbuster Barbie (2023)."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/euDPyqLnuwaWMHajcU3oZ9uZezR.jpg",
    },
    {
        "name": "Ryan Gosling",
        "birth_date": "1980-11-12",
        "bio": (
            "Canadian actor who gained acclaim with The Notebook and Half Nelson. "
            "Known for La La Land, Blade Runner 2049, and Barbie, for which he received an Oscar nomination."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/lyUyVARQKhGxaxy0FbPJCQRpiaW.jpg",
    },
    {
        "name": "Timothée Chalamet",
        "birth_date": "1995-12-27",
        "bio": (
            "Franco-American actor who became one of Hollywood's leading young talents with Call Me By Your Name. "
            "Leads Denis Villeneuve's Dune saga and starred in Wonka (2023)."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/BE2sdjpgsa2rNTFa66f7upkaOP.jpg",
    },
    {
        "name": "Matt Damon",
        "birth_date": "1970-10-08",
        "bio": (
            "American actor, screenwriter, and producer. Oscar winner for co-writing Good Will Hunting. "
            "Known for the Bourne series, The Martian, Saving Private Ryan, and The Departed."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/aCvBXTAR9B1qRjIRzMBYhhbm1fR.jpg",
    },
    {
        "name": "Samuel L. Jackson",
        "birth_date": "1948-12-21",
        "bio": (
            "American actor who is among the highest-grossing actors of all time. "
            "Known for Pulp Fiction, Django Unchained, the MCU's Nick Fury, and Jackie Brown."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/AiAYAqwpM5xmiFrAIeQvUXDCVvo.jpg",
    },
    {
        "name": "Kate Winslet",
        "birth_date": "1975-10-05",
        "bio": (
            "British actress and one of the most decorated performers of her generation. "
            "Academy Award winner for The Reader; iconic roles in Titanic, Eternal Sunshine, and Steve Jobs."
        ),
        "photo_url": "https://image.tmdb.org/t/p/w500/9xDnfZrWhM67wJlQJEsOOjQzDUQ.jpg",
    },
]

# ---------------------------------------------------------------------------
# 10 Movies — every FK (director) and M2M (genres, actors) is explicit.
#
# Genre and actor names must match the entries above exactly.
# ---------------------------------------------------------------------------
MOVIES: list[dict] = [
    {
        "title": "Inception",
        "release_year": 2010,
        "synopsis": (
            "Dom Cobb is a skilled thief who steals secrets from targets by entering their dreams. "
            "Given a chance to have his criminal record erased, he must plant an idea rather than steal one — "
            "a task deemed impossible. He assembles a team for the ultimate heist."
        ),
        "poster_url": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
        "director": "Christopher Nolan",
        "genres": ["Action", "Science Fiction", "Thriller"],
        "actors": ["Leonardo DiCaprio", "Cillian Murphy"],
    },
    {
        "title": "The Dark Knight",
        "release_year": 2008,
        "synopsis": (
            "Batman, Lieutenant Gordon, and District Attorney Harvey Dent form an alliance to dismantle organised "
            "crime in Gotham. But the emergence of the Joker — a sadistic agent of chaos — tests them all "
            "in ways they never anticipated."
        ),
        "poster_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "director": "Christopher Nolan",
        "genres": ["Action", "Crime", "Drama"],
        "actors": ["Christian Bale"],
    },
    {
        "title": "Pulp Fiction",
        "release_year": 1994,
        "synopsis": (
            "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits "
            "intertwine in four tales of violence and redemption in Los Angeles."
        ),
        "poster_url": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
        "director": "Quentin Tarantino",
        "genres": ["Crime", "Drama"],
        "actors": ["Samuel L. Jackson"],
    },
    {
        "title": "The Departed",
        "release_year": 2006,
        "synopsis": (
            "An undercover cop and a mole in the police simultaneously try to identify each other "
            "while working within a Massachusetts organised-crime gang. "
            "Scorsese's tense cat-and-mouse thriller won four Academy Awards including Best Picture."
        ),
        "poster_url": "https://image.tmdb.org/t/p/w500/nT97ifVT2J1yMQmeq20Qblg61T.jpg",
        "director": "Martin Scorsese",
        "genres": ["Crime", "Drama", "Thriller"],
        "actors": ["Leonardo DiCaprio", "Matt Damon"],
    },
    {
        "title": "Saving Private Ryan",
        "release_year": 1998,
        "synopsis": (
            "Following the D-Day invasion of Normandy, Captain Miller leads a squad of soldiers "
            "deep behind enemy lines on a mission to find and bring home Private James Ryan, "
            "whose three brothers have all been killed in combat."
        ),
        "poster_url": "https://image.tmdb.org/t/p/w500/uqx37cS8cpHg8U35f9U5IBlrCV3.jpg",
        "director": "Steven Spielberg",
        "genres": ["Drama", "Action"],
        "actors": ["Tom Hanks", "Matt Damon"],
    },
    {
        "title": "Barbie",
        "release_year": 2023,
        "synopsis": (
            "Barbie and Ken leave the utopian Barbieland for the real world after Barbie begins experiencing "
            "an existential crisis. A sharp satire on gender, identity, and capitalism wrapped in a candy-pink "
            "spectacle that became one of the highest-grossing films of all time."
        ),
        "poster_url": "https://image.tmdb.org/t/p/w500/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg",
        "director": "Greta Gerwig",
        "genres": ["Comedy", "Adventure"],
        "actors": ["Margot Robbie", "Ryan Gosling"],
    },
    {
        "title": "Dune",
        "release_year": 2021,
        "synopsis": (
            "Paul Atreides, a brilliant and gifted young man born into a great destiny, "
            "travels to the most dangerous planet in the universe to ensure the future of his family "
            "and his people. Epic adaptation of Frank Herbert's seminal science-fiction novel."
        ),
        "poster_url": "https://image.tmdb.org/t/p/w500/pc15b0pi8o1oUv9vNhakwMQ9TxA.jpg",
        "director": "Denis Villeneuve",
        "genres": ["Science Fiction", "Adventure", "Drama"],
        "actors": ["Timothée Chalamet"],
    },
    {
        "title": "Blade Runner 2049",
        "release_year": 2017,
        "synopsis": (
            "Officer K, a new blade runner for the LAPD, unearths a long-buried secret that has "
            "the potential to plunge what remains of society into chaos. His discovery leads him "
            "on a quest to find Rick Deckard, a former blade runner who has been missing for 30 years."
        ),
        "poster_url": "https://image.tmdb.org/t/p/w500/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",
        "director": "Denis Villeneuve",
        "genres": ["Science Fiction", "Drama", "Thriller"],
        "actors": ["Ryan Gosling"],
    },
    {
        "title": "Titanic",
        "release_year": 1997,
        "synopsis": (
            "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the ill-fated "
            "RMS Titanic. James Cameron's epic romance and disaster film became the first to gross over "
            "$1 billion and won 11 Academy Awards including Best Picture."
        ),
        "poster_url": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
        "director": "James Cameron",
        "genres": ["Drama", "Romance"],
        "actors": ["Leonardo DiCaprio", "Kate Winslet"],
    },
    {
        "title": "The Martian",
        "release_year": 2015,
        "synopsis": (
            "Astronaut Mark Watney is stranded on Mars after his crew believes he is dead and evacuates "
            "the planet. With only meagre supplies, he must draw on his ingenuity, wit, and spirit "
            "to survive — and signal to Earth that he is alive."
        ),
        "poster_url": "https://image.tmdb.org/t/p/w500/3ndAx3weG6KDkJIRMCi5vXX6Dyb.jpg",
        "director": "Ridley Scott",
        "genres": ["Science Fiction", "Adventure", "Drama"],
        "actors": ["Matt Damon"],
    },
]

# ---------------------------------------------------------------------------
# 10 Reviews — one per movie, ordered to match MOVIES list above.
# (movie title, author, rating /10, comment)
# ---------------------------------------------------------------------------
REVIEWS: list[tuple[str, str, int, str]] = [
    (
        "Inception",
        "Charlie Walker", 9,
        "A mind-bending masterpiece that rewards every repeat viewing. "
        "Nolan's best alongside The Dark Knight.",
    ),
    (
        "The Dark Knight",
        "Sarah Mitchell", 10,
        "Heath Ledger's Joker is the single greatest villain performance in cinema history. "
        "A perfect film.",
    ),
    (
        "Pulp Fiction",
        "James Rivera", 9,
        "Tarantino at his absolute finest — the dialogue, the structure, the style. "
        "Changed cinema forever.",
    ),
    (
        "The Departed",
        "Nina Patel", 9,
        "Scorsese's tightest thriller. Every scene crackles with tension, "
        "and the ensemble is flawless.",
    ),
    (
        "Saving Private Ryan",
        "Robert Hayes", 10,
        "The D-Day opening sequence is the most harrowing 27 minutes ever committed to film. "
        "Spielberg at his peak.",
    ),
    (
        "Barbie",
        "Emma Thompson", 8,
        "Surprisingly deep and wickedly funny. Gerwig threads the needle between spectacle "
        "and genuine emotional resonance.",
    ),
    (
        "Dune",
        "Oliver Chen", 9,
        "Villeneuve's world-building is breathtaking. Chalamet shoulders the epic with quiet intensity — "
        "a visual and emotional triumph.",
    ),
    (
        "Blade Runner 2049",
        "Yasmin Torres", 9,
        "Visually the most stunning film of the decade. Roger Deakins deserved every award he received. "
        "A worthy successor.",
    ),
    (
        "Titanic",
        "Laura Kim", 8,
        "A timeless romance wrapped in spectacular disaster filmmaking. "
        "The practical and visual effects still hold up 25 years later.",
    ),
    (
        "The Martian",
        "Daniel Ford", 8,
        "Smart, funny, and genuinely tense. Damon's performance is charming throughout, "
        "and the science actually matters.",
    ),
]


class Command(BaseCommand):
    """Seed the database with exactly 10 rows per entity table."""

    help = "Load 10 genres, 10 directors, 10 actors, 10 movies, and 10 reviews with proper FK/M2M relations."

    def handle(self, *args, **options) -> None:
        # --- Genres (10) ---
        self.stdout.write("Seeding 10 genres...")
        genre_map: dict[str, Genre] = {}
        for name in GENRES:
            obj, created = Genre.objects.update_or_create(
                name=name,
                defaults={"slug": slugify(name)},
            )
            genre_map[name] = obj
            if created:
                self.stdout.write(f"  + Genre: {name}")

        # --- Directors (10) ---
        self.stdout.write("Seeding 10 directors...")
        director_map: dict[str, Director] = {}
        for d in DIRECTORS:
            obj, created = Director.objects.update_or_create(
                name=d["name"],
                defaults={
                    "slug": slugify(d["name"]),
                    "birth_date": d["birth_date"],
                    "bio": d["bio"],
                    "photo_url": d["photo_url"],
                },
            )
            director_map[d["name"]] = obj
            if created:
                self.stdout.write(f"  + Director: {d['name']}")

        # --- Actors (10) ---
        self.stdout.write("Seeding 10 actors...")
        actor_map: dict[str, Actor] = {}
        for a in ACTORS:
            obj, created = Actor.objects.update_or_create(
                name=a["name"],
                defaults={
                    "slug": slugify(a["name"]),
                    "birth_date": a["birth_date"],
                    "bio": a["bio"],
                    "photo_url": a["photo_url"],
                },
            )
            actor_map[a["name"]] = obj
            if created:
                self.stdout.write(f"  + Actor: {a['name']}")

        # --- Movies (10) with FK + M2M ---
        self.stdout.write("Seeding 10 movies...")
        movie_map: dict[str, Movie] = {}
        for m in MOVIES:
            director = director_map[m["director"]]
            movie, created = Movie.objects.update_or_create(
                title=m["title"],
                release_year=m["release_year"],
                defaults={
                    "slug": slugify(f"{m['title']}-{m['release_year']}"),
                    "synopsis": m["synopsis"],
                    "poster_url": m["poster_url"],
                    "director": director,
                },
            )
            # Re-set M2M on every run (idempotent)
            movie.genres.set([genre_map[g] for g in m["genres"]])   # M2M → Genre
            movie.actors.set([actor_map[a] for a in m["actors"]])   # M2M → Actor
            movie_map[m["title"]] = movie
            if created:
                genre_names = ", ".join(m["genres"])
                actor_names = ", ".join(m["actors"]) or "—"
                self.stdout.write(
                    f"  + Movie: {m['title']} ({m['release_year']}) | "
                    f"Dir: {m['director']} | Genres: {genre_names} | Actors: {actor_names}"
                )

        # --- Reviews (10 — one per movie) ---
        self.stdout.write("Seeding 10 reviews...")
        for movie_title, author, rating, comment in REVIEWS:
            movie = movie_map[movie_title]
            _, created = Review.objects.get_or_create(
                movie=movie,
                author_name=author,
                defaults={"rating": rating, "comment": comment},
            )
            if created:
                self.stdout.write(f"  + Review: {author} → {movie_title} ({rating}/10)")

        # --- Summary ---
        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeed complete: "
                f"{Genre.objects.count()} genres, "
                f"{Director.objects.count()} directors, "
                f"{Actor.objects.count()} actors, "
                f"{Movie.objects.count()} movies, "
                f"{Review.objects.count()} reviews."
            )
        )
