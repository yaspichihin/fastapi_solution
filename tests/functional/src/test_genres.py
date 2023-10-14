import pytest

from tests.functional.settings import config
from tests.functional.testdata.es_data import genres_data


@pytest.mark.asyncio
async def test_get_genres_default_size(make_get_request):
    response = await make_get_request("/genres/")
    assert response.status == 200
    assert len(response.body) == config.page_size


@pytest.mark.asyncio
async def test_get_genres_custom_size(make_get_request):
    response = await make_get_request("/genres/", params={"page[size]": 40})
    assert response.status == 200
    assert len(response.body) == 40


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "genre_id, status", [(genres_data[0]["id"], 200), ("Aca4f2ac-2398-42b9-a142-5567a8a0b366", 404)]
)
async def test_get_genre_by_id(make_get_request, genre_id, status):
    response = await make_get_request(f"/genres/{genre_id}")
    assert response.status == status
