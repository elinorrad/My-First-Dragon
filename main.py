from pet import Pet
from general_functions import *
import log_writer


def create_pet(log_file: str) -> Pet:
    """
    The function creates a new pet.
    :return: The new pet.
    """
    while True:
        print_possible_pet_types()
        try:
            pet_type = int(input("What is your pet type? "))
        except ValueError:
            pet_type = 0
            log_writer.invalid_not_int_error("pet type")
            continue

        if check_pets_type(pet_type):
            break

    log_writer.chose_info("pet type", Pets(pet_type).name.capitalize())
    print("The chosen pet type is " + Pets(pet_type).name.capitalize())

    while True:
        print("One rule for pat name: Pat name can't be empty!")
        pet_name = input("What is your pet name? ")

        if check_pet_name(pet_name):
            break

    log_writer.chose_info("pet name", pet_name)
    print("The chosen pet name is " + pet_name)

    while True:
        print(LEVEL_MSG)
        try:
            level = int(input("Choose a level: "))
            log_writer.chose_info("level", str(level))
        except ValueError:
            level = 0
            log_writer.invalid_not_int_error("level")
            continue

        if check_chosen_level(level):
            break

    try:
        my_pet = Pet(pet_name, Pets(pet_type).name, level, log_file=log_file)
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
        if my_pet.pets_score == 100:
            log_writer.any_info("Win!")
            print("You win!")
            break
        print(MENU_MSG)
        try:
            selection = int(input("What action would you like to do? "))
        except ValueError:
            log_writer.invalid_not_int_error("selection")
            continue
        if selection == Actions.EAT.value:
            my_pet.eat()
        elif selection == Actions.SLEEP.value:
            my_pet.sleep()
        elif selection == Actions.PLAY.value:
            my_pet.play()
        elif selection == Actions.WEIGHTED_SCORE.value:
            pets_score = my_pet.pets_score
            print(pets_score)
            log_writer.any_info(f"Pet score: {pets_score}")
        elif selection == Actions.EXIT.value:
            break
        else:
            log_writer.invalid_error("selection", str(selection))


def main():
    print(WELCOME_MSG)
    log_file = generate_log_file_path()
    log_writer.config_logging(log_file)
    my_pet = create_pet(log_file)
    play(my_pet)


if __name__ == "__main__":
    main()
