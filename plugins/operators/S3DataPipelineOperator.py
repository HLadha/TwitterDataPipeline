from airflow.models import BaseOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime

class S3DataPipelineOperator(BaseOperator):
    def __init__(self,
                 source_conn,
                 source_bucket,
                 max_items,
                 *args, **kwargs):
        self.max_items = max_items
        self.source_conn = source_conn
        self.source_bucket = source_bucket
        super().__init__(*args, **kwargs)

    def execute(self, context):

    	self.log.info("Connecting to S3")

    	s3_hook = S3Hook(aws_conn_id=self.source_conn)
    	response = s3_hook.list_keys(bucket_name=self.source_bucket,
    		              max_itemsmax_items=self.max_items)
    	self.log.info(response)