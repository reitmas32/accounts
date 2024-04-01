FROM python:3.12

ENV PYTHONUNBUFFERED 1

# Install requirements
RUN apt-get update \
    && pip install --upgrade pip \
    && pip install -U poetry \
    && pip install gunicorn uvicorn[standard]

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN cd /tmp \
    && poetry export -f requirements.txt --output /app/requirements.txt --without-hashes --dev \
    && pip install --no-warn-script-location --disable-pip-version-check --no-cache-dir -r /app/requirements.txt

COPY ../src /app/
EXPOSE 9000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--workers", "2"]
