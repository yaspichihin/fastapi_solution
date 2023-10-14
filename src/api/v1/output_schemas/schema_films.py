from uuid import UUID
from pydantic import BaseModel


class FilmListOut(BaseModel):
    id: UUID
    title: str
    imdb_rating: float


