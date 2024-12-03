from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
import re

# File path to your SQL script
SQL_FILE_PATH = '/opt/airflow/files/loginLogs-3-64.sql'

# Function to parse SQL file and prepare INSERT statements
def parse_sql_file(**kwargs):
    sql_statements = []
    with open(SQL_FILE_PATH, 'r') as file:
        for line in file:
            # Match the INSERT statement structure
            match = re.match(
                r"insert into LOGIN_LOGS \(user_id, user_ip, device_info, log_date, login_status\) values \('(.*?)', '(.*?)', '(.*?)', to_date\('(.*?)', '.*?'\), (\d)\);",
                line.strip(),
            )
            if match:
                user_id, user_ip, device_info, log_date, login_status = match.groups()

                # Initialize fields
                device_type = "Unknown"
                os = "Unknown"
                browser = "Unknown"
                browser_version = "Unknown"

                # Parsing logic for device_info
                if "iPhone" in device_info:
                    device_type = "iPhone"
                    os_match = re.search(r"iPhone OS ([\d_]+)", device_info)
                    os = os_match.group(1).replace("_", ".") if os_match else "iOS"
                    browser = "Safari"
                    version_match = re.search(r"Version/([\d.]+)", device_info)
                    browser_version = version_match.group(1) if version_match else "Unknown"
                elif "Android" in device_info:
                    device_type = "Android"
                    os_match = re.search(r"Android ([\d.]+)", device_info)
                    os = os_match.group(1) if os_match else "Android"
                    browser = "Chrome" if "Chrome" in device_info else "Unknown"
                    version_match = re.search(r"Chrome/([\d.]+)", device_info)
                    browser_version = version_match.group(1) if version_match else "Unknown"
                elif "Windows" in device_info:
                    device_type = "Windows PC"
                    os_match = re.search(r"Windows NT ([\d.]+)", device_info)
                    os = f"Windows {os_match.group(1)}" if os_match else "Windows"
                    browser = "Chrome" if "Chrome" in device_info else "Unknown"
                    version_match = re.search(r"Chrome/([\d.]+)", device_info)
                    browser_version = version_match.group(1) if version_match else "Unknown"
                elif "Mac OS X" in device_info:
                    device_type = "Mac"
                    os_match = re.search(r"Mac OS X ([\d_]+)", device_info)
                    os = os_match.group(1).replace("_", ".") if os_match else "Mac OS X"
                    browser = "Safari" if "Safari" in device_info else "Unknown"
                    version_match = re.search(r"Version/([\d.]+)", device_info)
                    browser_version = version_match.group(1) if version_match else "Unknown"
                elif "Linux" in device_info and "Android" not in device_info:
                    device_type = "Linux PC"
                    os = "Linux"
                    browser = "Chrome" if "Chrome" in device_info else "Unknown"
                    version_match = re.search(r"Chrome/([\d.]+)", device_info)
                    browser_version = version_match.group(1) if version_match else "Unknown"

                # Prepare INSERT statement for PostgreSQL
                sql = f"""
                INSERT INTO LOGIN_LOGS (user_id, user_ip, device_type, os, browser, browser_version, log_date, login_status)
                VALUES ('{user_id}', '{user_ip}', '{device_type}', '{os}', '{browser}', '{browser_version}', 
                to_timestamp('{log_date}', 'DD-MM-YYYY HH24:MI:SS'), {login_status});
                """
                sql_statements.append(sql)

    # Push SQL statements to XCom for the next task
    kwargs['ti'].xcom_push(key='parsed_sql', value=sql_statements)

# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id='load_login_logs',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    # Task 1: Parse SQL file
    parse_sql_task = PythonOperator(
        task_id='parse_sql_file',
        python_callable=parse_sql_file,
    )

    # Task 2: Insert parsed data into PostgreSQL
    insert_data_task = PostgresOperator(
        task_id='insert_data',
        postgres_conn_id='1',  # Replace with your Postgres connection ID
        sql="{{ task_instance.xcom_pull(task_ids='parse_sql_file', key='parsed_sql') }}",
        autocommit=True,
    )

    # Define task dependencies
    parse_sql_task >> insert_data_task
