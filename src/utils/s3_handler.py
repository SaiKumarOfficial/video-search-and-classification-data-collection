import boto3
import os,sys
import boto3.session
from typing import Dict       
from src.utils.utils import video_unique_name
from src.exception import CustomException
from dotenv import load_dotenv
load_dotenv()
class S3Connection:
    def __init__(self):
        session = boto3.Session(
            aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY']

        )
        self.s3 = session.resource("s3")
        self.bucket = self.s3.Bucket(os.environ['AWS_BUCKET_NAME'])

    def add_label(self,label:str) ->Dict:

        try:
            key = f"videos/{label}/"
            response = self.bucket.put_object(Body="",Key = key)
            return {"Created":True,"Path":response.key}
        except Exception as e:
            message = CustomException(e,sys)
            return {"Created":False, "Reason":message.error_message}
        

    def upload_to_s3(self,video_path, label:str):

        try:
            self.bucket.upload_fileobj(
                video_path,
                f"videos/{label}/{video_unique_name()}.mp4",
                ExtraArgs = {'ACL':"public-read"},
            )
            return {"Created":True}
        except Exception as e:
            message = CustomException(e,sys)
            return {"Created":False, "Reason":message.error_message}
        

        