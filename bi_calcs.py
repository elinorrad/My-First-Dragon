import ast
from datetime import datetime, timedelta
import defaults
import pet


def status_dict(action_data: str) -> dict:
    """
    The function return the status as a dict.
    :param action_data: The data of the action that
     includes the status dict in it.
    :return: The status as a dict.
    """
    return ast.literal_eval(action_data
                            [action_data.find('{'):action_data.find('}') + 1])


def happy_hour(actions: list) -> tuple:
    """
    The function return the hour when happiness value was the highest.
    :param actions: All the actions that have been done.
    :return: The hour when happiness value was the highest and the value.
    """
    most_happy_value = defaults.DEFAULT_HAPPINESS
    most_happy_hour = datetime.now().strftime("%d-%b-%y %H:%M:%S")
    for action in actions:
        if "failed" not in action['data']:
            happiness = status_dict(action['data'])['happiness']
            if int(happiness) > most_happy_value:
                most_happy_value = int(happiness)
                most_happy_hour = action['timestamp']
    return most_happy_hour, most_happy_value


def common_action(actions: list) -> tuple:
    """
    The function return the action that was used the most.
    :param actions: All the actions that have been done.
    :return: The action that was used the most and the value.
    """
    most_common_action = ""
    most_common_amount = 0
    actions_count = {k: 0 for k in [action.name.lower()
                                    for action in defaults.Actions]}
    for action in actions:
        if "failed" not in action['data']:
            actions_count[action['data'].split()
                                [defaults.DEFAULT_ACTION_INDEX_IN_DATA]] += 1
    for action_type, amount in actions_count.items():
        if amount > most_common_amount:
            most_common_amount = amount
            most_common_action = action_type
    return most_common_action, most_common_amount


def happiness_average(actions: list, my_pet: pet.Pet) -> float:
    """
    The function return the average happiness value.
    :param my_pet: The pet the average checked on.
    :param actions: All the actions that have been done.
    :return: The average happiness value.
    """
    happiness_sum = 0
    happiness_amount = 0
    if not actions:
        return float(my_pet.status['happiness'])
    for action in actions:
        happiness = status_dict(action['data'])['happiness']
        happiness_sum += int(happiness)
        happiness_amount += 1
    return happiness_sum / happiness_amount


def actions_per_day(actions: list) -> dict:
    """
    The function return the actions per day.
    :param actions: All the actions that have been done.
    :return: The actions per day.
    """
    if not actions:
        return {}
    possible_dates = {k: 0 for k in [action['timestamp']
                                     .split(' ')[0] for action in actions]}
    for action in actions:
        possible_dates[action['timestamp'].split(' ')[0]] += 1
    return possible_dates


def average_time_between_actions(actions: list) -> timedelta:
    """
    The function return the average time between actions.
    :param actions: All the actions that have been done.
    :return: The average time between actions.
    """
    sum_time = timedelta()
    if not actions:
        return sum_time
    for i in range(1, len(actions)):
        sum_time += (datetime.strptime(actions[i]['timestamp'],
                                       "%d-%b-%y %H:%M:%S") -
                     datetime.strptime(actions[i-1]['timestamp'],
                                       "%d-%b-%y %H:%M:%S"))

    return sum_time / len(actions)
