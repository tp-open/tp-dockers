FROM apache/airflow:slim-2.10.5-python3.12
ARG USER_ID=1001

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    telnet \
  && if ! getent group ${USER_ID} >/dev/null 2>&1; then \
       groupadd -g ${USER_ID} airflow; \
     fi \
  && if ! id -u airflow >/dev/null 2>&1; then \
       useradd -u ${USER_ID} -g ${USER_ID} -m -d /home/airflow -s /bin/bash airflow; \
     else \
       usermod -u ${USER_ID} -g ${USER_ID} airflow 2>/dev/null || true; \
     fi \
  && mkdir -p /opt/airflow /home/airflow \
  && chown -R ${USER_ID}:${USER_ID} /opt/airflow /home/airflow 2>/dev/null || true \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow
# Install additional packages
COPY requirements.txt /home/airflow/requirements.txt
RUN pip install --no-cache-dir -r /home/airflow/requirements.txt
COPY alerts /opt/airflow/alerts
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"

