from typing import Optional
from uuid import UUID

from src.models.base_orjson import BaseOrjsonModel


class Film(BaseOrjsonModel):
    id: UUID
    imdb_rating: float
    genre: list
    title: str
    description: Optional[str]
    director: list
    actors_names: list
    writers_names: list
    actors: list
    writers: list
