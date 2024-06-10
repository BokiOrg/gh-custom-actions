import os
import boto3
import mimetypes
from botocore.config import Config
from pathlib import Path


def run():
    bucket = os.environ['INPUT_BUCKET']
    bucket_region = os.environ['INPUT_BUCKET-REGION']
    dist_folder = os.environ['INPUT_DIST-FOLDER']

    configuration = Config(region_name=bucket_region)

    s3_client = boto3.client('s3', config=configuration)

    for root, sub_dirs, files in os.walk(dist_folder):
        for file in files:
            file_path = str(Path(root) / file)
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'binary/octet-stream'

            with open(file_path, 'rb') as data:
                s3_client.upload_fileobj(data, bucket, file, ExtraArgs={'ContentType': content_type})

    website_url = f'http://{bucket}.s3-website-{bucket_region}.amazonaws.com'

    # print(f'::set-output name=website-url::{website_url}')
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        print(f'website-url={website_url}', file=f)


if __name__ == '__main__':
    run()
