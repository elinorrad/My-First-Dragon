import logging


def config_logging(log_file: str) -> None:
    """
    The function defines the logging configuration.
    :param log_file: The name of the log file
    :return: None.
    """
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


def new_pet_log_info(
    name: str, pet_type: str, hunger: int, happiness: int,
        energy: int, points: int) -> None:
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
    logging.info(
        f"New pet was created! Name: {name}, Type: {pet_type},"
        f" Hunger: {hunger},"
        f"Happiness: {happiness}, Energy: {energy}, Points: {points}"
    )


def action_log_info(action: str) -> None:
    """
    The function creates a log about actions.
    :param action: The action that was done.
    :return: None.
    """
    logging.info(f"Action: {action} was made")


def pet_type_log_error(pet_type: str) -> None:
    """
    The function creates an error log when invalid pet type was given.
    :param pet_type: The type of pet.
    :return: None.
    """
    logging.error(f"The pet type {pet_type} is invalid.")


def pet_name_log_error() -> None:
    """
    The function creates an error log when empty pet name was given.
    :return:
    """
    logging.error(f"Pet name cant be empty.")


def invalid_traits_param_error() -> None:
    """
    The function creates an error log when invalid pet traits params was given.
    :return: None.
    """
    logging.error(f"Invalid pet traits params were given.")


def invalid_level_error() -> None:
    """
    The function creates an error log when invalid level was given.
    :return: None.
    """
    logging.error(f"Invalid level was given.")


def invalid_action_error() -> None:
    """
    The function creates an error log when invalid action was given.
    :return: None.
    """
    logging.error(f"Invalid action was given.")


def invalid_level_not_int_error() -> None:
    """
    The function creates an error log when invalid level was given.
    :return: None.
    """
    logging.error(f"Invalid level! Level must be an integer.")


def level_chose_info(level: int) -> None:
    """
    The function creates an info log when level is chosen.
    :param level: The level chosen.
    :return: None.
    """
    logging.info(f"Chosen level: {level}")


def pet_type_chose_info(pet_type: str) -> None:
    """
    The function creates an info log when pet type is chosen.
    :param pet_type: The type of pet.
    :return: None.
    """
    logging.info(f"Chosen pet type: {pet_type}")


def pet_name_chose_info(pet_name: str) -> None:
    """
    The function creates an info log when pet name is chosen.
    :param pet_name: The name of the pet.
    :return: None.
    """
    logging.info(f"Chosen pet name: {pet_name}")


def pet_score_info(score: float) -> None:
    """
    The function creates an info log about pet score.
    :param score: pet score.
    :return: None.
    """
    logging.info(f"Pet score: {score}")


def win_info() -> None:
    """
    The function creates an info log when there is a win.
    :return: None.
    """
    logging.info(f"Win!")


def invalid_selection_not_int_error() -> None:
    """
    The function creates an error log when invalid selection was given.
    :return: None.
    """
    logging.error(f"Invalid selection! Selection must be an integer.")


def invalid_selection_error(selection: int) -> None:
    """
    The function creates an error log when invalid selection was given.
    :param selection: The selection that was given.
    :return: None.
    """
    logging.error(f"Invalid selection! {selection} isnt an exist selection.")
