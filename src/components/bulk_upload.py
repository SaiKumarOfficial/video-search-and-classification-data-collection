import os
import base64
from from_root import from_root
from tqdm import tqdm


# Upload data using boto3 [ Takes a lot of time ]
def upload_bulk_data(root="ISRO-documentary"):
    labels = os.listdir(root)
    for label in tqdm(labels):
        data = []
        videos = os.listdir(root + "/" + label)
        for video in tqdm(videos):
            path = os.path.join(from_root(), root, label, video)
            with open(rf'{path}', "rb") as video:
                data.append(base64.b64encode(video.read()).decode())

    print("/nCompleted")


upload_bulk_data(root="ISRO-documentary")