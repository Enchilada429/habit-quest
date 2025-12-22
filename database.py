from os import environ as ENV, _Environ

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv


def get_mongodb_client(config: _Environ) -> MongoClient:
    """Returns a MongoDB client for the HabitQuestCluster."""
    return MongoClient(
        f"mongodb+srv://{config["DB_USERNAME"]}:{config["DB_PASSWORD"]}@habitquestcluster.dwoqkpl.mongodb.net/?appName=HabitQuestCluster",
        server_api=ServerApi('1')
    )


if __name__ == "__main__":
    load_dotenv()

    # Send a ping to confirm a successful connection
    try:
        client = get_mongodb_client(ENV)
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
