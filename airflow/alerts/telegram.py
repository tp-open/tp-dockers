import requests
import os
import logging
from urllib.parse import quote
from airflow.configuration import conf

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
logger = logging.getLogger(__name__)

def _base_url():
    return (os.getenv("AIRFLOW_BASE_URL") or conf.get("api", "base_url", fallback="")).rstrip("/")

def _log_url(context):
    ti = context['task_instance']
    dag_id = context['dag'].dag_id
    run_id = quote(context['run_id'], safe='')
    return f"{_base_url()}/dags/{dag_id}/runs/{run_id}/tasks/{ti.task_id}?try_number={ti.try_number}"

def _short_error(exception, limit=300):
    if not exception:
        return "unknown"
    lines = [l.strip() for l in str(exception).splitlines() if l.strip()]
    text = f"{type(exception).__name__}: {lines[-1] if lines else ''}"
    return text if len(text) <= limit else text[:limit] + "..."

def _build_message(context, icon, status, error=None):
    lines = [
        f"{icon} DAG: {context['dag'].dag_id}",
        f"Task: {context['task_instance'].task_id}",
        f"Date: {context['logical_date']}",
        f"Status: {status}",
    ]
    if error is not None:
        lines.append(f"Error: {error}")
    lines.append(f"Log: {_log_url(context)}")
    return "\n".join(lines)

def _send(message):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TG_CHAT_ID, "text": message})
    except Exception as e:
        logger.error(f"Telegram error: {e}")

def task_failure_callback(context):
    error = _short_error(context.get('exception'))
    _send(_build_message(context, "❌", "FAILED", error))

def task_success_callback(context):
    _send(_build_message(context, "✅", "SUCCESS"))
