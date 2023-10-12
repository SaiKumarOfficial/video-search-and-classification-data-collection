from src.utils.vector_database_handler import WeaviateClient
from src.utils.s3_handler import S3Connection
from src.utils.utils import video_unique_name
from src.exception import CustomException
from src.constants.database import AWS_BUCKET_NAME,BATCH_SIZE,CLASS_NAME,SCHEMA_CONFIG
from src.logger import logging
from moviepy.editor import VideoFileClip
import os, sys
import base64
import boto3
import numpy as np
import cv2


class WeaviateDataStore:
    def __init__(self):

        self.videos = os.path.join(os.getcwd(), 'ISRO-documentary')
        self.labels = os.listdir(self.videos)

        self.s3 = S3Connection()
        self.s3client = boto3.client('s3')

        self.video_urls = []
        self.video_file_names = []
        self.video_labels = []

        
    def list_public_video_urls_filenames_labels(self,bucket_name):
        try:
            logging.info("Connecting to the s3 and getting data")
            bucket = self.s3.bucket
            objects = iter(bucket.objects.all())
            next(objects)
            for obj in objects:
                parts = obj.key.split('/')
                self.video_file_names.append(parts[-1])
                self.video_labels.append(parts[1])
                video_url = self.s3client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name, 'Key': obj.key},
                                                    ExpiresIn=None)  # URL expires in 1 hour
                self.video_urls.append(video_url)
            logging.info("Successfully get the data from s3")

            return self.video_file_names,self.video_labels,self.video_urls
        except Exception as e:
            message = CustomException(e,sys)
            return {"GetPublicURL":False,"message":message.error_message}
    def get_frames(self,video_file_path):
        logging.info(f"Extracting the frames from the {video_file_path}")
        video = VideoFileClip(video_file_path)

        base_name = os.path.basename(video_file_path)
        filename, extension = os.path.splitext(base_name)
        duration = video.duration
        # Extract 20 frames from the whole video
        frames = [video.get_frame(t) for t in np.linspace(0, duration, 20)]
        base64_frames = []
        frame_names = []
        for i,frame in enumerate(frames):
            base64_frames.append(base64.b64encode(frame).decode('utf-8'))
            frame_name = video_unique_name(filename,i+1)
            frame_names.append(frame_name)
        logging.info("Extracted successfully...!")
        return base64_frames,frame_names

    def create_data(self):
        try:
            video_file_names, video_labels, video_urls = self.list_public_video_urls_filenames_labels(bucket_name=AWS_BUCKET_NAME)
            # Store the data
            video_file_paths = {}
            logging.info("Getting video file paths....")
            # Loop through video directories and files
            for root, _, files in os.walk(self.videos):
                for file_name in files:
                    if file_name in video_file_names:
                        video_file_path = os.path.join(root, file_name)
                        video_file_paths[file_name] = video_file_path

            logging.info("Create and store dictionaries with video data")
            video_data_list = []
            for video_filename, video_path in video_file_paths.items():
                base64_frames, frame_names = self.get_frames(video_path)
                for i in range(len(frame_names)):

                    video_data = {
                        'image': base64_frames[i],
                        'Frame_Name': frame_names[i],
                        'Video_File_Name': video_filename,
                        'Video_URL': video_urls[video_file_names.index(video_filename)],
                        'Label': video_labels[video_file_names.index(video_filename)],
                    }
                    video_data_list.append(video_data)

            logging.info("Successfully return the video data!!")   
        except Exception as e:
            message = CustomException(e,sys)
            return {'Created':False,'message':message.error_message}
        return video_data_list 
    # def count_of_inserted_documents(self,class_name = CLASS_NAME):
    #     count = self.client.query.aggregate(class_name).with_meta_count().do()
    #     return count

    def store_data(self,batchsize = BATCH_SIZE,class_name = CLASS_NAME):
        try:
            
            logging.info("Strated storing data...........")
            
            video_data_list = self.create_data()
            sample_single_data = video_data_list[0]
            print(sample_single_data['Video_URL'])
            logging.info("Adding data objects to the class....")
            count1 = 0
            client  = WeaviateClient().client
            client.batch.configure(
                batch_size = batchsize
            )
            for single_data in video_data_list:
                with client.batch as batch:
                    batch.add_data_object(single_data , class_name)
                    print("Data added successfullyy.......")

            logging.info("Successfully add data objects and returning count...")
            
            # count = self.count_of_inserted_documents(class_name=class_name)
            count = client.query.aggregate(class_name).with_meta_count().do()
    #     
            logging.info(f"Successfully Stored {count} no.of documents!!")
        except Exception as e:
            message = CustomException(e,sys)
            return {'Created':False,'message':message.error_message}

if __name__ =="__main__":
    logging.info("Connecting to weaviate...")
    storedata = WeaviateDataStore()
    # Create class
    # logging.info('Created Class in weaviate...')
    # storedata.weaviateClient.create_class(schemaConfig=SCHEMA_CONFIG)
    storedata.store_data()
    # print(storedata.count_of_inserted_documents(class_name=CLASS_NAME))