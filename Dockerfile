# Pull the base image
FROM python:3.10.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# GDAL
RUN  sudo apt-get install binutils libproj-dev gdal-bin
# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
