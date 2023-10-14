from typing import List
import pytest
from elasticsearch import AsyncElasticsearch, helpers

from tests.functional.settings import config
from tests.functional.testdata.es_mappings import index_mappings, index_settings
from tests.functional.testdata.es_data import genres_data, films_data, persons_data


@pytest.fixture(scope="session", autouse=True)
async def es_client():
    client = AsyncElasticsearch(hosts=config.es_host)
    yield client
    await client.close()


async def es_write_data(es_client, index, data: List[dict]):
    if not await es_client.indices.exists(index=index):
        index_dict = dict(index_mappings[index], **index_settings)
        await es_client.indices.create(index=index, body=index_dict)
    bulk_query = [{"_index": index, "_id": item[config.es_id_field], **item} for item in data]
    await helpers.async_bulk(es_client, actions=bulk_query)


@pytest.fixture(scope="session", autouse=True)
async def es_write_genres(es_client):
    """
    Write genres data to ElasticSearch
    """
    await es_write_data(es_client, "genres", genres_data)



@pytest.fixture(scope="session", autouse=True)
async def es_write_films(es_client):
    """
    Write genres data to ElasticSearch
    """
    await es_write_data(es_client, "movies", films_data)


@pytest.fixture(scope="session", autouse=True)
async def es_write_persons(es_client):
    """
    Write genres data to ElasticSearch
    """
    await asyncio.sleep(60)
    await es_write_data(es_client, "persons", persons_data)
