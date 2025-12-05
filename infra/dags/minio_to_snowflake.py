# Importing libraries needed for file handling, object storage, Snowflake, and Airflow tasks
import os
import boto3                     # Used to connect to MinIO (S3 compatible)
import snowflake.connector       # Snowflake database connector
from airflow import DAG          # DAG object for defining workflows
from airflow.operators.python import PythonOperator  # Runs Python functions as tasks
from datetime import datetime, timedelta             # For scheduling

# -----------------------------
# MINIO CONFIGURATION
# -----------------------------

# Endpoint URL for MinIO inside Docker network (service name "minio")
MINIO_ENDPOINT = "http://minio:9000"

# Default admin credentials for MinIO
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "password123"

# Bucket name where your consumer stores JSON files
BUCKET = "bronze-transactions"

# Local directory inside Airflow container where files will be downloaded temporarily
LOCAL_DIR = "/tmp/minio_downloads"

# -----------------------------
# SNOWFLAKE CONFIGURATION
# -----------------------------

SNOWFLAKE_USER = "mahak"
SNOWFLAKE_PASSWORD = "Mahak@2003choubey"
SNOWFLAKE_ACCOUNT = "ft13754.ap-southeast-1"
     # ✔ ONLY THIS !!!
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
SNOWFLAKE_DB = "STOCK_MDS"
SNOWFLAKE_SCHEMA = "COMMON"

# -----------------------------
# TASK 1: DOWNLOAD FILES FROM MINIO
# -----------------------------

def download_from_minio():

    os.makedirs(LOCAL_DIR, exist_ok=True)

    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )

    objects = s3.list_objects_v2(Bucket=BUCKET).get("Contents", [])
    local_files = []

    for obj in objects:
        key = obj["Key"]
        local_file = os.path.join(LOCAL_DIR, os.path.basename(key))
        s3.download_file(BUCKET, key, local_file)

        print(f"Downloaded {key} -> {local_file}")

        local_files.append(local_file)

    return local_files

# -----------------------------
# TASK 2: LOAD FILES INTO SNOWFLAKE
# -----------------------------

def load_to_snowflake(**kwargs):

    local_files = kwargs['ti'].xcom_pull(task_ids='download_minio')

    if not local_files:
        print("No files to load.")
        return

    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DB,
        schema=SNOWFLAKE_SCHEMA
    )
    cur = conn.cursor()

    # Upload to Snowflake INTERNAL STAGE linked to your table
    for f in local_files:
        cur.execute(f"PUT file://{f} @%bronze_stock_raw")
        print(f"Uploaded {f} to Snowflake stage")

    # Load JSON files into table
    cur.execute("""
        COPY INTO bronze_stock_raw
        FROM @%bronze_stock_raw
        FILE_FORMAT = (TYPE=JSON)
    """)
    print("COPY INTO executed")

    cur.close()
    conn.close()

# -----------------------------
# AIRFLOW DAG CONFIGURATION
# -----------------------------

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "minio_to_snowflake",
    default_args=default_args,
    schedule="*/1 * * * *"
,  # run every 1 minute
    catchup=False,
) as dag:

    task1 = PythonOperator(
        task_id="download_minio",
        python_callable=download_from_minio,
    )

    task2 = PythonOperator(
        task_id="load_snowflake",
        python_callable=load_to_snowflake,
        provide_context=True,
    )

    task1 >> task2