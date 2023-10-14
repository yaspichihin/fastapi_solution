from typing import Optional, List
from elasticsearch import AsyncElasticsearch, NotFoundError


class ElasticExtractor:
    def __init__(self, elastic_url: str):
        self.es = AsyncElasticsearch(hosts=elastic_url)

    async def close(self) -> None:
        """Close connections to Elastic"""
        await self.es.close()

    async def get_object(self, index: str, object_id: str) -> Optional[dict]:
        """Get object by id in specified index

        Args:
            index (str): Index name.
            object_id (str): Object's ID to find
        Returns:
            Optional[dict]: Found object or None
        """
        try:
            resp = await self.es.get(index=index, id=object_id)
        except NotFoundError:
            return None
        else:
            return resp.get("_source")

    async def get_objects(
        self,
        index: str,
        query: dict,
        sort: Optional[str],
        page_number: int,
        size: int,
        scroll: str,
    ) -> tuple[List[dict], int]:
        """Get list of object by query in specified index with additional params

        Args:
            index (str): Index name.
            query (dict): Query in DSL syntax for search in Elastic
            sort (Optional[str]): Field for sorting and direction
            page_number (int): Page number in search results
            size (int): Quantity objects on pages
            scroll (str): Scroll params in Elastic
        Returns:
            tuple[List[dict], int]: Tuple of searched objects and pages quantities
        """
        try:
            search_resp = await self.es.search(
                index=index,
                query=query,
                size=size,
                scroll=scroll,
                sort=sort,
            )
        except NotFoundError:
            return list(), 0
        else:
            qty_pages = self.count_pages(
                size,
                search_resp.get("hits").get("total").get("value"),
            )
            if page_number == 1:
                return [hit.get("_source") for hit in search_resp.get("hits").get("hits")], qty_pages
            if page_number > qty_pages:
                return list(), qty_pages
            return (
                await self._get_objects_by_page_number(page_number, search_resp.get("_scroll_id"), scroll=scroll),
                qty_pages,
            )

    async def _get_objects_by_page_number(self, page_number: int, scroll_id: str, scroll: str):
        """Get list of object in scroll search by scroll_id

        Args:
            page_number (int): Page number in search results
            scroll_id (str):
            scroll (str): Scroll params in Elastic
        Returns:
            List[dict]: List of searched objects
        """
        scroll_resp = None
        for _ in range(1, page_number):
            scroll_resp = await self.es.scroll(scroll_id=scroll_id, scroll=scroll)
            scroll_id = scroll_resp.get("_scroll_id")
        return [hit.get("_source") for hit in scroll_resp.get("hits").get("hits")]

    @staticmethod
    def count_pages(page_size: int, obj_qty: int):
        return round(obj_qty / page_size)


es_extractor: Optional[ElasticExtractor] = None


async def get_elastic_extractor() -> ElasticExtractor:
    return es_extractor
