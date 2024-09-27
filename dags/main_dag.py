from airflow import DAG
from operators.feedly import FeedlyToS3Operator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

dag = DAG(dag_id='main_dag',
          default_args=default_args,
          catchup=False,
          schedule_interval='0 12,23 * * *') #twice daily - once at noon, the other at 11pm

# Must create a connection in admin panel called main_feedly_connection with
# base url, and in the "extra" field, the header for bearer auth i.e.:
# {"Authorization": "Bearer xxxxxxxxxxxx"}
# Must create the S3 connection in the admin panel called 'main_aws'
# before this works.
load_feedly_data = FeedlyToS3Operator(source_conn='main_feedly',
                                      source_endpoint='v3/.......',
                                      dest_conn='main_aws',
                                      dest_bucket=''
                                      )