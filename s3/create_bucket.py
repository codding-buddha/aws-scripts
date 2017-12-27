import sys
import pprint
import helper
from boto3.session import Session

config = helper.app_config()

def create_bucket(bucket_name, is_publicly_readable=False, session=None, region=None):
    session = session if session else helper.get_session()
    region = region if region else config['aws_default_region']
    s3 = session.resource('s3')
    new_bucket = s3.create_bucket(Bucket=bucket_name,
                                CreateBucketConfiguration={'LocationConstraint': region}, 
                                ACL= 'public-read' if is_publicly_readable else 'private')
    return new_bucket

if __name__ == '__main__':
    bucket_name = sys.argv[1]
    pprint.pprint(create_bucket(bucket_name))

