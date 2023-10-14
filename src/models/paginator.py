from fastapi import Query
from pydantic import BaseModel, Field

from src.core.config import settings


class Paginator(BaseModel):
    page_size: int = Field(default=settings.PAGE_SIZE)
    page_number: int = Field(default=1)


def get_paginator_params(
    page_size: int = Query(settings.PAGE_SIZE, alias="page[size]", ge=1),
    page_number: int = Query(1, alias="page[number]", ge=1),
):
    return Paginator(
        page_size=page_size,
        page_number=page_number,
    )
