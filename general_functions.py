import os

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

import log_writer
import defaults


def check_pets_type(pet_type: int, session_id: str) -> bool:
    """
    This function checks if the pet type is valid.
    :param session_id: The session id that the pet was created from.
    :param pet_type: The pet type to be checked.
    :return: If the pet type is valid.
    """
    if pet_type not in [pet.value for pet in defaults.Pets]:
        log_writer.invalid_error("pet type", str(pet_type), session_id)
        return False
    return True


def check_pet_name(name: str, session_id: str) -> bool:
    """
    This function checks if the pet name is valid.
    :param session_id: The session id that the pet was created from.
    :param name: The pet name to be checked.
    :return: If the pet name is valid.
    """
    if name.strip() == "":
        log_writer.any_error("Pet name cant be empty.", session_id)
        return False
    return True


def check_pet_params(hunger: int, happiness: int,
                     energy: int, session_id: str) -> None:
    """
    This function checks if the pet params are valid
     and raises an error if not.
    :param session_id: The session id that the pet was created from.
    :param hunger: The hunger of the pet.
    :param happiness: The happiness of the pet.
    :param energy: The energy of the pet.
    :return: None.
    """
    if (
        hunger < defaults.TRAIT_MIN_VAL
        or hunger > defaults.TRAIT_MAX_VAL
        or happiness < defaults.TRAIT_MIN_VAL
        or happiness > defaults.TRAIT_MAX_VAL
        or energy < defaults.TRAIT_MIN_VAL
        or energy > defaults.TRAIT_MAX_VAL
    ):
        log_writer.invalid_error(
            "traits param",
            f"hunger: {hunger}, " f"happiness: {happiness}, energy: {energy}",
            session_id)
        raise ValueError("One of the traits parameters is invalid.")


def check_chosen_level(level: int, session_id: str) -> bool:
    """
    This function checks if the chosen level is valid.
    :param session_id: The session that the chosen level was created from.
    :param level: The chosen level to be checked.
    :return: If the chosen level is valid.
    """
    if level not in [curr_level.value for curr_level in defaults.Levels]:
        log_writer.invalid_error("level", str(level), session_id)
        return False
    return True


def generate_log_file_path(dir_for_log: str) -> str:
    """
    This function generates the log file path.
    :param dir_for_log: The directory where the log file is stored.
    :return: The log file path.
    """
    log_file = defaults.DEFAULT_LOG_FILE
    i = 1
    while log_file in os.listdir(dir_for_log):
        log_file = defaults.DEFAULT_LOG_FILE + str(i)
        i += 1
    with open(os.path.join(dir_for_log, log_file), "w"):
        pass
    return log_file


def clamp(value: int, min_val: int, max_val: int) -> int:
    """
    This function returns the value clamped to the given range.
    :param value: The value to be clamped.
    :param min_val: The minimum value to be clamped.
    :param max_val: The maximum value to be clamped.
    :return: The clamped value.
    """
    return max(min(value, max_val), min_val)


def check_create_pet_params(pet_type: str, pet_name: str,
                            level: str, session_id: str) -> str:
    """
    The function checks the pet type and pet name and level.
    :param session_id: The session id that the pet was created from.
    :param pet_type: The pet type to check.
    :param pet_name: The pet name to check.
    :param level: The level to check.
    :return: The error if there is an error.
    """
    error = ""
    try:
        pet_type_int = int(pet_type)
        if not check_pets_type(pet_type_int, session_id):
            error += "Invalid pet type! "
    except ValueError:
        log_writer.invalid_not_int_error("pet type", session_id)
        error += "Invalid pet type! Please enter an integer. "

    if not check_pet_name(pet_name, session_id):
        error += "Invalid pet name! "

    try:
        level_int = int(level)
        if not check_chosen_level(level_int, session_id):
            error += "Invalid level! "
    except ValueError:
        log_writer.invalid_not_int_error("level", session_id)
        error += "Invalid level! Please enter an integer. "

    return error


def set_basic_attributes(span, session_id: str, pet_name: str,
                         pet_type: str) -> None:
    """
    The function sets the basic attributes of the pet.
    :param span: The span to set the basic attributes to.
    :param session_id: The session id that the pet was created from.
    :param pet_name: The pet name.
    :param pet_type: The pet type.
    :return: None.
    """
    span.set_attribute("session_id", session_id)
    span.set_attribute("pet_name", pet_name)
    span.set_attribute("pet_type", pet_type)
