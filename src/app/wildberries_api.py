import asyncio
import json
from typing import Any, Literal
from urllib.parse import urlencode

from loguru import logger

from src.app.http_client import HttpClient


class WildberriesPublicAPIClient:
    BASE_URL = "https://search.wb.ru"

    def __init__(self) -> None:
        self.http_client = HttpClient()

    async def _request(
        self, *, method: Literal["GET"], route: str, query: dict[str, Any]
    ) -> Any:
        url_args = urlencode(query)
        url = f"{self.BASE_URL}/{route}?{url_args}"

        async with self.http_client.session.request(method, url) as request:
            logger.debug(f"Sent request to {url}")
            response = json.loads(await request.text())

        return response

    async def get_search_page(self, *, search_query: str, page: int = 1):
        query: dict[str, Any] = {
            "resultset": "catalog",
            "sort": "popular",
            "appType": "1",
            "curr": "rub",
            "dest": "-1257786",  # TODO: implement location selection. https://user-geo-data.wildberries.ru/get-geo-info?currency=RUB&latitude=41.2345&longitude=-8.6182&locale=ru&address=%D0%9C%D0%B0%D0%B9%D1%8F&dt=0&currentLocale=ru&b2bMode=false
            "lang": "ru",
            "page": page,
            "query": search_query,
        }

        return await self._request(
            method="GET", route="exactmatch/ru/common/v13/search", query=query
        )

    async def get_search_listing(self, search_query: str, pages: int = 30):
        results = await asyncio.gather(
            *[
                self.get_search_page(search_query=search_query, page=page)
                for page in range(1, pages + 1)
            ],
        )

        return (result.get("data", {}).get("products", [{}]) for result in results)
