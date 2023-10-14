from typing import List, Optional, Any

from src.core.config import settings
from src.db.elastic_extractor import ElasticExtractor
from src.models.mapping import MODEL_MAPPING


class BaseService:
    def __init__(self, index, es_extractor: ElasticExtractor):
        self.es_extractor = es_extractor
        self.index = index

    async def get_by_id(self, object_id: str) -> Optional[Any]:
        """Get object by id in specified index

        Args:
            object_id (str): Object's ID to find
        Returns:
            Optional[Any]: Found object or None
        """
        obj_found = await self.es_extractor.get_object(index=self.index, object_id=object_id)
        if not obj_found:
            return None
        return MODEL_MAPPING.get(self.index)(**obj_found)

    async def get_all(
        self,
        sort: Optional[str] = None,
        page_number: int = 1,
        size: int = settings.PAGE_SIZE,
        scroll: str = settings.SCROLL_TIME,
        query: Optional[dict] = None,
    ) -> tuple[Optional[List[Any]], int]:
        """Get objects in specified index

        Args:
            sort (Optional[str]): Object's ID to find
            page_number (int): Page number,
            size (int): Page size - quantity of objects on one page,
            scroll (str): scroll time of elastic,
            query(Optional[str]): query in dsl format for elastic,
        Returns:
            tuple[Optional[List[Any], int]: tuple of found objects with total page quantity or None and 0
        """
        if query is None:
            query = {"match_all": {}}

        objs_found, page_qty = await self.es_extractor.get_objects(
            index=self.index,
            query=query,
            page_number=page_number,
            size=size,
            scroll=scroll,
            sort=sort,
        )
        if not objs_found:
            return None, 0
        return [MODEL_MAPPING.get(self.index)(**obj_found) for obj_found in objs_found], page_qty

    async def search_objects(
        self,
        query: dict,
        sort: Optional[str] = None,
        page_number: int = 1,
        size: int = settings.PAGE_SIZE,
        scroll: str = settings.SCROLL_TIME,
    ) -> tuple[Optional[List[Any]], int]:
        """Search objects in specified index and specified query

        Args:
            query(dict): query in dsl format for elastic,
            sort (Optional[str]): Object's ID to find
            page_number (int): Page number,
            size (int): Page size - quantity of objects on one page,
            scroll (str): scroll time of elastic,
        Returns:
            tuple[Optional[List[Any], int]: tuple of found objects with total page quantity or None and 0
        """
        objs_found, page_qty = await self.es_extractor.get_objects(
            index=self.index,
            query=query,
            page_number=page_number,
            size=size,
            scroll=scroll,
            sort=sort,
        )
        if not objs_found:
            return None, 0
        return [MODEL_MAPPING.get(self.index)(**obj_found) for obj_found in objs_found], page_qty
