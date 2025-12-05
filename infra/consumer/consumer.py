import json
import boto3
import time
from kafka import KafkaConsumer
from botocore.exceptions import ClientError

# ---- MinIO CONFIG ----
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9002',
    aws_access_key_id='admin',
    aws_secret_access_key='password123'
)

bucket_name = 'bronze-transactions'

# Create bucket if not exists
try:
    s3.head_bucket(Bucket=bucket_name)
except ClientError:
    print(f"Bucket not found. Creating bucket: {bucket_name}")
    s3.create_bucket(Bucket=bucket_name)

# ---- KAFKA CONSUMER ----
consumer = KafkaConsumer(
    'stock-quotes',
    bootstrap_servers=["localhost:29092"],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='bronze-consumers',
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Consumer streaming and saving to MinIO...")

for message in consumer:
    record = message.value
    symbol = record.get("symbol", "UNKNOWN")
    ts = record.get("timestamp", int(time.time()))  # FIXED

    key = f"{symbol}/{ts}.json"

    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(record),
        ContentType='application/json'
    )

    print(f"Saved → s3://{bucket_name}/{key}")
