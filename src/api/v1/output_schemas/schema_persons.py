from uuid import UUID
from pydantic import BaseModel


class PersonListOut(BaseModel):
    id: UUID
    full_name: str
