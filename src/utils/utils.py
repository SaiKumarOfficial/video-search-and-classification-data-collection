import uuid

# Generate unique names for all the videos
def video_unique_name(video_filename,count):
    return "img-"+str(count) +'-'+ video_filename+ "-"+str(uuid.uuid4())[:11]
