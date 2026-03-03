from enum import auto, Enum


# *****ENUM CLASSES*****
class Actions(Enum):
    EAT = 1
    SLEEP = auto()
    PLAY = auto()
    WEIGHTED_SCORE = auto()
    EXIT = auto()


class Pets(Enum):
    DRAGON = 1
    CAPYBARA = auto()
    ARMADILLO = auto()


class Levels(Enum):
    EASY = 1
    MEDIUM = auto()
    HARD = auto()


class LogFields(Enum):
    DATE = 0
    TIME = auto()
    LEVEL = auto()
    SESSION = auto()
    DATA_START = auto()


# *****DEFAULTS*****
DEFAULT_HUNGER = 50
DEFAULT_HAPPINESS = 50
DEFAULT_ENERGY = 50
DEFAULT_POINTS = 0
TRAIT_MAX_VAL = 100
TRAIT_MIN_VAL = 0
DEFAULT_LOG_FILE = "log.txt"
DEFAULT_ACTION_INDEX_IN_DATA = 1


# *****PARAMS CHANGE FOR ACTION*****
# Eat
HUNGER_REDUCE_WHEN_EAT = {1: 25, 2: 20, 3: 20}
ENERGY_ADD_WHEN_EAT = {1: 20, 2: 10, 3: 10}
POINTS_ADD_WHEN_EAT = 15

# Sleep
HUNGER_ADD_WHEN_SLEEP = {1: 10, 2: 20, 3: 15}
ENERGY_ADD_WHEN_SLEEP = {1: 50, 2: 40, 3: 10}
POINTS_ADD_WHEN_SLEEP = 10

# Play
ENERGY_REDUCE_WHEN_PLAY = {1: 5, 2: 10, 3: 10}
HAPPINESS_ADD_WHEN_PLAY = {1: 25, 2: 30, 3: 20}
POINTS_ADD_WHEN_PLAY = 20
