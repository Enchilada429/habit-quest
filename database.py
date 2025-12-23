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


def get_account_using_email(email: str) -> dict:
    """Returns the account in account table using their email.
    Returns None if it does not exist."""

    with get_mongodb_client(ENV) as client:

        account_collection = client["HabitQuest"]["account"]

        return account_collection.find_one({"email": email})


def get_habit(habit_id: str) -> dict:
    """Returns a habit given its id as a string."""

    with get_mongodb_client(ENV) as client:

        habit_collection = client["HabitQuest"]["habit"]

        habit = habit_collection.find_one({"_id": ObjectId(habit_id)})

        if not habit:
            raise ValueError("Habit not found.")

        return habit


def get_habits(email: str) -> list[dict]:
    """Returns a list of habits for a user via their email."""

    with get_mongodb_client(ENV) as client:

        account = get_account_using_email(email)

        if not account:
            raise ValueError("Email does not link to a valid account.")

        habit_collection = client["HabitQuest"]["habit"]

        return [habit for habit in habit_collection.find({"account_id": account["_id"]})]


def create_account(email: str, password: str, display_name: str) -> dict:
    """Create a HabitQuest account with username, password, and email. Hashes the password.
    Returns new account details as dict. Returns error if email has invalid format."""

    if not match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        raise ValueError("Email has invalid format.")

    with get_mongodb_client(ENV) as client:

        account_collection = client["HabitQuest"]["account"]

        # If email already exists
        if get_account_using_email(email):
            raise ValueError("Email already exists.")

        account_data = {
            "email": email,
            "password": get_hashed_password(password),
            "displayname": display_name
        }

        account_collection.insert_one(account_data)

        return account_data


def create_habit(habit_name: str, habit_type: str, email: str) -> dict:
    """Create a single habit with name, whether it is a good or bad habit, and the email to link it to.
    Returns the habit in dict format."""

    with get_mongodb_client(ENV) as client:

        account = get_account_using_email(email)

        if not account:
            raise ValueError("Email does not link to a valid account.")
        if habit_type.lower() not in ["good", "bad"]:
            raise ValueError("Habit type must be 'good' or 'bad'.")

        habit_collection = client["HabitQuest"]["habit"]

        habit_data = {
            "habit_name": habit_name,
            "habit_type": habit_type.lower(),
            "points": 0,
            "account_id": account["_id"]
        }

        habit_collection.insert_one(habit_data)

        return {key: str(value) for (key, value) in habit_data.items()}


def create_wishlist_entry(name: str, cost: int, email: str) -> dict:
    """Creates an entry in the wishlist table with a name, cost and associated account email.
    Returns the entry in dict format."""

    with get_mongodb_client(ENV) as client:

        account = get_account_using_email(email)

        if not account:
            raise ValueError("Email does not link to a valid account.")
        if not isinstance(cost, int):
            raise ValueError("Cost given is not an integer.")

        wishlist_collection = client["HabitQuest"]["wishlist"]

        wishlist_entry = {
            "name": name,
            "cost": cost,
            "account_id": account["_id"]
        }

        wishlist_collection.insert_one(wishlist_entry)

        return {key: str(value) for (key, value) in wishlist_entry.items()}


def delete_account(account_id: str) -> dict:
    """Deletes an account in the database using its id as a string.
    Returns the deleted account."""

    with get_mongodb_client(ENV) as client:

        account_collection = client["HabitQuest"]["account"]

        deleted = account_collection.find_one_and_delete(
            {"_id": ObjectId(account_id)})

        if not deleted:
            raise ValueError("Invalid habit ID.")

        return deleted


def delete_habit(habit_id: str) -> dict:
    """Deletes a habit in the database using its id as a string.
    Returns the deleted habit."""

    with get_mongodb_client(ENV) as client:

        habit_collection = client["HabitQuest"]["habit"]

        deleted = habit_collection.find_one_and_delete(
            {"_id": ObjectId(habit_id)})

        if not deleted:
            raise ValueError("Invalid habit ID.")

        return deleted


def delete_wishlist_entry(entry_id: str) -> dict:
    """Deletes a wishlist entry in the database using its id as a string.
    Returns the deleted entry."""

    with get_mongodb_client(ENV) as client:

        wishlist_collection = client["HabitQuest"]["wishlist"]

        deleted = wishlist_collection.find_one_and_delete(
            {"_id": ObjectId(entry_id)})

        if not deleted:
            raise ValueError("Invalid habit ID.")

        return deleted


def validate_user(email: str, password: str) -> dict:
    """Checks whether email and password match any accounts in database.
    Returns account if successful."""

    account = get_account_using_email(email)

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

    create_account("example@gmail.com", "example", "example_display_name")
