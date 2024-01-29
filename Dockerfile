# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install curl, sudo, and procps
# Install required packages
RUN apt-get update && \
    apt-get install -y curl wget sudo procps influxdb && \
    rm -rf /var/lib/apt/lists/*


# Set the working directory in the containerdocker-compose up --build
WORKDIR /usr/src/app
# Copy the current directory contents into the container at /usr/src/app
#COPY . /usr/src/app

COPY requirements.txt /usr/src/app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r  requirements.txt
RUN pip install gunicorn
RUN pip install docker
RUN pip install psycopg2-binary
RUN pip install influxdb
RUN pip install pymonetdb




# Run the application
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
