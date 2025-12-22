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


def get_hashed_password(password: str) -> bytes:
    """Returns a hashed password from a given password."""
    return hashpw(bytes(password, "utf-8"), gensalt())


def get_account_using_email(mongodb_client: MongoClient, email: str) -> dict:
    """Returns the account in account table using their email.
    Returns None if it does not exist."""

    account_collection = mongodb_client["HabitQuest"]["account"]

    return account_collection.find_one({"email": email})


def get_habit(mongodb_client: MongoClient, habit_id: str) -> dict:
    """Returns a habit given its id as a string."""

    habit_collection = mongodb_client["HabitQuest"]["habit"]

    habit = habit_collection.find_one({"_id": ObjectId(habit_id)})

    if not habit:
        raise ValueError("Habit not found.")

    return habit


def get_habits(mongodb_client: MongoClient, email: str) -> list[dict]:
    """Returns a list of habits for a user via their email."""

    account = get_account_using_email(mongodb_client, email)

    if not account:
        raise ValueError("Email does not link to a valid account.")

    habit_collection = mongodb_client["HabitQuest"]["habit"]

    return [habit for habit in habit_collection.find({"account_id": account["_id"]})]


def create_account(mongodb_client: MongoClient, email: str, password: str, display_name: str) -> None:
    """Create a HabitQuest account with username, password, and email. Hashes the password.
    Returns error if email has invalid format."""

    if not match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        raise ValueError("Email has invalid format.")

    account_collection = mongodb_client["HabitQuest"]["account"]

    # If email already exists
    if get_account_using_email(client, email):
        raise ValueError("Email already exists.")

    account_collection.insert_one({
        "email": email,
        "password": get_hashed_password(password),
        "displayname": display_name
    })


def create_habit(mongodb_client: MongoClient, description: str, habit_type: str, email: str) -> None:
    """Create a single habit with description, whether it is a good or bad habit, and the email to link it to."""

    account = get_account_using_email(mongodb_client, email)

    if not account:
        raise ValueError("Email does not link to a valid account.")
    if habit_type.lower() not in ["good", "bad"]:
        raise ValueError("Habit type must be 'good' or 'bad'.")

    habit_collection = mongodb_client["HabitQuest"]["habit"]

    habit_collection.insert_one({
        "description": description,
        "habit_type": habit_type.lower(),
        "account_id": account["_id"]
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


def validate_user(mongodb_client: MongoClient, email: str, password: str) -> dict:
    """Checks whether email and password match any accounts in database.
    Returns account if successful."""

    account = get_account_using_email(mongodb_client, email)

    if not account:
        raise ValueError("Email does not exist in account database.")

    valid = checkpw(bytes(password, "utf-8"), account["password"])

    if not valid:
        raise ValueError("Given password does not match account password.")

    return account


if __name__ == "__main__":
    load_dotenv()

    client = get_mongodb_client(ENV)
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    print(validate_user(client, "anotherexample@gmail.com", "yahya"))
