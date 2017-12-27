import sys
import pprint
import helper
import os
import mimetypes

from boto3.session import Session

config = helper.app_config()

def upload_file(bucket_name, file_name, file_path, is_public=False, session=None):
    session = session if session else helper.get_session()
    client = session.client('s3')
    content_type = mimetypes.MimeTypes().guess_type(file_name)[0]
    obj = client.put_object(Bucket=bucket_name, Key=file_name, Body=open(file_path, 'rb'), ContentType=content_type)
    if is_public:
        client.put_object_acl(Bucket=bucket_name, Key=file_name, ACL='public-read')

def upload_dir(bucket_name, dir, is_public=False, session=None):
    session = session if session else helper.get_session()
    file_list = flatten_filelist(dir)
    for file_name, file_path in file_list:
        print('Uploading {} from path {}'.format(file_name, file_path))
        upload_file(bucket_name, file_name, file_path, is_public)

def flatten_filelist(dir, removedir_prefix=True):
    file_names = []
    file_paths = []
    for root, dirs, files in os.walk(dir, topdown = True):
        dr = os.path.relpath(root, dir) if removedir_prefix else dir
        dr = dr if dr != '.' else ''
        for name in files:
            file_paths.append(os.path.join(root, name))
            file_names.append(os.path.join(dr, name))
    return zip(file_names, file_paths)


if __name__ == '__main__':
    get_filenames(sys.argv[1])
    bucket_name = sys.argv[1]
    file_path = sys.argv[2]
    create_empty_directory(bucket_name, 'files')
    file_name = os.path.basename(file_path)
    #pprint.pprint(upload_file(bucket_name, file_name, file_path))

