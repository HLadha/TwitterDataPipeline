from airflow import DAG
from operators.feedly import S3DataPipelineOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

dag = DAG(dag_id='main_dag',
          default_args=default_args,
          catchup=False,
          schedule_interval='0 12,23 * * *')

check_s3_keys = S3DataPipelineOperator(source_conn='main_aws',
	                                   source_bucket='',
	                                   max_items=100)