from django.conf import settings
from storages.backends.s3 import S3Storage


class StaticStorage(S3Storage):
    bucket_name = settings.AWS_STATIC_STORAGE_BUCKET_NAME
    default_acl = "public-read"
    querystring_auth = False
