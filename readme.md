# Real-Time Stocks Market Data Pipeline

![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?logo=snowflake&logoColor=white)
![DBT](https://img.shields.io/badge/dbt-FF694B?logo=dbt&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?logo=apacheairflow&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?logo=apachekafka&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?logo=powerbi&logoColor=black)

📌 Overview

I built this project to understand how real-world data engineering systems work across ingestion, storage, transformation, orchestration, and analytics.

This pipeline pulls live stock market tick data, processes it using the modern data stack, and exposes clean “Gold” data models for BI dashboards.

The aim was not just to replicate a tutorial —
👉 but to design a robust, production-style pipeline end-to-end as a fresher preparing for Data Engineer / Data Analyst roles.

🏗️ Architecture (My Version)

This is the architecture I implemented:

API → Kafka → MinIO → Airflow → Snowflake (Bronze → Silver → Gold via DBT) → Power BI

Each layer has a clear responsibility:

Kafka → Handles the "real-time" nature

MinIO → Acts as object storage for raw events

Snowflake → Scalable warehouse

DBT → Transformations & model logic

Airflow → Automation/orchestration

Power BI → Visualization using Gold models

🔧 Tech Stack (What I Actually Used Hands-On)
Layer	Tools
Streaming	Apache Kafka (Docker)
Storage	MinIO (S3 bucket)
Ingestion	Python (Producer + Consumer)
Orchestration	Apache Airflow
Warehouse	Snowflake
Transformations	DBT Core
Dashboard	Power BI
🌟 What This Pipeline Does

Collects live stock price ticks every few seconds

Streams them into Kafka as JSON

Writes raw JSON to MinIO

Loads raw objects into Snowflake Bronze tables

DBT cleans and enriches data into Silver

Creates business-friendly Gold models:

Latest KPIs

Candlestick charts

Trendline summaries

Power BI connects directly to Gold models for near real-time monitoring

📂 Project Structure (Cleaned & Curated)
real-time-stocks-mds/
│── producer/                 # Live API → Kafka
│── consumer/                 # Kafka → MinIO
│── infra/                    # Airflow & Docker infra
│── dbt_stocks/               # DBT models (Bronze, Silver, Gold)
│── dashboard/                # Power BI dashboard files
│── docker-compose.yml
│── requirements.txt
│── README.md

🧠 My Learning Outcomes (Placement Focus)

This project taught me:

1. How real-time data pipelines actually work

Message queue usage

Event streaming

Fault tolerance

2. How companies clean and structure raw data

Bronze → Silver → Gold

Window functions for trendlines and candlesticks

KPI calculations

3. How orchestration ties everything together

DAG scheduling

Task dependencies

Automated ingestion

4. How BI dashboards read transformed data

Direct Query vs Import

KPI modeling

Data refresh strategies

This helps me answer questions clearly in interviews like:

“Explain a project where you used SQL and Python together.”

“Have you worked with any warehousing tools?”

“What is your understanding of ELT pipelines?”

🚀 Steps to Run (My Setup)

Start Kafka, Zookeeper, MinIO & Airflow

docker-compose up -d


Run producer

python producer/producer.py


Run consumer

python consumer/consumer.py


Trigger Airflow DAG
This loads MinIO → Snowflake Bronze

Run DBT models

dbt run


Open Power BI
Connect to Snowflake Gold models.

📊 Final Dashboard (My Deliverables)

Candlestick chart

Price trendline

Symbol-level KPI cards

Change % charts

Tree map for stock comparison

👤 Author

Mahak Choubey
Data Engineering & Analytics Enthusiast
📧 2003mahakchoubey@gmail.com

🔗 LinkedIn: https://www.linkedin.com/in/mahak-choubey-a38b90289
