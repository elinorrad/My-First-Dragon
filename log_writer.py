import logging

import pet


class SafeFormatter(logging.Formatter):
    """
    The formatter class defines the log format.
    """
    def format(self, record):
        if not hasattr(record, 'session_id'):
            record.session_id = '--'
        return super().format(record)


class ActionListHandler(logging.Handler):
    """
    The handler class defines the action list.
    """
    def __init__(self):
        super().__init__()
        self.actions = []

    def emit(self, record):
        """
        The function emits the log actions.
        :param record: The log record to emit.
        :return: The log actions.
        """
        msg = record.getMessage()
        if "Action:" in msg:
            cleaned = msg.replace("Action:", "")
            date = self.formatter.formatTime(record, self.formatter.datefmt)
            self.actions.append(f"{date} - {cleaned}")



def config_logging(log_file: str) -> None:
    """
    The function defines the logging configuration.
    :param log_file: The name of the log file
    :return: None.
    """
    if logging.root.handlers:
        return
    formatter = SafeFormatter("%(asctime)s %(levelname)s"
                              " %(session_id)s %(message)s",
                              datefmt="%d-%b-%y %H:%M:%S")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    console.setFormatter(logging.Formatter("\n%(levelname)s - %(message)s"))

    action_handler = ActionListHandler()
    action_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(file_handler)
    root.addHandler(console)
    root.addHandler(action_handler)


def get_action_logs() -> list:
    """
    The function gets all the actions logs.
    :return: All actions logs.
    """
    root = logging.getLogger()

    for handler in root.handlers:
        if isinstance(handler, ActionListHandler):
            return handler.actions

    return []


def new_pet_log_info(
    name: str, pet_type: str, hunger: int, happiness: int,
        energy: int, points: int, session_id: str) -> None:
    """
    The function creates a log about newly created pet.
    :param session_id: The session id the pet was created for.
    :param name: The name of the pet.
    :param pet_type: The type of pet.
    :param hunger: The hunger level of the pet.
    :param happiness: The happiness level of the pet.
    :param energy: The energy level of the pet.
    :param points: The points the pet has.
    :return: None.
    """
    logging.info(
        "New pet was created! Name: %s, Type: %s,"
        " Hunger: %s, Happiness: %s, Energy: %s, Points: %s",
        name,
        pet_type,
        hunger,
        happiness,
        energy,
        points,
        extra={"session_id": session_id},
    )


def action_log_info(action: str, my_pet) -> None:
    """
    The function creates a log about actions.
    :param my_pet: The pet that the log was written about.
    :param action: The action that was done.
    :return: None.
    """
    logging.info("Action: %s was made - %s", action, my_pet.status,
                 extra={"session_id": my_pet.session_id})


def any_error(data: str, session_id: str) -> None:
    """
    The function creates an error log for any error.
    :param session_id: The session id the log writen from.
    :param data: The error.
    :return:
    """
    logging.error(f"{data}", extra={"session_id": session_id})



def chose_info(what_chosen: str, data: str, session_id: str) -> None:
    """
    The function creates an info log when pet type is chosen.
    :param session_id: The session id the log writen from.
    :param what_chosen: what was chosen.
    :param data: The choice.
    :return: None.
    """
    logging.info(f"Chosen {what_chosen}: {data}",
                 extra={"session_id": session_id})


def any_info(data: str, session_id: str) -> None:
    """
    The function creates an info log for any info.
    :param session_id: The session id the log writen from.
    :param data: The info.
    :return: None.
    """
    logging.info(f"{data}", extra={"session_id": session_id})


def invalid_not_int_error(what_invalid: str, session_id: str) -> None:
    """
    The function creates an error log when str was given instead of int.
    :param session_id: The session id the log writen from.
    :param what_invalid: what invalid, for example: level, action...
    :return: None.
    """
    logging.error(f"Invalid {what_invalid}! Please enter an integer.",
                  extra={"session_id": session_id})


def invalid_error(what_invalid: str, data: str, session_id: str) -> None:
    """
    The function creates an error log when invalid pet type was given.
    :param session_id: The session id the log writen from.
    :param what_invalid: what invalid, for example: level, action...
    :param data: The wrong input that was given.
    :return: None.
    """
    logging.error(f"The {what_invalid} {data} is invalid.",
                  extra={"session_id": session_id})


def action_fail_info(data: str, session_id: str, my_pet: pet.Pet) -> None:
    """
    The function creates an action fails.
    :param my_pet: The pet that the action was made for.
    :param session_id: The session id the log writen from.
    :param data: The action.
    :return: None.
    """
    logging.info(f"Action: {data} failed - {my_pet.status}",
                 extra={"session_id": session_id})
