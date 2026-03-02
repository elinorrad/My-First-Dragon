import os
import log_writer
from defaults import *


def check_pets_type(pet_type: int) -> bool:
    """
    This function checks if the pet type is valid.
    :param pet_type: The pet type to be checked.
    :return: If the pet type is valid.
    """
    if pet_type not in [pet.value for pet in Pets]:
        log_writer.invalid_error("pet type", str(pet_type))
        return False
    return True


def check_pet_name(name: str) -> bool:
    """
    This function checks if the pet name is valid.
    :param name: The pet name to be checked.
    :return: If the pet name is valid.
    """
    if name.strip() == "":
        log_writer.any_error("Pet name cant be empty.")
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
        log_writer.invalid_error(
            "traits param",
            f"hunger: {hunger}, " f"happiness: {happiness}, energy: {energy}",
        )
        raise ValueError("One of the traits parameters is invalid.")


def check_chosen_level(level: int) -> bool:
    """
    This function checks if the chosen level is valid.
    :param level: The chosen level to be checked.
    :return: If the chosen level is valid.
    """
    if level != 1 and level != 2 and level != 3:
        log_writer.invalid_error("level", str(level))
        return False
    return True


def print_possible_pet_types() -> None:
    """
    This function prints the possible pet types.
    :return: None.
    """
    print("Here is the possible pet types: ")
    for pet in Pets:
        print(f"{pet.value}.", pet.name.capitalize(), end=" ")
    print()


def generate_log_file_path() -> str:
    """
    This function generates the log file path.
    :return: The log file path.
    """
    log_file = DEFAULT_LOG_FILE
    i = 1
    while log_file in os.listdir(os.getcwd()):
        log_file = DEFAULT_LOG_FILE + str(i)
        i += 1
    with open(log_file, "w"):
        pass
    return log_file
