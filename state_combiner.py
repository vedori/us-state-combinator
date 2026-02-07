import itertools
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

from us_states import US_STATES
from utils import csv_utils

GDP_COMBINATION_SEPERATOR: Final = " + "


# Immutable
# Represents a county
# It should have a name, population, and gdp
@dataclass(frozen=True, order=True)
class County:
    name: str
    population: int
    gdp: int


# Immutable
# Represents a regular state
# It should have a name, abbreviation, gdp, and list of counties
@dataclass(frozen=True, order=True)
class State:
    name: str
    gdp: int
    abbreviation: str = field(compare=False, repr=False)
    counties: list[County] = field(
        default_factory=list, compare=False, hash=False, repr=False
    )


# The main mutable component of this program
# A container for one or more counties
@dataclass(order=True)
class CustomState:
    counties: list[County] = field(default_factory=list, compare=False, hash=False)
    pass


# Aggregates multiple csv data and writes it to one state config file
class StateConfigCreator:
    data_path: Path = Path.cwd() / "data"
    raw_data_path: Path = data_path / "raw"
    processed_data_path = data_path / "processed"

    population_csv_file: Path = raw_data_path / "2020-pop.csv"
    gdp_csv_file: Path = raw_data_path / "2020-gdp.csv"

    @classmethod
    def get_county_population_from_csv(cls):
        return csv_utils.CSVReader(cls.population_csv_file).as_dict_list(
            ["county", "state", "population"]
        )

    @classmethod
    def get_county_gdp_from_csv(cls):
        return csv_utils.CSVReader(cls.gdp_csv_file).as_dict_list(
            ["county", "state", "gdp"]
        )

    # Aggregates county data from seperate csv files
    @classmethod
    def merge_gdp_population_csv_data(cls):
        """
        Merges gdp and population county csv data
        GDP data is irregular because some counties / cities are grouped as a single economic unit.
        An example entry: `Maui County + Kalawao County,Hawaii,8577089`
        This function must handle these exceptions
        """
        gdp_list = cls.get_county_gdp_from_csv()
        population_list = cls.get_county_population_from_csv()

        # Some entries in `gdp_list` are combination areas where a single entry has a county name
        # that follows the structure: 'county1 + county2 + ...'
        # This expands a single gdp combo entry into multiple entries
        # where each entry is a tuple stored in a set {(county1, state), (county2, state), ...}
        def generate_expanded_entries(combo_area: dict[str, str]):
            if GDP_COMBINATION_SEPERATOR in combo_area.get("county", ""):
                grouped_counties = combo_area.get("county", "").split(
                    GDP_COMBINATION_SEPERATOR
                )
                for individual_county in grouped_counties:
                    entry = {
                        "county": individual_county,
                        "state": combo_area.get("state", ""),
                        "gdp_area": combo_area.get("county", ""),
                    }
                    yield entry

        gdp_combination_areas = list(map(generate_expanded_entries, gdp_list))
        gdp_combination_areas = [
            individual_entry
            for gdp_combination_area in gdp_combination_areas
            for individual_entry in gdp_combination_area
        ]
        print(gdp_combination_areas)
        # Builds a JSON representation of the static state config
        # Iterates through the population data set since it has every county
        # Adds a relevant field that indicates counties grouped by gdp
        merged_entry_list: list[dict[str, str]] = []
        for p_entry in population_list:
            county = p_entry.get("county", "")
            state = p_entry.get("state", "")
            population = p_entry.get("population", "")

            # Check if the entry belongs to a gdp combination area
            gdp_area = None
            for c in gdp_combination_areas:
                if c.get("county") == county and c.get("state") == state:
                    gdp_area = c.get("gdp_area", "")
                    break

            # Merge population data with gdp area data
            if gdp_area:
                merged_entry_list.append(
                    {
                        "county": county,
                        "state": state,
                        "population": population,
                        "gdp_area": gdp_area,
                    }
                )

            # Merge population data with gdp data
            gdp = None
            for c in gdp_list:
                if c.get("county") == county and c.get("state") == state:
                    gdp = c.get("gdp", "")
                    break

            if gdp:
                merged_entry_list.append(
                    {
                        "county": county,
                        "state": state,
                        "population": population,
                        "gdp": gdp,
                    }
                )
        return merged_entry_list

    @classmethod
    def write_config_to_file(cls):
        with open(
            cls.processed_data_path / "intermediate_state.json",
            mode="w",
            encoding="utf8",
        ) as config_file:
            _ = config_file.write(json.dumps(cls.merge_gdp_population_csv_data()))


# A country class contains all valid states and is in charge of organizing them into super-states
# A country initializes states and combines them into super-states
# A country will default to naming the super state after the state with the most gdp prefixed with
# "Super", for example, a super-state of Ohio and Indiana would be called "Super Ohio"
class Country:
    pass
