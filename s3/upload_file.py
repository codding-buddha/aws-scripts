import sys
import json
import pprint
import os
from boto3.session import Session

config = json.load(open(os.path.join(os.path.dirname(__file__), 'config.json')))

def upload_file(bucket_name, file_path, session=None):
    session = session if session else Session(aws_access_key_id=config['aws_client_id'], 
                                    aws_secret_access_key=config['aws_client_secret'],
                                    region_name=config['aws_default_region'])
    s3 = session.resource('s3')
    file_name = os.path.basename(file_path)
    return s3.Object(bucket_name, file_name).put(Body=open(file_path, 'rb'))

if __name__ == '__main__':
    bucket_name = sys.argv[1]
    file_path = sys.argv[2]
    pprint.pprint(upload_file(bucket_name, file_path))

