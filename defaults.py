from enum import auto, Enum


# *****ENUM CLASSES*****
class Actions(Enum):
    EAT = 1
    SLEEP = auto()
    PLAY = auto()
    WEIGHTED_SCORE = auto()
    EXIT = auto()


# *****DEFAULTS*****
POSSIBLE_PETS = ["Dragon", "Capybara", "Labubu"]
DEFAULT_HUNGER = 50
DEFAULT_HAPPINESS = 50
DEFAULT_ENERGY = 50
DEFAULT_POINTS = 0
TRAIT_MAX_VAL = 100
TRAIT_MIN_VAL = 0
DEFAULT_LOG_FILE = "log.txt"


# *****PARAMS CHANGE FOR ACTION*****
# Eat
HUNGER_REDUCE_WHEN_EAT = [25, 20, 20]
ENERGY_ADD_WHEN_EAT = [20, 10, 10]
POINTS_ADD_WHEN_EAT = 15

# Sleep
HUNGER_ADD_WHEN_SLEEP = [10, 20, 15]
ENERGY_ADD_WHEN_SLEEP = [50, 40, 10]
POINTS_ADD_WHEN_SLEEP = 10

# Play
ENERGY_REDUCE_WHEN_PLAY = [5, 10, 10]
HAPPINESS_ADD_WHEN_PLAY = [25, 30, 20]
POINTS_ADD_WHEN_PLAY = 20


# *****PRINTS*****
WELCOME_MSG = "Welcome to the my first dragon game!\n"\
              "Its time to create a pet!"

MENU_MSG = (
    "Choose an action to do from the menu:\n"
    "1. Feed your pet.\n"
    "2. Put your pet to sleep.\n"
    "3. Give your pet a play time.\n"
    "4. Get pets weighted score.\n"
    "5. Exit the game.\n"
)

LEVEL_MSG = (
    "Which level would you like to play:\n" "1. Easy.\n"
    "2. Medium.\n" "3. Hard.\n"
)
