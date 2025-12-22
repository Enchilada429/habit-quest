"""Database functions for """

from os import environ as ENV, _Environ

from re import match
from bcrypt import gensalt, hashpw, checkpw
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv


def get_mongodb_client(config: _Environ) -> MongoClient:
    """Returns a MongoDB client for the HabitQuestCluster."""
    return MongoClient(
        f"mongodb+srv://{config["DB_USERNAME"]}:{config["DB_PASSWORD"]}@habitquestcluster.dwoqkpl.mongodb.net/?appName=HabitQuestCluster",
        server_api=ServerApi('1')
    )


def get_hashed_password(password: str) -> str:
    """Returns a hashed password from a given password."""
    return hashpw(bytes(password, "utf-8"), gensalt())


def get_id_using_email(mongodb_client: MongoClient, email: str) -> ObjectId:
    """Returns the Object Id of a user in account table using their email."""

    account_collection = mongodb_client["HabitQuest"]["account"]

    account = account_collection.find_one({"email": email})

    if account:
        return account["_id"]

    return None


def get_habits(mongodb_client: MongoClient, email: str) -> list[dict]:
    """Returns a list of habits for a user via their email."""

    account_id = get_id_using_email(mongodb_client, email)

    if not account_id:
        raise ValueError("Email does not link to a valid account.")

    habit_collection = mongodb_client["HabitQuest"]["habit"]

    return [habit for habit in habit_collection.find({"account_id": account_id})]


def create_account(mongodb_client: MongoClient, email: str, password: str, display_name: str) -> None:
    """Create a HabitQuest account with username, password, and email. Hashes the password.
    Returns error if email has invalid format."""

    if not match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        raise ValueError("Email has invalid format.")

    account_collection = mongodb_client["HabitQuest"]["account"]

    # If email already exists
    if get_id_using_email(client, email) is not None:
        raise ValueError("Email already exists.")

    account_collection.insert_one({
        "email": email,
        "password": get_hashed_password(password),
        "displayname": display_name
    })


def create_habit(mongodb_client: MongoClient, description: str, habit_type: str, email: str) -> None:
    """Create a single habit with description, whether it is a good or bad habit, and the email to link it to."""

    account_id = get_id_using_email(mongodb_client, email)

    if not account_id:
        raise ValueError("Email does not link to a valid account.")
    if habit_type.lower() not in ["good", "bad"]:
        raise ValueError("Habit type must be 'good' or 'bad'.")

    habit_collection = mongodb_client["HabitQuest"]["habit"]

    habit_collection.insert_one({
        "description": description,
        "habit_type": habit_type.lower(),
        "account_id": account_id
    })


def delete_account(mongodb_client: MongoClient, account_id: str) -> dict:
    """Deletes an account in the database using its id as a string.
    Returns the deleted account."""

    account_collection = mongodb_client["HabitQuest"]["account"]

    deleted = account_collection.find_one_and_delete(
        {"_id": ObjectId(account_id)})

    if not deleted:
        raise ValueError("Invalid habit ID.")

    return deleted


def delete_habit(mongodb_client: MongoClient, habit_id: str) -> dict:
    """Deletes a habit in the database using its id as a string.
    Returns the deleted habit."""

    habit_collection = mongodb_client["HabitQuest"]["habit"]

    deleted = habit_collection.find_one_and_delete({"_id": ObjectId(habit_id)})

    if not deleted:
        raise ValueError("Invalid habit ID.")

    return deleted


if __name__ == "__main__":
    load_dotenv()

    client = get_mongodb_client(ENV)
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    print(delete_account(client, "69495e0c4683ee94e55e3d45"))
