from uuid import UUID
from pydantic import BaseModel


class GenresListOut(BaseModel):
    id: UUID
    name: str


class GenreOut(BaseModel):
    id: UUID
    name: str
