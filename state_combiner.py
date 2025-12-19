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
    # state_by_gdp: dict['str', int] = { 'ca': 4_103_124, 'tx': 2_709_393, 'ny': 4_103_124, 'fl': 1_705_565, 'il': 1_137_244, 'pa': 1_024_206, 'oh': 927_740, 'ga': 882535, 'wa': 854683, 'nj': 846587, 'nc': 839122, 'ma': 780666, 'va': 764475, 'mi': 719392, 'co': 553323, 'az': 552167, 'tn': 549709, 'md': 719392, 'in': 499503, 'mn': 500851, 'wi': 451285, 'mo': 451285, 'ct': 365723, 'sc': 349965, 'or': 331_029, 'la': 327782, 'al': 321238, 'ut': 300904, 'ky': 293021, 'ok': 265779, 'nv': 260728, 'ia': 257021, 'ks': 234673, 'ar': 188723, 'ne': 185411, 'ms': 157491, 'nm': 140542, 'id': 128132, 'nh': 121829, 'hi': 115627, 'wv': 107660, 'de': 103253, 'me': 98606, 'ri': 82493, 'mt': 75999, 'nd': 75399, 'sd': 75179, 'ak': 69969, 'wy': 52946, 'vt': 45707 }

    def __init__(self, state_list: list[State]):
        self.state_list: list[State] = state_list
        self.gdp: int = 0

    def total_gdp(self):
        print("TODO")
