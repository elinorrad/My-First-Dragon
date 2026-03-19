import random
from typing import Dict

from opentelemetry import trace
from opentelemetry.trace import Tracer, Status, StatusCode

import general_functions
import log_writer
import defaults
import sqlite_db


class Pet:
    def __init__(
            self,
            name: str,
            pet_type: str,
            level: int,
            session_id: str,
            hunger: int = defaults.DEFAULT_HUNGER,
            happiness: int = defaults.DEFAULT_HAPPINESS,
            energy: int = defaults.DEFAULT_ENERGY,
            points: int = defaults.DEFAULT_POINTS,
            log_file: str = defaults.DEFAULT_LOG_FILE
    ) -> None:
        general_functions.check_pet_params(
            hunger, happiness, energy, session_id
        )
        self._name = name
        self._pet_type = pet_type
        self._level = level
        self._hunger = hunger
        self._happiness = happiness
        self._energy = energy
        self._points = points
        self._log_file = log_file
        self._history: list = []
        self._session_id = session_id
        log_writer.new_pet_log_info(
            name,
            pet_type,
            hunger,
            happiness,
            energy,
            points,
            self._session_id
        )

    def _add_action_to_history(self, action: str) -> None:
        """
        The function for adding an action to the history.
        :param action: The action to add to the history.
        :return: None.
        """
        self._history.append(action)

    def eat(self) -> str:
        """
        The function for the pet to eat.
        :return: a success or fail message.
        """
        action_name = "eat"
        tracer = trace.get_tracer(__name__)

        with tracer.start_as_current_span(action_name) as span:

            general_functions.set_basic_attributes(span, self._session_id,
                                                   self._name, self._pet_type)

            span.set_attribute("hunger_before", self._hunger)
            span.set_attribute("energy_before", self._energy)

            is_succeeded = self._action_succeeded(action_name)
            if not is_succeeded:
                span.set_status(Status(StatusCode.ERROR, "The pet vomited"))
                span.set_attribute("hunger_after", self._hunger)
                span.set_attribute("energy_after", self._energy)
                return "ughhh the pet vomited"

            self._hunger = general_functions.clamp(
                self._hunger - defaults.HUNGER_REDUCE_WHEN_EAT[self._level],
                defaults.TRAIT_MIN_VAL,
                defaults.TRAIT_MAX_VAL,
            )

            self._energy = general_functions.clamp(
                self._energy + defaults.ENERGY_ADD_WHEN_EAT[self._level],
                defaults.TRAIT_MIN_VAL,
                defaults.TRAIT_MAX_VAL,
            )

            span.set_attribute("hunger_after", self._hunger)
            span.set_attribute("energy_after", self._energy)

            span.set_attribute("points_before", self._points)
            self._points += defaults.POINTS_ADD_WHEN_EAT
            span.set_attribute("points_after", self._points)

        self._add_action_to_history(action_name)
        log_writer.action_log_info(action_name, self)
        sqlite_db.update_pet(
            self._session_id,
            self,
            defaults.DATABASE_FILE
        )
        return (
            f"The pet ate! "
            f"hunger: {self._hunger}, "
            f"energy: {self._energy}, "
            f"happiness: {self._happiness}, "
            f"points: {self._points}"
        )

    def sleep(self) -> str:
        """
        The function for the pet to sleep.
        :return: a success or fail message.
        """

        action_name = "sleep"
        tracer = trace.get_tracer(__name__)

        with tracer.start_as_current_span(action_name) as span:

            general_functions.set_basic_attributes(span, self._session_id,
                                                   self._name, self._pet_type)

            span.set_attribute("hunger_before", self._hunger)
            span.set_attribute("energy_before", self._energy)

            is_succeeded = self._action_succeeded(action_name)
            if not is_succeeded:
                span.set_status(Status(StatusCode.ERROR, "The pet slept bad"))
                span.set_attribute("hunger_after", self._hunger)
                span.set_attribute("energy_after", self._energy)
                return "ughhh I slept so bad!! I am just more tired now"


            self._hunger = general_functions.clamp(
                self._hunger + defaults.HUNGER_ADD_WHEN_SLEEP[self._level],
                defaults.TRAIT_MIN_VAL,
                defaults.TRAIT_MAX_VAL,
            )

            self._energy = general_functions.clamp(
                self._energy + defaults.ENERGY_ADD_WHEN_SLEEP[self._level],
                defaults.TRAIT_MIN_VAL,
                defaults.TRAIT_MAX_VAL,
            )

            span.set_attribute("hunger_after", self._hunger)
            span.set_attribute("energy_after", self._energy)

            span.set_attribute("points_before", self._points)
            self._points += defaults.POINTS_ADD_WHEN_SLEEP
            span.set_attribute("points_after", self._points)

        self._add_action_to_history(action_name)
        log_writer.action_log_info(action_name, self)
        sqlite_db.update_pet(self._session_id, self, defaults.DATABASE_FILE)

        return (
            f"The pet slept! "
            f"Current trait values: hunger: {self._hunger},"
            f" energy: {self._energy}, happiness: {self._happiness},"
            f" points: {self._points}"
        )

    def play(self) -> str:
        """
        The function for the pet to play.
        :return: a success or fail message.
        """

        action_name = "play"
        tracer = trace.get_tracer(__name__)

        with tracer.start_as_current_span(action_name) as span:

            general_functions.set_basic_attributes(span, self._session_id,
                                                   self._name, self._pet_type)

            span.set_attribute("energy_before", self._energy)
            span.set_attribute("happiness_before", self._happiness)

            is_succeeded = self._action_succeeded(action_name)
            if not is_succeeded:
                span.set_status(Status(StatusCode.ERROR,
                                    "The pet didn't like the play"))
                span.set_attribute("energy_after", self._energy)
                span.set_attribute("happiness_after", self._happiness)
                return "ughhh I didn't like the play at all!" \
                       " Now I am not happy at all."

            self._energy = general_functions.clamp(
                self._energy - defaults.ENERGY_REDUCE_WHEN_PLAY[self._level],
                defaults.TRAIT_MIN_VAL,
                defaults.TRAIT_MAX_VAL,
            )

            self._happiness = general_functions.clamp(
                self._happiness + defaults.HAPPINESS_ADD_WHEN_PLAY[self._level],
                defaults.TRAIT_MIN_VAL,
                defaults.TRAIT_MAX_VAL,
            )

            span.set_attribute("points_before", self._points)
            self._points += defaults.POINTS_ADD_WHEN_PLAY
            span.set_attribute("points_after", self._points)

        self._add_action_to_history(action_name)
        log_writer.action_log_info(action_name, self)
        sqlite_db.update_pet(self._session_id, self, defaults.DATABASE_FILE)

        return (
            f"The pet played! "
            f"Current trait values: hunger: {self._hunger},"
            f" energy: {self._energy}, happiness: {self._happiness},"
            f" points: {self._points}"
        )

    @property
    def pet_score(self) -> float:
        """
        The function returns pets weighted score.
        :return: The pets weighted score.
        """
        positive_hunger = defaults.TRAIT_MAX_VAL - self._hunger
        return (positive_hunger + self._energy + self._happiness) / 3

    @property
    def status(self) -> Dict[str, str]:
        """
        The function returns pets status.
        :return: The pet parameters of good condition.
        """
        return {
            "hunger": str(self._hunger),
            "energy": str(self._energy),
            "happiness": str(self._happiness),
            "points": str(self._points),
            "pet_score": str(self.pet_score),
        }

    @property
    def log_file(self) -> str:
        """
        The function returns the log file name.
        :return: The log file name.
        """
        return self._log_file

    @property
    def pet_type(self) -> str:
        """
        The function returns the pet type.
        :return: The pet type.
        """
        return self._pet_type

    @property
    def pet_name(self) -> str:
        """
        The function returns the pet name.
        :return: The pet name.
        """
        return self._name

    @property
    def session_id(self) -> str:
        """
        The function returns the session id.
        :return: The session id of the session the pet belongs to.
        """
        return self._session_id

    def _action_succeeded(self, action_name: str) -> bool:
        """
        The function randomly choose if the action succeeded.
        for highest level the chances for an action to fail is bigger.
        :param action_name: The action that happened.
        :return: If the action failed.
        """
        if random.randrange(0, 6 - self._level) == 2:
            random_number = random.randrange(0, 10)
            if action_name == "eat":
                new_hunger = (
                    self._hunger
                    + defaults.HUNGER_REDUCE_WHEN_EAT[self._level]
                    + random_number
                )
                self._hunger = general_functions.clamp(
                    new_hunger, defaults.TRAIT_MIN_VAL, defaults.TRAIT_MAX_VAL
                )
                log_writer.action_fail_info(action_name,
                                            self._session_id, self)
            elif action_name == "sleep":
                new_energy = (
                    self._energy
                    - defaults.ENERGY_ADD_WHEN_SLEEP[self._level]
                    - random_number
                )
                self._energy = general_functions.clamp(
                    new_energy, defaults.TRAIT_MIN_VAL,
                    defaults.TRAIT_MAX_VAL
                )
                log_writer.action_fail_info(action_name,
                                            self._session_id, self)
            elif action_name == "play":
                new_happiness = (
                    self._happiness
                    - defaults.HAPPINESS_ADD_WHEN_PLAY[self._level]
                    - random_number
                )
                self._happiness = general_functions.clamp(
                    new_happiness, defaults.TRAIT_MIN_VAL,
                    defaults.TRAIT_MAX_VAL
                )
                log_writer.action_fail_info(action_name,
                                            self._session_id, self)
                sqlite_db.update_pet(self._session_id, self, defaults.DATABASE_FILE)
            return False
        return True
