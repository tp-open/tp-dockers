# Airflow
[![Docker Hub](https://img.shields.io/badge/%20-DockerHub-blue?logo=docker&style=plastic)](https://hub.docker.com/r/tpopen/airflow)
![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/tpopen/airflow?sort=date&style=plastic)

## Overview

This custom Docker image extends the official [Apache Airflow](https://airflow.apache.org/) image with additional packages and functionality to enhance task execution and alerting.  

📦 **Dockerfile** available at: [github.com/tp-open/tp-dockers/airflow](https://github.com/tp-open/tp-dockers/tree/master/airflow)

## Features

- **Docker Operator Support**: Includes the Docker provider for container-based task execution.
- **Telegram Notifications**: Sends task success and failure alerts via Telegram using `task_success_callback` and `task_failure_callback`.

## Environment Variables

Set the following environment variables to enable Telegram notifications:

| Variable         | Description                                                  |
|------------------|--------------------------------------------------------------|
| `TG_CHAT_TOKEN`  | Telegram bot token (from [BotFather](https://t.me/BotFather)) |
| `TG_CHAT_ID`     | Telegram chat ID (user or group)                             |

## Usage

### Telegram Alerts Example

Send Telegram alerts on task success or failure:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from alerts.telegram import task_failure_callback, task_success_callback

def success_task():
    print("Hello World")

def zero_division():
    return 1 / 0

with DAG(
    dag_id="hello_world_dag",
    start_date=datetime.today() - timedelta(days=1),
    schedule=None,
    catchup=False,
    owner_links={"airflow": "https://airflow.apache.org"},
) as dag:

    success = PythonOperator(
        task_id="success_task",
        python_callable=success_task,
        on_success_callback=task_success_callback
    )

    failure = PythonOperator(
        task_id="fail_task",
        python_callable=zero_division,
        on_failure_callback=task_failure_callback
    )
```

### Docker Operator Example

Run a container as a task using the Docker operator:

```python
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="hello_docker",
    start_date=datetime.today() - timedelta(days=1),
    schedule=None,
    catchup=False,
    owner_links={"airflow": "https://airflow.apache.org"},
) as dag:

    task = DockerOperator(
        task_id='hello_world',
        image='hello-world',
        container_name='hello-world',
        docker_url='unix://var/run/docker.sock',
        mount_tmp_dir=False,
        auto_remove=True
    )
```

## License
[MIT License](https://github.com/tp-open/tp-dockers/blob/master/LICENSE)