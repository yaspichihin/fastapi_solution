import aiohttp
import pytest
from typing import Any, Optional
from pydantic.dataclasses import dataclass

from tests.functional.settings import config


@dataclass
class HTTPResponse:
    body: Any
    status: int


@pytest.fixture(scope="session")
async def session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = config.service_url + "/api/v1" + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(body=await response.json(), status=response.status)

    return inner
