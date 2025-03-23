# Airflow

## Overview

This custom Docker image extends the official [Apache Airflow](https://airflow.apache.org/) image by adding additional packages and features for enhanced functionality.

## Features

- **Docker operator**: Installed docker provider.
- **Telegram Alerts**: Integrates `task_failure_callback`, `task_success_callback` to send failure/success notifications via Telegram.

## Environment Variables

Set the following environment variables to enable Telegram notifications:

| Variable       | Description                                    |
|----------------|------------------------------------------------|
| `TG_CHAT_TOKEN` | Telegram bot token (from [BotFather](https://t.me/BotFather)) |
| `TG_CHAT_ID`    | Telegram user or group chat ID               |

## Usage

Example for sending Telegram alerts on task failure:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from alerts.telegram import task_failure_callback

with DAG(dag_id="alert_test", ...) as dag:
    task = PythonOperator(
        task_id="fail_task",
        python_callable=lambda: 1/0,
        on_failure_callback=task_failure_callback,
    )

```
