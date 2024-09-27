import boto3
import json
import pandas as pd
from datetime import datetime
import requests
from datetime import timezone

class S3_Op(BaseOperator):
    def __init__(self,
             source_conn,
             source_bucket,
             prefix,
             *args, **kwargs):
        self.source_conn = source_conn
        self.source_bucket = source_bucket
        self.prefix = prefix
        super().__init__(*args, **kwargs)

    def execute(self, context):
        s3_hook = S3Hook(aws_conn_id=self.source_conn)
        file_list = s3_hook.list_keys(bucket_name=self.source_bucket,
                         prefix=self.prefix)
        self.log.info(file_list)
        relevant_cols = ['language', 'authorDetails.username', 'content.content', 'published']
        dfs = []
        for file in file_list:
            file_data = s3_hook.read_key(key=file,
                bucket_name=self.source_bucket)
            js = json.load(file_data)
            df = pd.json_normalize(js['items'], max_level=10)[relevant_cols]
            df['tweet_id'] = df['content.content'].str.extract(r'<blockquote data-id="(\d*)".*')
            df['tweet_contents'] = df['content.content'].str.replace(r'<br>- [\w ]*\(@\w*\).*', '', regex=True).str.replace(r'<[^>]*>', '', regex=True).str.replace(r'[\w ]*\(@\w*\) retweeted:', '', regex=True)
            df['is_retweet'] = df['content.content'].str.contains(r'[\w ]*\(@\w*\) retweeted:')
            df = df[['tweet_id', 'tweet_contents', 'is_retweet', 'published', 'language', 'authorDetails.username']]
            df.columns = ['tweet_id', 'tweet_contents', 'is_retweet', 'published', 'language', 'username']
            df = df.loc[~df['is_retweet'], :]
            dfs.append(df)

        print(dfs)