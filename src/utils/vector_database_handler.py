from src.constants.database import CLASS_NAME,CLIENT_URL
from src.exception import CustomException
from src.logger import logging
import weaviate
import base64
import os,sys
from typing import Dict


class WeaviateClient:
    client = None
    def __init__(self,classname = CLASS_NAME):
        self.client = weaviate.Client(CLIENT_URL,)
        self.classname = classname

    def create_class(self,schemaConfig: Dict):
        try:
            self.client.schema.create_class(schemaConfig)
            logging.info(f"{schemaConfig['class']} class Created Successfully!!")
        except Exception as e:
            message = CustomException(e,sys)
            return {"Created":False,"Response":message.error_message}
        
    

        