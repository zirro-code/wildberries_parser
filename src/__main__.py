import asyncio

from loguru import logger

import src.app.file_manager
import src.app.wildberries_api


async def collect_search_query(
    *,
    wb_public_client: src.app.wildberries_api.WildberriesPublicAPIClient,
    file_manager: src.app.file_manager.FileManager,
    search_query: str,
):
    results = list(await wb_public_client.get_search_listing(search_query=search_query))
    file_manager.bulk_dump(search_query, results)
    logger.info(f"Finished fetching {search_query}")


async def main():
    wb_public_client = src.app.wildberries_api.WildberriesPublicAPIClient()
    file_manager = src.app.file_manager.FileManager()
    await wb_public_client.http_client.run()

    await asyncio.gather(
        *[
            collect_search_query(
                file_manager=file_manager,
                wb_public_client=wb_public_client,
                search_query=search_query,
            )
            for search_query in [
                "Платье",
                "Юбка",
                "Футболка",
                "Худи",
                "Диски воссен с золотым отливом",
            ]
        ]
    )

    await wb_public_client.http_client.stop()


if __name__ == "__main__":
    asyncio.run(main())
