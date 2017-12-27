import json
import os
from boto3.session import Session

def app_config():
    return json.load(open(os.path.join(os.path.dirname(__file__), 'config.json')))

def get_session():
    config = app_config()
    return Session(aws_access_key_id=config['aws_client_id'], 
                                    aws_secret_access_key=config['aws_client_secret'],
                                    region_name=config['aws_default_region'])