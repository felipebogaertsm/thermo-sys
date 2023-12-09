FROM ubuntu:latest

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install \
    python3.11 \
    python3-pip 

WORKDIR /usr/app
COPY ./requirements.txt ./

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r ./requirements.txt

COPY ./ ./

RUN useradd admin
RUN chown -R admin:admin ./
USER admin

ENTRYPOINT ["python3", ${FILE_NAME}]