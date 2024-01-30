FROM python:3.11-slim

WORKDIR /app
ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get update
RUN apt-get install -y openssh-client
RUN apt-get install -y sshpass
RUN apt-get install -y curl
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

EXPOSE 8080

CMD ["python", "monitor.py", "10.128.1.42", "10.128.2.42", "10.128.3.42", "10.128.4.42"]
