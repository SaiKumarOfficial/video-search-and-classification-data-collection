# S3 bucket constants.................

AWS_BUCKET_NAME = "isro-documentary-videos"


# .Mongodb database constants.............
DATABASE_NAME = "Isro-project"
COLLECTION_NAME = "labels-data"

# Weaviate vector database................
CLASS_NAME = "ISRODocumentaries"
CLIENT_URL = "http://localhost:8080"

SCHEMA_CONFIG =  {
    'class': CLASS_NAME,
    'vectorizer': 'img2vec-neural',
    'vectorIndexType': 'hnsw',
    'moduleConfig': {
        'img2vec-neural': {
            'imageFields': [
                'image'
            ]
        }
    },
    'properties': [{
            'name': 'image',
            'dataType': ['blob']
        },
        {
            'name': 'VideoFileName',
            'dataType': ['string']
        },
        {   
            'name':"FrameName",
            'dataType':['string']
        },
        {
            'name': "VideoURL",
            'dataType': ['string']
        },
        {
            'name':'Label',
            'dataType':['string']
        }
    ]

}