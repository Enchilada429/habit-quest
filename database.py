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


def create_account(mongodb_client: MongoClient, username: str, password: str, email: str) -> None:
    """Create a HabitQuest account with username, password, and email. Hashes the password.
    Returns error if email has invalid format."""

    if not match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        raise ValueError("Email has invalid format.")

    account_collection = mongodb_client["HabitQuest"]["account"]

    account_collection.insert_one({
        "username": username,
        "password": get_hashed_password(password),
        "email": email
    })


if __name__ == "__main__":
    load_dotenv()

    client = get_mongodb_client(ENV)
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    create_account(client, "omar", "yahya", "anotherexample@gmail.com")
