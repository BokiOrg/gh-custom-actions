import os
import boto3
from botocore.config import Config


def run():
    bucket = os.environ['INPUT_BUCKET']
    bucket_region = os.environ['INPUT_BUCKET-REGION']
    dist_folder = os.environ['INPUT_DIST-FOLDER']

    configuration = Config(region_name=bucket_region)

    s3_client = boto3.client('s3', config=configuration)

    for root, sub_dirs, files in os.walk(dist_folder):
        for file in files:
            s3_client.upload_file(os.path.join(root, file), bucket, file)

    website_url = f'http://{bucket}.s3-website-{bucket_region}.amazonaws.com'

    # print(f'::set-output name=website-url::{website_url}')
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        print(f'website-url={website_url}', file=f)


if __name__ == '__main__':
    run()