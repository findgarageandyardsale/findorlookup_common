import os

from storages.backends.s3boto3 import S3Boto3Storage


SERVER_CODE = os.getenv("SERVER_CODE", "findorlookup")

# When MEDIA_CDN_DOMAIN is set (e.g. "cdn.findcarsales.com"), MediaStorage
# serves images via CloudFront with stable, cacheable URLs and no object ACL
# (bucket policy / OAC grants access). When unset, falls back to the original
# private-presigned behavior so this flip is a single-env-var change.
_MEDIA_CDN_DOMAIN = os.getenv("MEDIA_CDN_DOMAIN") or None


class MediaStorage(S3Boto3Storage):
    bucket_name = os.getenv("MEDIA_BUCKET_NAME")
    location = ""
    default_acl = None if _MEDIA_CDN_DOMAIN else "private"
    querystring_auth = not bool(_MEDIA_CDN_DOMAIN)
    querystring_expire = int(os.getenv("S3_PRESIGN_EXPIRE_SECONDS", "900"))
    file_overwrite = False
    signature_version = "s3v4"
    custom_domain = _MEDIA_CDN_DOMAIN


class StaticStorage(S3Boto3Storage):
    bucket_name = os.getenv("STATIC_BUCKET_NAME", "mystaticimg")
    location = f"static-{SERVER_CODE}/"
    default_acl = "public-read"
    querystring_auth = False
    signature_version = "s3v4"
