import itertools
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

from us_states import US_STATES
from utils import csv_utils

GDP_COMBINATION_SEPERATOR: Final = " + "


# Immutable
# Represents  what a county should have
# It should have a name, gdp and population
@dataclass(frozen=True, order=True)
class County:
    name: str
    population: int
    gdp: int


# A county that has a gdp area that groups multiple counties
# as one gdp unit
@dataclass(frozen=True, order=True)
class GDPGroupedCounty(County):
    gdp_area: str


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
    processed_data_path: Path = data_path / "processed"
    final_data_path: Path = data_path / "final"

    population_csv_file: Path = raw_data_path / "2020-pop.csv"
    gdp_csv_file: Path = raw_data_path / "2020-gdp.csv"

    gdp_areas: dict[str, int] = dict()

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
                        "gdp": combo_area.get("gdp", ""),
                        "gdp_area": combo_area.get("county", ""),
                    }
                    yield entry

        gdp_combination_areas = list(map(generate_expanded_entries, gdp_list))
        gdp_combination_areas = [
            individual_entry
            for gdp_combination_area in gdp_combination_areas
            for individual_entry in gdp_combination_area
        ]
        # Builds a JSON representation of the static state config
        # Iterates through the population data set since it has every county
        # Adds a relevant field that indicates counties grouped by gdp
        merged_entry_list: list[dict[str, str | int]] = []
        for p_entry in population_list:
            county = p_entry.get("county", "")
            state = p_entry.get("state", "")
            population = p_entry.get("population", "")

            # Gets the gdp of the entry from gdp_list
            gdp = None
            for c in gdp_list:
                if c.get("county") == county and c.get("state") == state:
                    gdp = c.get("gdp", "")
                    break

            # Gets the gdp area from gdp_combination_areas if the entry belongs to a gdp combination area
            # Uses the gdp from gdp_combination_area since it contains entries for individual counties
            gdp_area = None
            for c in gdp_combination_areas:
                if c.get("county") == county and c.get("state") == state:
                    gdp_area = c.get("gdp_area", "")
                    gdp = c.get("gdp", "")
                    break

            # Converts the gdp into an int
            if gdp:
                gdp = int(gdp, 10)

            # Converts the population into an int
            if population:
                population = int(population, 10)

            # Merge population data with gdp area data
            if gdp_area and gdp:
                merged_entry_list.append(
                    {
                        "county": county,
                        "state": state,
                        "population": population,
                        "gdp_area": gdp_area,
                    }
                )

                # Add gdp_area to lookup table alongside its gdp
                cls.gdp_areas.update({gdp_area: gdp})

            # Merge population data with gdp data
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
    def generate_state_from_config(cls):
        county_gdp_pop_data = cls.merge_gdp_population_csv_data()

        for entry in county_gdp_pop_data:
            pass

    @classmethod
    def write_config_to_file(cls):
        county_data = cls.merge_gdp_population_csv_data()
        county_json = json.dumps(county_data)
        gdp_area_json = json.dumps(cls.gdp_areas)

        # Writes the county data to an intermediate file before processing
        with open(
            cls.processed_data_path / "intermediate_state.json",
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
            state_counties = all_states.get(state)
            if state_counties is not None:
                county_list: list[dict[str, str]] = state_counties.get("counties", "")
                county_list.append(c)

        state_json = json.dumps(all_states, indent=1)
        print(state_json)

        # Writes state data
        with open(
            cls.final_data_path / "state_data.json",
            mode="w",
            encoding="utf8",
        ) as config_file:
            _ = config_file.write(state_json)

        # Seperate file in final data path for GDP Areas
        with open(
            cls.final_data_path / "gdp_areas.json",
            mode="w",
            encoding="utf8",
        ) as config_file:
            _ = config_file.write(gdp_area_json)


# A country class contains all valid states and is in charge of organizing them into super-states
# A country initializes states and combines them into super-states
# A country will default to naming the super state after the state with the most gdp prefixed with
# "Super", for example, a super-state of Ohio and Indiana would be called "Super Ohio"
class Country:
    pass
