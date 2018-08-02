from storages.backends.s3boto3 import S3Boto3Storage, SpooledTemporaryFile
import os

class StaticS3Boto3Storage(S3Boto3Storage):
    location = 'static'


class MediaS3Boto3Storage(S3Boto3Storage):
    location = 'media'

    def _save_content(self, obj, content, parameters):

        content.seek(0, os.SEEK_SET)

        content_autoclose = SpooledTemporaryFile()

        content_autoclose.write(content.read())

        super(MediaS3Boto3Storage, self)._save_content(obj, content_autoclose, parameters)

        if not content_autoclose.closed:
            content_autoclose.close()