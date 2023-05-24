#RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list

RUN docker system prune -a

FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install -y 

RUN git python3-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY app app/

RUN python app/server.py

EXPOSE 5000

CMD ["python", "app/server.py", "serve"]
