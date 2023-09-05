from fastapi import FastAPI,File,UploadFile
from fastapi.responses import JSONResponse
from typing import List,Union,Any  
from src.utils.database_handler import MongobdClient      
from src.utils.s3_handler import S3Connection    
import uvicorn

app = FastAPI(title = "DataCollection-Server")
mongo = MongobdClient
s3 = S3Connection()

choices = {}
