import sys
import json
import pprint
import os
from boto3.session import Session

config = json.load(open(os.path.join(os.path.dirname(__file__), 'config.json')))

def create_bucket(bucket_name, session=None, region=None):
    session = session if session else Session(aws_access_key_id=config['aws_client_id'], 
                                    aws_secret_access_key=config['aws_client_secret'],
                                    region_name=config['aws_default_region'])
    region = region if region else config['aws_default_region']
    s3 = session.resource('s3')
    new_bucket = s3.create_bucket(Bucket=bucket_name,
                                CreateBucketConfiguration={'LocationConstraint': region})
    return new_bucket

if __name__ == '__main__':
    bucket_name = sys.argv[1]
    pprint.pprint(create_bucket(bucket_name))

