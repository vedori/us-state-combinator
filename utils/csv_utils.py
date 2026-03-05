import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Final

from us_states import US_STATES


@dataclass(frozen=True, order=True)
class CSVEntry:
    county: str
    state: str


@dataclass(frozen=True, order=True)
class MergedEntry(CSVEntry):
    population: int
    gdp: int


@dataclass(frozen=True, order=True)
class PopulationEntry(CSVEntry):
    population: int


@dataclass(frozen=True, order=True)
class GDPEntry(CSVEntry):
    gdp: int


@dataclass(frozen=True, order=True)
class GDPGroupedEntry(CSVEntry):
    gdp_group: str


GDP_COMBINATION_SEPERATOR: Final = " + "

# All relevant paths
data_path: Path = Path.cwd() / "data"
raw_data_path: Path = data_path / "raw"
processed_data_path: Path = data_path / "processed"
final_data_path: Path = data_path / "final"
population_csv_file: Path = raw_data_path / "2020-pop.csv"
gdp_csv_file: Path = raw_data_path / "2020-gdp.csv"


# A dictionary of gdp group names to their respective gdp
gdp_group_table: dict[str, int] = dict()


class CSVReader:
    """
    This class parses gdp and population csv data from the raw data directory
    into valid entry objects.
    It also contains a class-level dictionary that serves as a lookup table for
    gdp grouped data.

    Methods:
        `population_entry_list()`: returns a list of the parsed population entries
        `gdp_entry_list()`: returns a list of the parsed gdp entries

    """

    def __init__(self, file_path: Path):
        self.file_path: Path = file_path

    def _expand_grouped_counties(
        self,
        name: str,
        state: str,
        gdp: int,
        gdp_entry_list: list[CSVEntry],
    ) -> bool:
        """
        GDP data is irregular because some counties / cities are grouped as a single economic unit.
        An example entry: `Maui County + Kalawao County,Hawaii,8577089`
        Expands gdp grouped entries into individual entries and
        updates the gdp group table
        """
        if GDP_COMBINATION_SEPERATOR not in name:
            return False

        grouped_counties = name.split(GDP_COMBINATION_SEPERATOR)
        for individual_county in grouped_counties:
            entry = GDPGroupedEntry(
                county=individual_county,
                state=state,
                gdp_group=name,
            )
            gdp_entry_list.append(entry)

            # Updates the gdp group table
            gdp_group_table.update({name: gdp})
        return True

    def population_entry_list(self):
        fieldnames = ["county", "state", "population"]
        population_entry_list: list[PopulationEntry] = []
        with open(
            file=self.file_path, mode="r", newline="", encoding="utf-8-sig"
        ) as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=fieldnames)
            for row in reader:
                entry = PopulationEntry(
                    county=row["county"],
                    state=row["state"],
                    population=int(row["population"], 10),
                )
                population_entry_list.append(entry)
        return population_entry_list

    def gdp_entry_list(self):
        fieldnames = ["county", "state", "gdp"]
        gdp_entry_list: list[CSVEntry] = []
        with open(
            file=self.file_path, mode="r", newline="", encoding="utf-8-sig"
        ) as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=fieldnames)
            for row in reader:
                name = row["county"]
                state = row["state"]
                gdp = int(row["gdp"], 10)

                # Expands gdp grouped entries into individual entries
                # and updates the gdp group table
                if not self._expand_grouped_counties(
                    name=name,
                    state=state,
                    gdp=gdp,
                    gdp_entry_list=gdp_entry_list,
                ):
                    entry = GDPEntry(county=name, state=state, gdp=gdp)
                    gdp_entry_list.append(entry)

        return gdp_entry_list


# Aggregates multiple csv data and writes it to one state config file
class StateConfigCreator:
    """
    This class creates an initial configuration for the state data
    given the gdp and csv data from `CSVReader`

    Methods:
        `write_config_to_file`: creates an initial config
    """

    @classmethod
    def _merge_gdp_population_csv_data(cls):
        """
        Merges gdp and population county csv data
        """
        merged_entry_list: list[dict[str, str | int]] = []

        population_list = CSVReader(population_csv_file).population_entry_list()

        gdp_list = CSVReader(gdp_csv_file).gdp_entry_list()

        # Log lengths of gdp_list and population_list
        print(
            f"{'📋':<1} pop_list length: {len(population_list)}\n   gdp_list length: {len(gdp_list)}"
        )

        for p, g in zip(population_list, gdp_list):
            # Log mismatches
            if p.county != g.county and p.state != g.state:
                print(f"❌ {str(p):<100}{str(g):>4}")

            # Entry starts with the population entry
            merged_entry = asdict(p)

            # Adds the gdp group to the merged entry if the gdp entry has it
            if isinstance(g, GDPGroupedEntry):
                merged_entry.update(asdict(g))

            # Otherwise add the gdp entry to the merged entry dict
            if isinstance(g, GDPEntry):
                merged_entry.update(asdict(g))
            merged_entry_list.append(merged_entry)

        return merged_entry_list

    @classmethod
    def write_config_to_file(cls):
        """
        This function serializes the complete county data to json.
        1) Writes the json data to `county_data.json` in the intermediate data dir.
        2) Restructures the county data to be organized by state rather than being
           a flat list of county data.
        3) Writes the json data to `state_data` in the final data dir.
        4) Gets the gdp group data from the module, then writes the json data
           to `gdp_groups.json` in the final data dir.
        """
        county_data = cls._merge_gdp_population_csv_data()
        county_json = json.dumps(county_data, indent=1)
        gdp_groups_json = json.dumps(gdp_group_table)

        # Writes the county data to an intermediate file before processing
        with open(
            processed_data_path / "county_data.json",
            mode="w",
            encoding="utf8",
        ) as config_file:
            _ = config_file.write(county_json)

        # Reorganizes the dictionary to be grouped by states and
        # removes the state field from individual counties
        # This will reflect the way it will be stored in the final configuration
        # It will then be written to a file
        states = list(US_STATES.keys())
        all_states: dict[str, dict[str, str | list[dict[str, str | int]]]] = {
            s: {"abbreviation": US_STATES.get(s, ""), "counties": []} for s in states
        }
        for c in county_data:
            state = c.pop("state")
            if not isinstance(state, str):
                continue
            state_counties = all_states.get(state)
            if state_counties is None:
                continue
            county_list = state_counties.get("counties", [])
            if not isinstance(county_list, str):
                county_list.append(c)

        state_json = json.dumps(all_states, indent=1)

        # Writes state data
        with open(
            final_data_path / "state_data.json",
            mode="w",
            encoding="utf8",
        ) as config_file:
            _ = config_file.write(state_json)

        # Seperate file in final data path for GDP groups
        with open(
            final_data_path / "gdp_groups.json",
            mode="w",
            encoding="utf8",
        ) as config_file:
            _ = config_file.write(gdp_groups_json)
