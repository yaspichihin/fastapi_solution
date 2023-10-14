from uuid import UUID

from src.models.base_orjson import BaseOrjsonModel


class Genre(BaseOrjsonModel):
    id: UUID
    name: str
