from django.conf import settings
from storages.backends.s3 import S3Storage


class StaticStorage(S3Storage):
    bucket_name = f"{settings.AWS_STORAGE_BUCKET_NAME}-static"
    default_acl = "public-read"
    querystring_auth = False
