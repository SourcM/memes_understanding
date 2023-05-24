FROM python:3.7-slim-stretch

RUN echo "deb http://security.debian.org/debian-security bullseye-security main contrib non-free" > /etc/apt/sources.list

RUN apt-get dist-upgrade

RUN apt-get update

RUN apt -y upgrade 

RUN echo "lsb_release -a"

RUN apt-get install gcc-7 gcc-8

RUN apt-get install manpages-dev

RUN apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY app app/

RUN python app/server.py

EXPOSE 5000

CMD ["python", "app/server.py", "serve"]
