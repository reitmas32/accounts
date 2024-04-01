FROM python:3.12-alpine3.18

ENV PYTHONUNBUFFERED 1

# Install requirements
RUN pip install --upgrade pip \
    && pip install -U ruff

# Define the working directory
WORKDIR /app

# Copy the project files
COPY ./pyproject.toml ./poetry.lock* /tmp/
COPY ../src /app/

# Change to the app directory
WORKDIR /app

# Run Ruff check
CMD ["ruff", "check", "."]
