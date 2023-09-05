import os,sys
from zipfile import ZipFile
import shutil
from src.logger import logging
from src.exception import CustomException

class DataStore:
    def __init__(self):
        self.root = os.path.join(os.getcwd(),"data")
        self.zip = os.path.join(self.root, "archive.zip")
        self.videos = os.path.join(self.root, "ISRO-documentry")
        self.list_unwanted = ["BACKGROUND_Google"]
    def prepare_data(self):
        try:

            logging.info("Extracting Data")
            with ZipFile(self.zip, "r") as files:
                files.extractall(path= self.root)
            files.close()
            logging.info("Process Completed")

        except Exception as e:
            message = CustomException(e,sys)
            return {"Created":False, "Reason":message.error_message}
        
    def remove_unwanted_classes(self):
        try:
            logging.info("Removing unwanted classes")
            for label in self.list_unwanted:
                path = os.path.join(self.images,label)
                shutil.rmtree(path,ignore_errors=True)

            logging.info("Process Completed")

        except Exception as e:
            message = CustomException(e,sys)
            return {"Created":False, "Reason":message.error_message}
        
    def sync_data(self):
        try:
            pass
        except Exception as e:
            message = CustomException(e,sys)
            return {"Created":False, "Reason":message.error_message}
        
    def run_step(self):
        try:
            self.prepare_data()
            self.remove_unwanted_classes()
            self.sync_data()
        except Exception as e:
            message = CustomException(e,sys)
            return {"Created":False, "Reason":message.error_message}

    

if __name__=="__main__":
    store = DataStore()
    store.run_step()