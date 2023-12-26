# Video Streaming Data Collection
This Repository is used to collect the data to train the Video classification model and to generate embeddings from the model for video search engine.

## Architecture

![DatacollectionPipeline](https://github.com/SaiKumarOfficial/video-streaming-data-collection/assets/95096218/77ed7a4e-521e-41f1-80c6-0b9506496451)

## Git-hub Configurations
```text
1. Go to setting -> actions -> runner
2. Add runner/ec2 instance by using X86_64 arc
3. Add pages for github
4. Go to secrets tab -> Repository secrets and add secrets 
```
## Route Details 
![image](https://user-images.githubusercontent.com/40850370/189587344-4044f19a-2da7-495f-a482-3533fc362e74.png)

1. **/fetch**  : To get labels currently present in the database. Important to call as it updates in memory database.
2. **/Single_upload** : This Api Should be used to upload single image to s3 bucket
3. **/bulk_upload**   : This Api should be used to upload bulk images to s3 bucket
4. **/add_label** :  This api should be ued to add new label in s3 bucket.

## Infrastructure Details
- S3 Bucket 
- Mongo Database
- Elastic Container Registry
- Elastic Compute Cloud

## Steps
1. Create data folder 
2. Put videos in data folder 
3. run s3 setup and mongo setup
4. Done

## Env variable

```bash

export ATLAS_CLUSTER_USERNAME=<username>
export ATLAS_CLUSTER_PASSWORD=<password>

export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
export AWS_REGION=<region>

export AWS_BUCKET_NAME=<AWS_BUCKET_NAME>
export AWS_ECR_LOGIN_URI=<AWS_ECR_LOGIN_URI>
export ECR_REPOSITORY_NAME=<name>

export DATABASE_NAME=<name>
```