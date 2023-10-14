import uuid
import random

genres_name = ("Action", "Sci-Fi", "Comedy", "Drama", "Fantasy")
movies_name = ("The Lord of Rings", "Matrix", "Iron Man", "Sherlok", "Star Wars")
persons_name = ("Ann", "Bob", "John", "Martin", "Alex", "Mary", "Julia")
roles_name = ("Director", "Actor", "Writer")


def generate_imdb_rating() -> float:
    return float("{:.1f}".format(random.random() * 10))


def create_genres_data() -> list[dict]:
    data = list()
    for genre_name in genres_name:
        for _ in range(15):
            data.append({"id": str(uuid.uuid4()), "name": genre_name})
    return data


genres_data = create_genres_data()


def create_films_data() -> list[dict]:
    data = list()
    for movie_name in movies_name:
        for _ in range(15):
            actors = [
                {"id": str(uuid.uuid4()), "name": persons_name[random.randint(0, len(persons_name) - 1)]}
                for _ in range(2)
            ]
            writers = [
                {"id": str(uuid.uuid4()), "name": persons_name[random.randint(0, len(persons_name) - 1)]}
                for _ in range(2)
            ]
            data.append(
                {
                    "id": str(uuid.uuid4()),
                    "imdb_rating": generate_imdb_rating(),
                    "genre": [genres_name[random.randint(0, len(genres_name) - 1)] for _ in range(2)],
                    "title": movie_name,
                    "description": "Some description",
                    "director": [persons_name[random.randint(0, len(persons_name) - 1)]],
                    "actors_names": [actor["name"] for actor in actors],
                    "writers_names": [writer["name"] for writer in writers],
                    "actors": actors,
                    "writers": writers,
                }
            )
    return data


films_data = create_films_data()


def create_persons_data() -> list[dict]:
    data = list()
    for person_name in persons_name:
        for _ in range(15):
            data.append(
                {
                    "id": str(uuid.uuid4()),
                    "full_name": person_name,
                    "films": [
                        {
                            "id": films_data[random.randint(0, len(films_data) - 1)]["id"],
                            "roles": [roles_name[random.randint(0, len(roles_name) - 1)] for _ in range(2)],
                        }
                    ],
                }
            )
    return data


persons_data = create_persons_data()
