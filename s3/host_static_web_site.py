import os
import helper
import botocore
import sys
import json

from create_bucket import create_bucket
from upload import upload_dir

def host_static_website(rootdir, index_doc_path=None, error_doc_path=None):
    session = helper.get_session()
    try:
        bucket_name = os.path.basename(rootdir)   
        index_doc_path = index_doc_path if index_doc_path else 'index.html'
        error_doc_path = error_doc_path if error_doc_path else 'error.html'
        app_config = helper.app_config()
        client = session.client('s3', region_name=app_config['aws_default_region'])
        bucket = create_bucket(bucket_name, True, session, region=app_config['aws_default_region'])
        bucket.wait_until_exists()
        """
        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'AddPerm',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': "arn:aws:s3:::{}/*".format(bucket_name)
            }]
        }
        bucket_policy = json.dumps(bucket_policy)
        """
        website_config = {
            'IndexDocument': { 
                'Suffix': index_doc_path
            },
            'ErrorDocument': {
                'Key': error_doc_path
            }
        }

        client.put_bucket_website(Bucket=bucket_name, WebsiteConfiguration=website_config)
        #client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        upload_dir(bucket_name, rootdir, is_public=True)
    except botocore.exceptions.ClientError as e:
        print('Site creation failed')
        print(e)
        return
    print('Website created successfully')
    print('Check out ' + "https://s3-{0}.amazonaws.com/{1}/{2}".format(app_config['aws_default_region'],bucket_name, index_doc_path))


if __name__ == '__main__':
    rootdir = sys.argv[1]
    host_static_website(rootdir)