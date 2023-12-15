import uuid

# Generate unique names for all the videos
def video_unique_name():
    return "vid-"+str(uuid.uuid1())

