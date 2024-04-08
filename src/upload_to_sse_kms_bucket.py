import os
import boto3

endpoint_url = os.getenv("MINIO_TEST_S3_ENDPOINT")
aws_access_key_id = os.getenv("MINIO_ROOT_USER")
aws_secret_access_key = os.getenv("MINIO_ROOT_PASSWORD")

s3_client = boto3.resource(
    "s3",
    endpoint_url=endpoint_url,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=None,
    config=boto3.session.Config(signature_version="s3v4"),
    verify=False,
)


def upload_to_s3(bucket, kms_key, key):
    try:
        response = s3_client.Object(bucket, key).put(
            Body=b"some content of test object for upload",
            ServerSideEncryption="aws:kms",
            SSEKMSKeyId=kms_key,
        )
        print(f"Done with: {response}")

    except Exception as error:
        print(error)


if __name__ == "__main__":

    bucket = os.getenv("MINIO_TEST_S3_BUCKET")
    kms_key = os.getenv("MINIO_KMS_KES_KEY_NAME")
    object_key = "testfile.txt"

    upload_to_s3(bucket=bucket, kms_key=kms_key, key=object_key)
