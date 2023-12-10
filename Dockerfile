# Pull the base image
FROM python:3.10.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]