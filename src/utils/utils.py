import uuid

# Generate unique names for all the videos
def video_unique_name():
    return "video-"+str(uuid.uuid1())
