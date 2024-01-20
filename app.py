from fastapi import FastAPI,File,UploadFile
from fastapi.responses import JSONResponse
from typing import List,Union,Any  
from src.utils.database_handler import MongobdClient    
from src.constants.database import COLLECTION_NAME, DATABASE_NAME
from src.utils.s3_handler import S3Connection    
import uvicorn

app = FastAPI(title = "DataCollection-Server")
mongo = MongobdClient()
s3 = S3Connection()

choices = {}

@app.get("/")
def home():
    try: 
        response = {"Status":"Success","Response": "Go to fastAPI docs to access the routes" }
        return JSONResponse(content= response, status_code=200, media_type= "application/json")
    except Exception as e:
        raise e
# Fetch all the labels
@app.get("/fetch")
def fetch_label():
    try:
        global choices
        result = mongo.database[COLLECTION_NAME].find()
        documents = [document for document in result]
        choices = dict(documents[0])
        response = {"Status":"Success","Repsonse":str(documents[0]) }
        return JSONResponse(content=response, status_code= 200, media_type= "application/json")

    except Exception as e:
        raise e          
    
# Label api
@app.post("/add_label/{label_name}")
def add_label(label_name: str):
    result = mongo.database[COLLECTION_NAME].find()
    documents = [document for document in result]
    last_value = list(map(int,list(documents[0].keys())[1:]))[-1]
    response = mongo.database[COLLECTION_NAME].update_one({"_id":documents[0]["_id"]},
                                                          {"$set":{str(last_value+1):label_name}})
    
    if response.modified_count == 1:
        response = s3.add_label(label_name)
        return {"Status":"Success","S3-Response": response}
    else:
        return {"Status":"Fail","Message":response[1]}

#single video
@app.get("/single_upload/")
def single_upload():
    info = {"Reponse": "Available", "Post-Request-Body":["label","Files"]}
    return JSONResponse(content=info, status_code=200, media_type="application/json")


# Upload single video
@app.post("/single_upload/")
async def single_upload(label: str, file: UploadFile = None):
    # label = choices.get(label,False)
    print(file.content_type)
    if file.content_type == "video/mp4" and label !=False:
        response = s3.upload_to_s3(file.file,label)
        return {"filename":file.filename , "label":label,"S3-response":response}
    else:
        return {
            "ContentType":f"Content type should be video/mp4 not {file.content_type}",
            "LabelFounce": label,
        }
        
# Bulk upload video
@app.get("/bulk_upload")
def bulk_upload():
    info = {"Response":"Avialable", "Post-Request-Body":["label","Files"]}
    return JSONResponse(content=info, status_code=200, media_type="application/json")


# Tranforms here
@app.post("/bulk_upload")
def bulk_upload(label_value: str, files: List[UploadFile] = File(...)):
    try:
        skipped = []
        # label_value = choices.get(label, False)
        final_response = None  # Initialize final_response outside the if block
        if label_value:
            for file in files:
                if file.content_type == "video/mp4":
                    response = s3.upload_to_s3(file.file, label_value)
                    final_response = response
                else:
                    skipped.append(file.filename)
            return {
                "label": label_value,
                "skipped": skipped,
                "S3-Response": final_response,
                "LabelFound": label_value,
            }
        else:
            return {
                "label": label_value,
                "skipped": skipped,
                "S3-Response": final_response,
                "LabelFound": label_value,
            }

    except Exception as e:
        return {"ContentType": f"Content type should be video/mp4, not {e}"}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port =8030)
