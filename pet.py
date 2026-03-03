import random
from typing import Tuple, List, Dict

from general_functions import *
import log_writer


class Pet:
    def __init__(
        self,
        name: str,
        pet_type: str,
        level: int,
        hunger: int = DEFAULT_HUNGER,
        happiness: int = DEFAULT_HAPPINESS,
        energy: int = DEFAULT_ENERGY,
        points: int = DEFAULT_POINTS,
        log_file: str = DEFAULT_LOG_FILE,
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
        check_pet_params(hunger, happiness, energy)
        self._name = name
        self._pet_type = pet_type
        self._level = level
        self._hunger = hunger
        self._happiness = happiness
        self._energy = energy
        self._points = points
        self._log_file = log_file
        self._history: list = []
        log_writer.new_pet_log_info(name, pet_type, hunger, happiness, energy, points)

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

        if self._hunger - HUNGER_REDUCE_WHEN_EAT[self._level] < TRAIT_MIN_VAL:
            self._hunger = TRAIT_MIN_VAL
        else:
            self._hunger -= HUNGER_REDUCE_WHEN_EAT[self._level]

        if self._energy + ENERGY_ADD_WHEN_EAT[self._level] > TRAIT_MAX_VAL:
            self._energy = TRAIT_MAX_VAL
        else:
            self._energy += ENERGY_ADD_WHEN_EAT[self._level]

        self._points += POINTS_ADD_WHEN_EAT

        self._add_action_to_history(action_name)
        log_writer.action_log_info(action_name)

        print(
            "The pet ate!",
            f"Current trait values: hunger: {self._hunger},"
            f" energy: {self._energy}, happiness: {self._happiness},"
            f" points: {self._points}",
        )

        is_failed = self._action_didnt_succeeded("eat")
        if is_failed:
            return "ughhh the pet vomit"
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

        if self._hunger + HUNGER_ADD_WHEN_SLEEP[self._level] > TRAIT_MAX_VAL:
            self._hunger = TRAIT_MAX_VAL
        else:
            self._hunger += HUNGER_ADD_WHEN_SLEEP[self._level]

        if self._energy + ENERGY_ADD_WHEN_SLEEP[self._level] > TRAIT_MAX_VAL:
            self._energy = TRAIT_MAX_VAL
        else:
            self._energy += ENERGY_ADD_WHEN_SLEEP[self._level]

        self._points += POINTS_ADD_WHEN_SLEEP

        self._add_action_to_history(action_name)
        log_writer.action_log_info(action_name)

        print(
            "The pet slept!",
            f"Current trait values: hunger: {self._hunger},"
            f" energy: {self._energy}, happiness: {self._happiness},"
            f" points: {self._points}",
        )

        is_failed = self._action_didnt_succeeded("sleep")
        if is_failed:
            return "ughhh I slept so bad!! I just more tired now"
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

        if self._energy - ENERGY_REDUCE_WHEN_PLAY[self._level] < TRAIT_MIN_VAL:
            self._energy = TRAIT_MIN_VAL
        else:
            self._energy -= ENERGY_REDUCE_WHEN_PLAY[self._level]

        if self._happiness + HAPPINESS_ADD_WHEN_PLAY[self._level] > TRAIT_MAX_VAL:
            self._happiness = TRAIT_MAX_VAL
        else:
            self._happiness += HAPPINESS_ADD_WHEN_PLAY[self._level]

        self._points += POINTS_ADD_WHEN_PLAY

        self._add_action_to_history(action_name)
        log_writer.action_log_info(action_name)

        print(
            "The pet played! ",
            f"Current trait values: hunger: {self._hunger},"
            f" energy: {self._energy}, happiness: {self._happiness},"
            f" points: {self._points}",
        )

        is_failed = self._action_didnt_succeeded("play")
        if is_failed:
            return "ughhh I didnt like the play at all! Now I am not happy at all."
        else:
            return (
                f"The pet played! "
                f"Current trait values: hunger: {self._hunger},"
                f" energy: {self._energy}, happiness: {self._happiness},"
                f" points: {self._points}"
            )

    @property
    def pets_score(self) -> float:
        """
        The function returns pets weighted score.
        :return: The pets weighted score.
        """
        positive_hunger = TRAIT_MAX_VAL - self._hunger
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
            "pets_score": str(self.pets_score),
        }

    def _action_didnt_succeeded(self, action_name: str) -> bool:
        """
        The function randomly choose if the action succeeded.
        for highst level the chances for an action to fail is bigger.
        :param action_name: The acction that happend.
        :return: If the action failed.
        """
        if random.randrange(0, 6 - self._level) == 2:
            random_number = random.randrange(0, 10)
            if action_name == "eat":
                if (
                    self._hunger + HUNGER_REDUCE_WHEN_EAT[self._level] + random_number
                    > TRAIT_MAX_VAL
                ):
                    self._hunger += HUNGER_REDUCE_WHEN_EAT[self._level] + random_number
                else:
                    self._hunger = TRAIT_MAX_VAL
                print("ughhh the pet vomit")
                log_writer.action_fail_info(action_name)
            elif action_name == "sleep":
                if (
                    self._energy - ENERGY_ADD_WHEN_SLEEP[self._level] - random_number
                    < TRAIT_MIN_VAL
                ):
                    self._energy -= ENERGY_ADD_WHEN_SLEEP[self._level] - random_number
                else:
                    self._energy -= TRAIT_MIN_VAL
                print("ughhh I slept so bad!! I just more tired now")
                log_writer.action_fail_info(action_name)
            elif action_name == "play":
                if (
                    self._happiness
                    - HAPPINESS_ADD_WHEN_PLAY[self._level]
                    - random_number
                    < TRAIT_MIN_VAL
                ):
                    self._happiness -= (
                        HAPPINESS_ADD_WHEN_PLAY[self._level] - random_number
                    )
                else:
                    self._happiness -= TRAIT_MIN_VAL
                print(
                    "ughhh I didnt like the play at all!" " Now I am not happy at all."
                )
                log_writer.action_fail_info(action_name)
            return True
        return False
