FROM ubuntu:latest

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app
COPY ./requirements.txt ./

RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install -r ./requirements.txt

COPY . .

RUN useradd admin && \
    chown -R admin:admin ./
USER admin

CMD python3 ${FILE_NAME}
