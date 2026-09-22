import boto3


def upload_bytes(bucket_name: str, object_key: str, body: bytes) -> None:
    s3 = boto3.client("s3")

    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=body,
    )
    
