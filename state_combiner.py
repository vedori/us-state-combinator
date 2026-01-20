import json
import pprint
import random


# A StateReader is a class for reading and initializing states from a file
class StateFileReader:
    def get_states_from_file(self, yaml_file):
        pass


# A country class contains all valid states and is in charge of organizing them into super-states
# A country initializes states and combines them into super-states
# A country will default to naming the super state after the state with the most gdp prefixed with
# "Super", for example, a super-state of Ohio and Indiana would be called "Super Ohio"
class Country:
    def get_states_from_file(self, yaml_file):
        pass


# Represents a regular state
# It should have a name, gdp, and possible abbreviation
class State:
    def __init__(self, state_name: str, gdp: int):
        self.state_name: str = state_name
        self.gdp: int = gdp


# A grouping of two or more states
class SuperState:
    def __init__(self, state_list: list[State]):
        self.state_list: list[State] = state_list
        self.gdp: int = 0

    def total_gdp(self):
        print("TODO")
