FROM apache/airflow:slim-2.10.5-python3.12

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         telnet \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow
# Install additional packages
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
COPY alerts /opt/airflow/alerts
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"

