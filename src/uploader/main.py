import argparse
import sys
from pathlib import Path

from uploader.logger import logger
from uploader.presigner import get_presigned_url
from uploader.uploader import upload_file_to_presigned_url

DEFAULT_PROFILE = "default"


def main():
    """
    Main function to start upload process to s3.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket-name", help="Name of the S3 bucket to upload to.", required=True)
    parser.add_argument(
        "--upload-path",
        help="Path in the S3 bucket to upload to including the CSV file.",
        required=True,
    )
    parser.add_argument(
        "--file-location", help="Local path to the CSV file to upload.", required=True
    )
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE,
        help=f"AWS profile name to use for authentication (defaults to {DEFAULT_PROFILE}).",
    )
    args = parser.parse_args()
    file_path = Path(args.file_location).expanduser()

    if not file_path.is_file():
        logger.error(f"❌ File not found at: {file_path}")
        exit(1)

    logger.info(f"📦 Preparing upload of file: {file_path}")
    presigned_url = get_presigned_url(
        bucket_name=args.bucket_name,
        upload_path=args.upload_path,
        profile=args.profile,
        expiration=3600,
    )
    if presigned_url is None:
        logger.error("❌ Failed to generate presigned URL.")
        sys.exit(1)
    result = upload_file_to_presigned_url(
        presigned_url=presigned_url,
        file_path=str(file_path),
    )
    if result:
        logger.info("✅ Upload completed successfully.")
    else:
        logger.error("❌ Upload failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
