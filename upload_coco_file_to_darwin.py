"""
Batch preparation lambda function. Updates batch information in AIDA
database. Updates the resizing tables.
"""

# Standard imports
from typing import List, Tuple
import datetime as _dt
import logging
import json
import os
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Third party imports
import dotenv
import boto3

sagemaker_client = boto3.client("sagemaker")

processor_args = ["--batch_id", batch_id, "--coco_id", coco_id]

''' Replace "--batch_id" and the "--coco_id" with the IDs of the file you want to upload '''

def start_processing_job(processor_args, input_s3_uri: str) -> str:
    """
    Function to start a sagemaker processing job.
    Args:
        processor_args (List[str]): List of arguments to pass to the container.
        input_s3_uri (str): S3 URI to input data.
    Returns:
        processing_job_name (str): Name of processing job started.
    """
    processing_job_name = f"coco-upload-{_dt.datetime.now():%Y-%m-%d-%H-%M-%S-%f}"
    CONTAINER_INPUT_PATH = "/opt/ml/processing/input"
    INSTANCE_COUNT = "1"
    INSTANCE_TYPE = "ml.m5.xlarge"
    INSTANCE_VOL = "100"

    ROLE_ARN = "arn:aws:iam::608767285787:role/service-role/AmazonSageMaker-ExecutionRole-20210224T124037"
    IMAGE_URI = "608767285787.dkr.ecr.us-east-1.amazonaws.com/upload-coco:1.7"

    # Start processing job from sagemaker client
    sagemaker_client.create_processing_job(
        ProcessingJobName=processing_job_name,
        ProcessingInputs=[
            {
                "InputName": "Coco Input",
                "S3Input": {
                    "S3Uri": "s3://oreyeon-models/yolov5/coco-haivo-new/NRV1099.json",
                    ''' Replace the URI with the one that corresponds to the coco file'''
                    "LocalPath": CONTAINER_INPUT_PATH,
                    "S3DataType": "S3Prefix",
                    "S3InputMode": "File",
                    "S3DataDistributionType": "FullyReplicated",
                },
            },
        ],
        ProcessingResources={
            "ClusterConfig": {
                "InstanceCount": int(INSTANCE_COUNT),
                "InstanceType": INSTANCE_TYPE,
                "VolumeSizeInGB": int(INSTANCE_VOL),
            }
        },
        AppSpecification={
            "ImageUri": IMAGE_URI,
            "ContainerArguments": processor_args,
        },
        Environment={"INPUT_DATA_PATH": CONTAINER_INPUT_PATH},
        RoleArn=ROLE_ARN,
    )

    return processing_job_name

"""
BUCKET=oreyeon-data
COCO_PREFIX=labels/coco/downscaled
INSTANCE_COUNT=1
INSTANCE_TYPE=ml.m5.xlarge
INSTANCE_VOL=100
ROLE_ARN=arn:aws:iam::608767285787:role/service-role/AmazonSageMaker-ExecutionRole-20210224T124037
IMAGE_URI=608767285787.dkr.ecr.us-east-1.amazonaws.com/upload-coco:1.7
CONTAINER_INPUT_PATH=/opt/ml/processing/input
"""

start_processing_job(processor_args, "")







