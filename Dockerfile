FROM python:3.7-slim-stretch
RUN sed -i s/deb.debian.org/archive.debian.org/g /etc/apt/sources.list
RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY app app/

RUN python app/server.py

EXPOSE 5000

CMD ["python", "app/server.py", "serve"]
