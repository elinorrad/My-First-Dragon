import uuid
from typing import Union
from werkzeug import Response
import app_service
import backend_main
from flask import render_template, request, current_app, redirect, session
import bi_calcs
import general_functions
import log_writer
from pet import Pet


app = app_service.create_app()


def check_if_user_connected() -> None:
    """
    The function checks if users session exist and if not its creates one.
    :return: None.
    """
    if "id" not in session:
        session["id"] = str(uuid.uuid4())
        app.config["IS_ANIMAL_CREATED"][session["id"]] = False


def my_pet() -> Pet:
    """
    The function return the pet object by user's session.
    :return: The pet object by user's session.
    """
    return app.config["USER_TO_PET"][session["id"]]


@app.route("/create_animal", methods=["GET", "POST"])
def post_create_animal() -> Union[str, Response]:
    """
    This is the create animal page.
    :return: The create animal page.
    """
    if request.method == "POST":
        pet_type = request.form.get("pet_type")
        pet_name = request.form.get("pet_name")
        level = request.form.get("level")
        error = general_functions.check_create_pet_params(
            str(pet_type), str(pet_name), str(level), str(session.get("id")))
    else:
        return render_template(
            "create_animal.html",
            possible_pets=app.config["POSSIBLE_PETS"],
            possible_levels=app.config["POSSIBLE_LEVELS"],
        )

    if error != "":
        return render_template(
            "create_animal.html",
            possible_pets=app.config["POSSIBLE_PETS"],
            possible_levels=app.config["POSSIBLE_LEVELS"],
            error=error,
        )
    else:
        try:
            app.config["USER_TO_PET"][session["id"]] = backend_main.create_pet(
                int(str(pet_type)), str(pet_name),
                int(str(level)), app.config["LOG_FILE"], str(session.get("id"))
            )
        except ValueError as e:
            return render_template(
                "create_animal.html",
                possible_pets=app.config["POSSIBLE_PETS"],
                possible_levels=app.config["POSSIBLE_LEVELS"],
                error=str(e),
            )
        app.config["POSSIBLE_ACTIONS"][session["id"]] = {
            "eat": my_pet().eat,
            "sleep": my_pet().sleep,
            "play": my_pet().play,
        }
        app.config["IS_ANIMAL_CREATED"][session["id"]] = True
        return redirect("/")


@app.route("/")
def home() -> Union[Response, str]:
    """
    This is the home page
    :return: The home page
    """
    check_if_user_connected()
    if not app.config["IS_ANIMAL_CREATED"][session["id"]]:
        return redirect("/create_animal")
    return render_template("home_page.html")


@app.route("/status")
def status() -> Union[Response, str]:
    """
    This is the status page
    :return: The status page
    """
    check_if_user_connected()
    if not app.config["IS_ANIMAL_CREATED"][session["id"]]:
        return redirect("/create_animal")
    return render_template("status_page.html", data=my_pet().status)


@app.route("/action")
def action() -> Union[Response, str]:
    """
    This is the action page
    :return: The action page
    """
    check_if_user_connected()
    if not app.config["IS_ANIMAL_CREATED"][session["id"]]:
        return redirect("/create_animal")
    return render_template(
        "action_page.html", image=app_service.pet_image(my_pet().pet_type))


@app.post("/action/<chosen_action>")
def post_action(chosen_action: str) -> Union[Response, str]:
    """
    This is the post action to pet request.
    :param chosen_action: The chosen action.
    :return: The action page with message.
    """
    check_if_user_connected()
    if not app.config["IS_ANIMAL_CREATED"][session["id"]]:
        return redirect("/create_animal")
    output = ""
    if chosen_action in current_app.config["POSSIBLE_ACTIONS"][session["id"]]:
        output = (
            current_app.config["POSSIBLE_ACTIONS"][session["id"]][chosen_action]())
    return render_template(
        "action_page.html",
        output=output,
        image=app_service.pet_image(my_pet().pet_type),
        rain=chosen_action,
    )


@app.route("/bi")
def bi() -> Union[Response, str]:
    """
    This is the bi page
    :return: The bi page
    """
    check_if_user_connected()
    if not app.config["IS_ANIMAL_CREATED"][session["id"]]:
        return redirect("/create_animal")
    actions = app_service.actions_by_session(my_pet().log_file, session["id"])
    happiest_hour, happiest_value = bi_calcs.happy_hour(actions)
    most_common_action, most_common_action_amount =\
        bi_calcs.common_action(actions)
    happiness_average_value = bi_calcs.happiness_average(actions, my_pet())
    actions_per_date = bi_calcs.actions_per_day(actions)
    average_time_between_actions =\
        bi_calcs.average_time_between_actions(actions)
    return render_template("bi_page.html", happiest_hour=happiest_hour,
                           happiest_value=happiest_value,
                           most_common_action=most_common_action,
                           most_common_action_amount=most_common_action_amount,
                           happiness_average_value=happiness_average_value,
                           actions_per_date=actions_per_date,
                           average_time_between_actions=average_time_between_actions)


def main():
    log_writer.config_logging(app.config["LOG_FILE"])
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
