import sqlite3
import pickle
from typing import Union



def get_db(database: str) -> sqlite3.Connection:
    """
    This function creates a new database connection to a SQLite database
    :param database: The name of the database
    :return: The SQLite database connection
    """
    return sqlite3.connect(database)


def init_db(database: str) -> None:
    """
    The function creates the pet table in the database.
    :param database: The name of the database
    :return: None.
    """
    db = get_db(database)
    db.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            session_id TEXT PRIMARY KEY,
            pet_object TEXT
        )
    """)
    db.commit()


def save_pet(session_id: str, pet_object, database: str) -> None:
    """
    The function saves a pet object in the database.
    :param session_id: The session id.
    :param pet_object: The pet object.
    :param database: The name of the database.
    :return: None.
    """
    db = get_db(database)
    pet_object_binary = pickle.dumps(pet_object)
    db.execute("INSERT INTO pets (session_id, pet_object) VALUES (?, ?)",
            (session_id, pet_object_binary)
        )
    db.commit()


def get_pet(session_id: str, database: str):
    """
    The function gets a pet object from the database.
    :param session_id: The session id to get the pet object.
    :param database: The name of the database.
    :return: None.
    """
    db = get_db(database)
    row = db.execute("SELECT pet_object FROM pets WHERE session_id = ?",
                     (session_id,)).fetchone()
    if row is None:
        return None

    pet_object = pickle.loads(row[0])
    return pet_object


def update_pet(session_id: str, pet_object, database: str) -> None:
    """
    The function updates a pet object in the database.
    :param session_id: The session id.
    :param pet_object: The pet object.
    :param database: The name of the database.
    :return: None.
    """
    db = get_db(database)
    pet_object_binary = pickle.dumps(pet_object)
    db.execute("UPDATE pets SET pet_object = ? WHERE session_id = ?",
               (pet_object_binary, session_id)).fetchone()
    db.commit()
