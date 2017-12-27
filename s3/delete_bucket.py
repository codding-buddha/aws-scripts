import helper
import sys

def delete_bucket(bucket_name, region=None, sess = None):
    sess = sess if sess else helper.get_session()
    region = region if region else helper.app_config()['aws_default_region']
    s3_client = sess.client('s3', region_name=region)
    delete_all_objects(bucket_name, region=region, sess=sess)
    s3_client.delete_bucket(Bucket=bucket_name)
    print('Bucket {} deleted successfully'.format(bucket_name))
    


def delete_all_objects(bucket_name, region, sess):
    s3_client = sess.client('s3', region_name=region)
    paginator = s3_client.get_paginator('list_object_versions')
    page_iterator = paginator.paginate(Bucket=bucket_name, PaginationConfig={'PageSize': 10})
    for page in page_iterator:
        if 'Versions' in page:
            obj_keys = [(obj['Key'], obj['VersionId']) for obj in page['Versions']]
            delete_objects(bucket_name, obj_keys, region, sess)

        if 'DeleteMarkers' in page:
            delete_markers = [(obj['Key'], obj['VersionId']) for obj in page['DeleteMarkers']]
            delete_objects(bucket_name, delete_markers, region, sess)
        

def delete_objects(bucket_name, objects, region, sess):
    if not len(objects):
        return

    s3_client = sess.client('s3', region_name=region)
    delete_param = {'Objects': [{'Key': object_id, 'VersionId': version_id } for object_id, version_id in objects] , 'Quiet': True}
    print('Deleting {} Objects from bucket {}'.format(len(objects), bucket_name))
    s3_client.delete_objects(Bucket=bucket_name, Delete=delete_param)
    


if __name__ == '__main__':
    bucket_name = sys.argv[1]
    delete_bucket(bucket_name)