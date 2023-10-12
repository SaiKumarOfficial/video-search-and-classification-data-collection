from src.utils.database_handler import MongobdClient
from src.logger import logging
from src.exception import CustomException
from src.constants.database import COLLECTION_NAME
import os
import sys


class MetaDataStore:
    def __init__(self):
        
        self.videos = os.path.join(os.getcwd(), 'ISRO-documentary')
        self.labels = os.listdir(self.videos)
        self.mongo = MongobdClient()

    def register_labels(self):
        try:

            records = {}
            for num,label in enumerate(self.labels):
                records[f'{num}'] = label
            self.mongo.database[COLLECTION_NAME].insert_one(records)
            logging.info("Inserted successfully")
        except Exception as e:
            raise CustomException(e,sys)
        
    def run_step(self):
        try:
            self.register_labels()
        except Exception as e:
            message =  CustomException(e,sys)
            return {"Created":False,"Reason":message.error_message}
        
if __name__ =="__main__":
    meta = MetaDataStore()
    meta.run_step()
