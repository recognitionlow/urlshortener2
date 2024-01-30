FROM python:3.11-slim

WORKDIR /app
ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get update
RUN apt-get install -y procps
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN mkdir ~/logs

EXPOSE 80

CMD ["python", "-u", "logger.py"]

