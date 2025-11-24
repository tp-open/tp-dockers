FROM apache/airflow:slim-2.10.5-python3.12
ARG USER_ID=1001

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    telnet \
  # map airflow user to provided UID so host-mounted volumes can match ownership
  && groupmod -g ${USER_ID} airflow 2>/dev/null || true \
  && usermod -u ${USER_ID} -g ${USER_ID} airflow 2>/dev/null || true \
  && chown -R ${USER_ID}:${USER_ID} /opt/airflow /home/airflow 2>/dev/null || true \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow
# Install additional packages
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
COPY alerts /opt/airflow/alerts
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"

