import os

from storages.backends.s3boto3 import S3Boto3Storage


SERVER_CODE = os.getenv("SERVER_CODE", "findorlookup")


class MediaStorage(S3Boto3Storage):
    bucket_name = os.getenv("MEDIA_BUCKET_NAME")
    location = ""
    default_acl = "private"
    querystring_auth = True
    querystring_expire = int(os.getenv("S3_PRESIGN_EXPIRE_SECONDS", "900"))
    file_overwrite = False
    signature_version = "s3v4"


class StaticStorage(S3Boto3Storage):
    bucket_name = os.getenv("STATIC_BUCKET_NAME", "mystaticimg")
    location = f"static-{SERVER_CODE}/"
    default_acl = "public-read"
    querystring_auth = False
    signature_version = "s3v4"
