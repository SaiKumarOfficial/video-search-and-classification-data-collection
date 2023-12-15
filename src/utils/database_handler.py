from src.constants.database import DATABASE_NAME
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
class MongobdClient:
    client = None

    def __init__(self,database_name= DATABASE_NAME) -> None:
        if MongobdClient.client is None:
            MongobdClient.client = pymongo.MongoClient(
                f"mongodb+srv://{os.environ['CLUSTER_USERNAME']}:{os.environ['CLUSTER_PASSWORD']}@cluster0.edjcajk.mongodb.net"
            )

            self.client = MongobdClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
