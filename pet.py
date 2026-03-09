import random
from typing import Dict
import general_functions
import log_writer
import defaults


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
        log_file: str = defaults.DEFAULT_LOG_FILE,
    ) -> None:
        """
        The constructor for Pet.
        :param name: The name of the pet.
        :param pet_type: The type of pet.
        :param hunger: The initial hunger of the pet.
        :param happiness: The initial happiness of the pet.
        :param energy: The initial energy of the pet.
        :param points: The initial points of the pet.
        :return: None.
        """
        general_functions.check_pet_params(hunger, happiness,
                                           energy, session_id)
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
        log_writer.new_pet_log_info(name, pet_type, hunger,
                                    happiness, energy, points,
                                    self._session_id)

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

        if (
            self._hunger - defaults.HUNGER_REDUCE_WHEN_EAT[self._level]
            < defaults.TRAIT_MIN_VAL
        ):
            self._hunger = defaults.TRAIT_MIN_VAL
        else:
            self._hunger -= defaults.HUNGER_REDUCE_WHEN_EAT[self._level]

        if (
            self._energy + defaults.ENERGY_ADD_WHEN_EAT[self._level]
            > defaults.TRAIT_MAX_VAL
        ):
            self._energy = defaults.TRAIT_MAX_VAL
        else:
            self._energy += defaults.ENERGY_ADD_WHEN_EAT[self._level]

        self._points += defaults.POINTS_ADD_WHEN_EAT

        self._add_action_to_history(action_name)
        log_writer.action_log_info(action_name, self)

        is_succeeded = self._action_succeeded("eat")
        if not is_succeeded:
            return "ughhh the pet vomited"
        else:
            return (
                f"The pet ate! "
                f"Current trait values: hunger: {self._hunger},"
                f" energy: {self._energy}, happiness: {self._happiness},"
                f" points: {self._points}"
            )

    def sleep(self) -> str:
        """
        The function for the pet to sleep.
        :return: a success or fail message.
        """

        action_name = "sleep"

        if (
            self._hunger + defaults.HUNGER_ADD_WHEN_SLEEP[self._level]
            > defaults.TRAIT_MAX_VAL
        ):
            self._hunger = defaults.TRAIT_MAX_VAL
        else:
            self._hunger += defaults.HUNGER_ADD_WHEN_SLEEP[self._level]

        if (
            self._energy + defaults.ENERGY_ADD_WHEN_SLEEP[self._level]
            > defaults.TRAIT_MAX_VAL
        ):
            self._energy = defaults.TRAIT_MAX_VAL
        else:
            self._energy += defaults.ENERGY_ADD_WHEN_SLEEP[self._level]

        self._points += defaults.POINTS_ADD_WHEN_SLEEP

        self._add_action_to_history(action_name)
        log_writer.action_log_info(action_name, self)

        is_succeeded = self._action_succeeded("sleep")
        if not is_succeeded:
            return "ughhh I slept so bad!! I am just more tired now"
        else:
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

        if (
            self._energy - defaults.ENERGY_REDUCE_WHEN_PLAY[self._level]
            < defaults.TRAIT_MIN_VAL
        ):
            self._energy = defaults.TRAIT_MIN_VAL
        else:
            self._energy -= defaults.ENERGY_REDUCE_WHEN_PLAY[self._level]

        if (
            self._happiness + defaults.HAPPINESS_ADD_WHEN_PLAY[self._level]
            > defaults.TRAIT_MAX_VAL
        ):
            self._happiness = defaults.TRAIT_MAX_VAL
        else:
            self._happiness += defaults.HAPPINESS_ADD_WHEN_PLAY[self._level]

        self._points += defaults.POINTS_ADD_WHEN_PLAY

        self._add_action_to_history(action_name)
        log_writer.action_log_info(action_name, self)

        is_succeeded = self._action_succeeded("play")
        if not is_succeeded:
            return "ughhh I didn't like the play at all!"\
                   " Now I am not happy at all."
        else:
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
            return False
        return True
