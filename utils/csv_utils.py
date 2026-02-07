import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CSVReader:
    """
    This class handles a single path to a csv file and returns the processed data

    Attributes:
        file_path (Path): Path to the csv file

    Methods:
        as_list(): returns a list of the parsed csv entries
    """

    file_path: Path

    def as_list(self):
        result: list[list[str]] = []
        with open(file=self.file_path, mode="r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
            for row in csv_reader:
                result.append(row)
        return result

    def as_dict_list(self, fieldnames: list[str]):
        result: list[dict[str, str]] = []
        with open(file=self.file_path, mode="r", newline="") as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=fieldnames)
            for row in reader:
                result.append(row)
        return result
