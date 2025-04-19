import boto3
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound

from uploader.logger import logger


def get_s3_client(profile: str | None = None):
    try:
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        logger.info(f"🔐 Using AWS profile: {profile or 'default'}")
        return session.client("s3")
    except ProfileNotFound as e:
        logger.error(f"❌ AWS profile not found: {e}")
        raise


def get_presigned_url(
    bucket_name: str, upload_path: str, profile: str | None = None, expiration: int = 3600
) -> str | None:
    """
    Generate a presigned URL to upload a file to S3.

    Args:
        bucket_name (str): Name of the S3 bucket.
        upload_path (str): Path in the S3 bucket to upload to (including the name of the file).
        profile (str, optional): AWS profile name. Defaults to None and default AWS profile.
        expiration (int, optional):
          Time in seconds for the presigned URL to remain valid. Defaults to 3600.

    Returns:
        str: Presigned URL as a string. None if error occurs.
    """

    try:
        s3_client = get_s3_client(profile=profile)
        logger.info(
            f"🔗 Generating presigned URL for bucket='{bucket_name}' and key='{upload_path}'..."
        )
        response = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket_name, "Key": upload_path},
            ExpiresIn=expiration,
            HttpMethod="PUT",
        )
        return response
    except ProfileNotFound as e:
        logger.error(f"❌ AWS profile not found: {e}")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        logger.error(f"❌ AWS ClientError [{error_code}]: {e}")
    except BotoCoreError as e:
        logger.error(f"❌ BotoCoreError: {e}")
    except Exception as e:
        logger.exception(f"❌ Unexpected error while generating presigned URL: {e}")

    return None
