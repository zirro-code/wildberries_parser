import csv
from pathlib import Path
from typing import Literal

import arrow


class FileManager:
    def __init__(self, *, output_folder: str = "./output"):
        today = arrow.utcnow()
        self.output_folder = f"{output_folder}/{today.format('YYYY/MM/DD')}"

        if not Path(self.output_folder).exists():
            Path(self.output_folder).mkdir(parents=True)

    def bulk_dump(
        self,
        filename: str,
        data: list[list[dict[str, str]]],
        file_open_mode: Literal["w", "a"] = "w",
    ):
        with Path(f"{self.output_folder}/{filename}.csv").open(file_open_mode) as file:
            writer = csv.writer(file)
            # TODO: either add row names, or dump to json
            for element in data:
                writer.writerows(row.values() for row in element)
