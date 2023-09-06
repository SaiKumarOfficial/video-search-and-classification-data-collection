import os,sys
from zipfile import ZipFile
import shutil
import subprocess
from src.logger import logging
from src.exception import CustomException
from src.constants.database import AWS_BUCKET_NAME


class DataStore:
    def __init__(self):
        self.videos = os.path.join(os.getcwd(), "ISRO-documentary")
        # self.list_unwanted = ["BACKGROUND_Google"]
        self.bucket_name = AWS_BUCKET_NAME
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
        
    # def remove_unwanted_classes(self):
    #     try:
    #         logging.info("Removing unwanted classes")
    #         for label in self.list_unwanted:
    #             path = os.path.join(self.images,label)
    #             shutil.rmtree(path,ignore_errors=True)

    #         logging.info("Process Completed")

        except Exception as e:
            message = CustomException(e,sys)
            return {"Created":False, "Reason":message.error_message}
        
    def sync_data(self):
        try:
            if os.path.exists(self.videos):
                logging.info("================= Starting Data sync =================")
                command = f'aws s3 sync "{self.videos}"  s3://isro-documentary-videos/videos/'

                # Use subprocess.run to execute the command
                subprocess.run(command, shell=True)
                # os.system(f"aws s3 sync {self.videos} s3://{self.bucket_name}/videos/")
                logging.info("================= Data sync Completed =================")
        except Exception as e:
            message = CustomException(e,sys)
            return {"Created":False, "Reason":message.error_message}
        
    def run_step(self):
        try:
            # self.prepare_data()
            # self.remove_unwanted_classes()
            self.sync_data()
        except Exception as e:
            message = CustomException(e,sys)
            return {"Created":False, "Reason":message.error_message}

    

if __name__=="__main__":
    store = DataStore()
    store.run_step()