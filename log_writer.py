import logging


def config_logging(log_file: str) -> None:
    """
    The function defines the logging configuration.
    :param log_file: The name of the log file
    :return: None.
    """
    if logging.root.handlers:
        return

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level=logging.DEBUG,
        filename=log_file,
    )
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    console.setFormatter(logging.Formatter(f"\n%(levelname)s - %(message)s"))
    logger.addHandler(console)
    return None


def new_pet_log_info(
    name: str, pet_type: str, hunger: int,
        happiness: int, energy: int, points: int) -> None:
    """
    The function creates a log about newly created pet.
    :param name: The name of the pet.
    :param pet_type: The type of pet.
    :param hunger: The hunger level of the pet.
    :param happiness: The happiness level of the pet.
    :param energy: The energy level of the pet.
    :param points: The points the pet has.
    :return: None.
    """
    logging.info("New pet was created! Name: %s, Type: %s,"
                 " Hunger: %s, Happiness: %s, Energy: %s, Points: %s",
                 name, pet_type, hunger, happiness, energy, points)


def action_log_info(action: str) -> None:
    """
    The function creates a log about actions.
    :param action: The action that was done.
    :return: None.
    """
    logging.info(f"Action: {action} was made")


def any_error(data: str) -> None:
    """
    The function creates an error log for any error.
    :param data: The error.
    :return:
    """
    logging.error(f"{data}")


def chose_info(what_chosen: str, data: str) -> None:
    """
    The function creates an info log when pet type is chosen.
    :param what_chosen: what was chosen.
    :param data: The choice.
    :return: None.
    """
    logging.info(f"Chosen {what_chosen}: {data}")


def any_info(data: str) -> None:
    """
    The function creates an info log for any info.
    :param data: The info.
    :return: None.
    """
    logging.info(f"{data}")


def invalid_not_int_error(what_invalid: str) -> None:
    """
    The function creates an error log when str was given instead of int.
    :param what_invalid: what invalid, for example: level, action...
    :return: None.
    """
    logging.error(f"Invalid {what_invalid}! Please enter an integer.")


def invalid_error(what_invalid: str, data: str) -> None:
    """
    The function creates an error log when invalid pet type was given.
    :param what_invalid: what invalid, for example: level, action...
    :param data: The wrong input that was given.
    :return: None.
    """
    logging.error(f"The {what_invalid} {data} is invalid.")


def action_fail_info(data: str) -> None:
    """
    The function creates an action fails.
    :param data: The action.
    :return: None.
    """
    logging.info(f"Action {data} failed.")
