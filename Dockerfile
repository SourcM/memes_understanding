FROM python:3.7-slim-stretch

#RUN apt-get update
RUN ["/bin/bash", "-c", "apt update"]

RUN apt-get -y upgrade 

RUN apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY app app/

RUN python app/server.py

EXPOSE 5000

CMD ["python", "app/server.py", "serve"]
