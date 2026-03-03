from opentelemetry.trace import Tracer

import defaults
from pet import Pet
import log_writer


def create_pet(pet_type: int, pet_name: str, level: int, log_file: str,
               session_id: str, tracer: Tracer) -> Pet:
    """
    This function creates a pet object.
    :param tracer: The Tracer object to use for this pet.
    :param session_id: The session id the pet belongs to
    :param pet_type: Pet type.
    :param pet_name: Pet name.
    :param level: Level to play with.
    :param log_file: The log file to use.
    :return: The created pet object.
    """
    log_writer.chose_info("pet type",
                          defaults.Pets(pet_type).name.capitalize(),
                          session_id)
    log_writer.chose_info("pet name", pet_name, session_id)
    log_writer.chose_info("level", str(level), session_id)
    my_pet = Pet(pet_name, defaults.Pets(pet_type).name,
                 level, session_id, tracer, log_file=log_file)
    return my_pet
