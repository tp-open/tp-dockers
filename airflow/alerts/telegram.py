import requests
import os
import logging

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
logger = logging.getLogger(__name__)

def task_failure_callback(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    execution_date = context['execution_date']
    message = f"❌ DAG: {dag_id}\nTask: {task_id}\nDate: {execution_date}\nStatus: FAILED"

    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, json=payload)
    except Exception as e:
        logger.error(f"Telegram error: {e}")

def task_success_callback(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    execution_date = context['execution_date']
    message = f"✅ DAG: {dag_id}\nTask: {task_id}\nDate: {execution_date}\nStatus: SUCCESS"

    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        logger.error(f"Telegram error: {e}")
