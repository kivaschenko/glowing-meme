FROM python:3.10-bullseye

WORKDIR /app
RUN apt-get update
RUN apt-get install -y gettext postgresql-client gdal-bin python3-gdal

COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]