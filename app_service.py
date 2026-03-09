import os

from flask import Flask

import defaults
import general_functions


def pet_image(pet_type: str) -> str:
    """
    The function returns the pet image url.
    :param pet_type: The pet type.
    :return: The pet image url.
    """
    if pet_type == defaults.Pets.DRAGON.name:
        return "/static/images/dragon.png"
    elif pet_type == defaults.Pets.CAPYBARA.name:
        return "/static/images/capybara.png"
    elif pet_type == defaults.Pets.ARMADILLO.name:
        return "/static/images/armadillo.png"
    else:
        return "error"


def create_app() -> Flask:
    """
    The function creates the flask app
    :return: The flask app
    """
    app = Flask(__name__)
    app.config["LOG_FILE"] =\
        general_functions.generate_log_file_path(os.getcwd())
    app.config["USER_TO_PET"] = {}
    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
    app.config["IS_ANIMAL_CREATED"] = {}
    app.config["POSSIBLE_PETS"] = {pet.value: pet.name.capitalize()
                                   for pet in defaults.Pets}
    app.config["POSSIBLE_LEVELS"] = {level.value: level.name.capitalize()
                                     for level in defaults.Levels}
    app.config["POSSIBLE_ACTIONS"] = {}
    return app


def actions_by_session(log_file: str, session_id: str) -> list:
    """
    The function returns a list of actions based on a session id.
    :param log_file: The log file the actions took from.
    :param session_id: The session id to filter the actions by.
    :return: The list of actions based on a session id.
    """
    result = []
    with open(log_file, "r") as f:
        opened_log_file = f.read()
    actions = [
        "-".join(row.split("- INFO - " + session_id + " - Action:"))
        for row in opened_log_file.strip().split("\n")
        if "Action" in row and session_id ==
           row.split(" ")[defaults.LogFields.SESSION.value]
    ]
    for action in actions:
        splited_action = action.split(" ")
        action_dict = {"timestamp":
                        splited_action[defaults.LogFields.DATE.value] +
                        " " + splited_action[defaults.LogFields.TIME.value],
                       defaults.LogFields.LEVEL.name.lower():
                           splited_action[defaults.LogFields.LEVEL.value],
                       defaults.LogFields.SESSION.name.lower():
                           splited_action[defaults.LogFields.SESSION.value],
                       "data": " ".join(splited_action[defaults.
                                        LogFields.DATA_START.value:])}
        result.append(action_dict)
    return result
