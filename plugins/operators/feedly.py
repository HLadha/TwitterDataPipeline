from airflow.models import BaseOperator
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime



class FeedlyToS3Operator(BaseOperator):
    def __init__(self,
                 source_conn,
                 source_endpoint,
                 dest_conn,
                 dest_bucket,
                 *args, **kwargs):
        self.source_conn = source_conn
        self.dest_conn = dest_conn
        self.source_endpoint = source_endpoint
        self.dest_bucket = dest_bucket
        super().__init__(*args, **kwargs)

    def execute(self, context):
        self.log.info("Connecting to feedly")

        feedly_hook = HttpHook('GET', self.source_conn)
        response = feedly_hook.run(endpoint=self.source_endpoint)

        s3_hook = S3Hook(aws_conn_id=self.dest_conn)
        datestring = datetime.now().strftime('%Y%m%d_%H%M%S')
        s3_hook.load_string(string_data=response.text,
                            key=f'raw_data/feedly/{datestring}.json',
                            bucket_name=self.dest_bucket)