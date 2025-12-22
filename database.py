"""Database functions for """

from os import environ as ENV, _Environ

from re import match
from bcrypt import gensalt, hashpw, checkpw
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


def get_id_using_email(mongodb_client: MongoClient, email: str) -> str:
    """Returns the Object Id of a user in account table using their email."""

    account_collection = mongodb_client["HabitQuest"]["account"]

    account = account_collection.find_one({"email": email})

    if account:
        return account["_id"]

    return None


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


def create_habit(mongodb_client: MongoClient, description: str, is_good_habit: bool, account_username: str) -> None:
    """Create a single habit with description, whether it is good or bad, and the account to link it to."""
    pass


if __name__ == "__main__":
    load_dotenv()

    client = get_mongodb_client(ENV)
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    create_account(client, "seven@gmail.com", "lll", "yoyo")
