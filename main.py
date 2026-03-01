from Pet import Pet
from general_functions import *
import log_writer


def create_pet(log_file: str) -> Pet:
    """
    The function creates a new pet.
    :return: The new pet.
    """
    pet_type = ""
    pet_name = "\t"
    level = 0

    while not check_pets_type(pet_type):
        print_possible_pet_types()
        pet_type = input("What is your pet type? ")
    log_writer.pet_type_chose_info(pet_type)
    print("The chosen pet type is " + pet_type)

    while not check_pet_name(pet_name):
        print("One rule for pat name: Pat name can't be empty!")
        pet_name = input("What is your pet name? ")
    log_writer.pet_name_chose_info(pet_name)
    print("The chosen pet name is " + pet_name)

    while not check_chosen_level(level):
        print(LEVEL_MSG)
        try:
            level = int(input("Choose a level: "))
            log_writer.level_chose_info(level)
        except ValueError:
            level = 0
            log_writer.invalid_level_not_int_error()
    try:
        my_pet = Pet(pet_name, pet_type, level, log_file=log_file)
        return my_pet
    except ValueError as e:
        print(e)
        print("Now try again!")
        return create_pet(log_file)


def play(my_pet: Pet) -> None:
    """
    The function plays the chosen pet.
    :param my_pet: The pet to play with.
    :return: None.
    """
    while True:
        if my_pet.get_pets_score == 100:
            log_writer.win_info()
            print("You win!")
            break
        print(MENU_MSG)
        try:
            selection = int(input("What action would you like to do? "))
        except ValueError:
            log_writer.invalid_selection_not_int_error()
            continue
        if selection == Actions.EAT.value:
            my_pet.eat()
        elif selection == Actions.SLEEP.value:
            my_pet.sleep()
        elif selection == Actions.PLAY.value:
            my_pet.play()
        elif selection == Actions.WEIGHTED_SCORE.value:
            print(my_pet.get_pets_score)
        elif selection == Actions.EXIT.value:
            break
        else:
            log_writer.invalid_selection_error(selection)


def main():
    print(WELCOME_MSG)
    log_file = generate_log_file_path()
    log_writer.config_logging(log_file)
    my_pet = create_pet(log_file)
    play(my_pet)


if __name__ == "__main__":
    main()
