import asyncio

import pytest

from tests.functional.settings import config
from tests.functional.testdata.es_data import persons_data


@pytest.mark.asyncio
async def test_get_persons_default_size(make_get_request):
    response = await make_get_request("/persons/")
    assert response.status == 200
    assert len(response.body) == config.page_size


@pytest.mark.asyncio
async def test_get_persons_custom_size(make_get_request):
    response = await make_get_request("/persons/", params={"page[size]": 40})
    assert response.status == 200
    assert len(response.body) == 40


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "person_id, status",
    [
        (persons_data[0]["id"], 200),
        ("Aca4f2ac-2398-42b9-a142-5567a8a0b366", 404)
    ]
)
async def test_get_person_by_id(make_get_request, person_id, status):
    response = await make_get_request(f"/persons/{person_id}")
    assert response.status == status


@pytest.mark.asyncio
async def test_get_persons_default_size_2(make_get_request):
    response = await make_get_request("/persons/")
    assert response.status == 200
    assert len(response.body) == config.page_size
