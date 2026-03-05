from dataclasses import dataclass, field

from utils import csv_utils


# Immutable
# Represents what a county should have
# It should have a name population
@dataclass(frozen=True, order=True)
class BaseCounty:
    name: str
    population: int


# Immutable
# Represents a regular County
# Alongside a name and population it should have a gdp
@dataclass(frozen=True, order=True)
class County(BaseCounty):
    gdp: int


# Immutable
# Represents a county that is part of a gdp group
# A gdp group can be used to find the gdp of all the grouped counties
# Alongside a name and population it should have a gdp group label
@dataclass(frozen=True, order=True)
class GDPGroupedCounty(BaseCounty):
    gdp_group: str

    def get_gdp(self) -> int:
        gdp = csv_utils.gdp_group_table[self.gdp_group]
        return gdp


# A country class contains all valid states and is in charge of organizing them into custom states
# A country initializes all states and uses all their counties to form custom states
# A country will default to naming the super state after the state with the most gdp prefixed with
# "Super", for example, a super-state of Ohio and Indiana would be called "Super Ohio"
class Country:
    pass


# The main mutable component of this program
# A container for one or more counties
# It has a name and a list of counties
@dataclass(order=True)
class CustomState:
    counties: list[BaseCounty] = field(default_factory=list, compare=False, hash=False)

    # TODO: rework this to "borrow" counties from Country
    def get_gdp(self) -> int:
        gdp = 0
        grouped_counties: set[str] = set()
        for c in self.counties:
            if isinstance(c, County):
                gdp += c.gdp
            if isinstance(c, GDPGroupedCounty):
                if c.gdp_group not in grouped_counties:
                    grouped_counties.add(c.gdp_group)
                    gdp += c.get_gdp()
        return gdp
