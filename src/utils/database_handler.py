import pymongo
import os

class MongobdClient:
    client = None

    def __init__(self,database_name= os.environ['DATABASE_NAME']) -> None:
        if MongobdClient.client is None:
            MongobdClient.client = pymongo.MongoClient(
                f"mongobd+srv://{os.environ['CLUSTER_USERNAME']}:{os.environ['CLUSTER_PASSWORD']}@projects.ch4mixt."
            )

            self.client = MongobdClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
    