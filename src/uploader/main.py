import argparse

from uploader.presigner import get_presigned_url

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

    _ = get_presigned_url(
        bucket_name=args.bucket_name,
        upload_path=args.upload_path,
        profile=args.profile,
        expiration=3600,
    )


if __name__ == "__main__":
    main()
