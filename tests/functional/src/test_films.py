import pytest

from tests.functional.settings import config
from tests.functional.testdata.es_data import films_data


@pytest.mark.asyncio
async def test_get_films_default_size(make_get_request):
    response = await make_get_request("/films/")
    assert response.status == 200
    assert len(response.body) == config.page_size


@pytest.mark.asyncio
async def test_get_films_custom_size(make_get_request):
    response = await make_get_request("/films/", params={"page[size]": 40})
    assert response.status == 200
    assert len(response.body) == 40


@pytest.mark.asyncio
@pytest.mark.parametrize("film_id, status", [(films_data[0]["id"], 200), ("Aca4f2ac-2398-42b9-a142-5567a8a0b366", 404)])
async def test_get_genre_by_id(make_get_request, film_id, status):
    response = await make_get_request(f"/films/{film_id}")
    assert response.status == status
