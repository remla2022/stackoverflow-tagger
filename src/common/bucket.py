"""
Provides download and upload functionality
For interfacing with MinIO buckets
"""
import os

from joblib import load
from minio import Minio
from minio.error import S3Error

from common.logger import Logger

def authenticate(object_storage_endpoint : str,
                 access_key : str, secret_key : str,
                 secure : bool):
    """Authenticates to the object storage environment.

    Args:
        object_storage_endpoint (str): The endpoint to connect to
        access_key (str): Object storage access key
        secret_key (str): Object storage secret key
        secure (bool): Whether the connection should use TLS

    Returns:
        Minio: The Minio client
    """
    # Get credentials from env variables
    return Minio(
        object_storage_endpoint,
        access_key=access_key, secret_key=secret_key,
        secure=secure
    )


def upload_model(model_path : str,
                 bucket_name : str,
                 model_name : str,
                 object_storage_endpoint : str,
                 access_key : str,
                 secret_key : str,
                 secure : bool):
    """Uploads a file to the object storage bucket.

    Args:
        model_path (str): The local path of the model to upload
        bucket_name (str): The name of the bucket to upload to
        model_name (str): The name that the object in the bucket
        object_storage_endpoint (str) : The endpoint used for auth
        access_key (str) : The auth access key
        secret_key (str) : The auth secret key
        secure (str) : Whether to use TLS during auth
    """
    Logger.info(f'Uploading model from path\
        {model_path} to bucket {bucket_name} as {model_name}')

    client = authenticate(object_storage_endpoint, access_key, secret_key, secure)
    if not client.bucket_exists(bucket_name):
        Logger.info(f'Creating bucket : {bucket_name}')
        client.make_bucket(bucket_name)
        Logger.info('Creating creation succeeded ✔️')
    try:
        client.fput_object(bucket_name, model_name, model_path)
    except S3Error as error:
        err = Logger.get_color_string(error, Logger.FAIL)
        Logger.fail(f'Model upload failed ❌\n{err}')
    Logger.info('Model upload succeeded ✔️')


def download_model(model_path : str,
                   bucket_name : str,
                   model_name : str,
                   object_storage_endpoint : str,
                   access_key : str, secret_key : str,
                   secure : bool):
    """Downloads a file to the object storage bucket.

    Args:
        model_path (str): The local path of the model to upload
        bucket_name (str): The name of the bucket to upload to
        model_name (str): The name that the object in the bucket
        object_storage_endpoint (str) : The endpoint used for auth
        access_key (str) : The auth access key
        secre_key (str) : The auth secret key
        secure (str) : Whether to use TLS during auth

    Returns:
        bool: Whether the download was successful.
    """
    Logger.info(f'Downloading model {model_name}\
        from bucket {bucket_name} to {model_path}')

    client = authenticate(object_storage_endpoint, access_key, secret_key, secure)
    if not client.bucket_exists(bucket_name):
        Logger.fail(f'Model download failed, bucket {bucket_name} does not exist ❌')
        return False
    success = True
    try:
        client.fget_object(bucket_name, model_name, model_path)
    except S3Error as error:
        success = False
        err = Logger.get_color_string(error, Logger.FAIL)
        Logger.fail(f'Model download failed ❌\n{err}')
    
    if success:
        Logger.info('Model download succeeded ✔️')

    return success

def load_model(model_path : str):
    """Loads a model from the specified path.

    Args:
        model_path (str): The path of the model to load

    Returns:
        The loaded scikitlearn model.
    """
    Logger.info('Attempting to load new model from bucket...')
    if not os.path.isfile(model_path):
        Logger.fail(f'No model available at {model_path} ❌')
        return None
    model = load(model_path)

    Logger.info('Model loading succeeded ✔️')
    return model
