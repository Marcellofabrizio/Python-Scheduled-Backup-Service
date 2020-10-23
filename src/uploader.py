import os
import boto3
import logging
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import ClientError
from file_handler import remove_file

AWS_ACCESS_KEY_ID= 'YOUR AWS ID '
AWS_SECRET_ACCESS_KEY= 'YOUR SUPER SECRET AWS ACCESS KEY'

def upload_to_aws(file_name, bucket, object_name=None, remove_zips=True):
    """
    Upload a file to an S3 bucket
    Args:
        file_name: file to be uploaded.
        bucket: bucket to be uploaded.
        object_name: the s3 object name. If not specified, it 
                     will have the same name as file_name.
        remove_zips: if true, will remove the zips files after 
                     uploading. Only recommend setting it False
                     for testing reasons. 
    """

    if object_name == None:
        object_name = file_name

    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        if remove_zips:
            remove_file(file_name)
    except ClientError as e:
        logging.error(e)
        return False
    except NoCredentialsError as e:
        logging.error(e)
        return False
    except FileNotFoundError as e:
        logging.error(e)
        return False
    return True

def upload_all_files(path_to_dir, bucket):

    directory = os.fsencode(path_to_dir)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.zip'):
            upload_to_aws(path_to_dir + '/' + filename, bucket)
