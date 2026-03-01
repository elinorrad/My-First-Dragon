import os
import log_writer
from defaults import *


def check_pets_type(pet_type: str) -> bool:
    """
    This function checks if the pet type is valid.
    :param pet_type: The pet type to be checked.
    :return: If the pet type is valid.
    """
    if pet_type == "":
        return False
    elif pet_type not in POSSIBLE_PETS:
        log_writer.pet_type_log_error(pet_type)
        return False
    return True


def check_pet_name(name: str) -> bool:
    """
    This function checks if the pet name is valid.
    :param name: The pet name to be checked.
    :return: If the pet name is valid.
    """
    if name == "\t":
        return False
    elif name.strip() == "":
        log_writer.pet_name_log_error()
        return False
    return True


def check_pet_params(hunger: int, happiness: int, energy: int) -> None:
    """
    This function checks if the pet params are valid
     and raises an error if not.
    :param hunger: The hunger of the pet.
    :param happiness: The happiness of the pet.
    :param energy: The energy of the pet.
    :param log_file: The log file of the pet.
    :return: None.
    """
    if (
        hunger < TRAIT_MIN_VAL
        or hunger > TRAIT_MAX_VAL
        or happiness < TRAIT_MIN_VAL
        or happiness > TRAIT_MAX_VAL
        or energy < TRAIT_MIN_VAL
        or energy > TRAIT_MAX_VAL
    ):
        log_writer.invalid_traits_param_error()
        raise ValueError("One of the traits parameters is invalid.")


def check_chosen_level(level: int) -> bool:
    """
    This function checks if the chosen level is valid.
    :param level: The chosen level to be checked.
    :return: If the chosen level is valid.
    """
    if level == 0:
        return False
    if level != 1 and level != 2 and level != 3:
        log_writer.invalid_level_error()
        return False
    return True


def print_possible_pet_types() -> None:
    """
    This function prints the possible pet types.
    :return: None.
    """
    print("Here is the possible pet types: ")
    for pet in POSSIBLE_PETS:
        print(pet, end=" ")
    print()


def generate_log_file_path() -> str:
    """
    This function generates the log file path.
    :return: The log file path.
    """
    log_file = DEFAULT_LOG_FILE
    i = 0
    for filename in os.listdir(os.getcwd()):
        if log_file in filename:
            i += 1
            log_file = DEFAULT_LOG_FILE + str(i)
    with open(log_file, "w"):
        pass
    return log_file
