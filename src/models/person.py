from typing import List
from uuid import UUID

from .base_orjson import BaseOrjsonModel


class PersonFilms(BaseOrjsonModel):
    id: UUID
    roles: List[str]


class Person(BaseOrjsonModel):
    id: UUID
    full_name: str
    films: List[PersonFilms]
