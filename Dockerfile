FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/app
COPY ./requirements.txt ./

RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install -r ./requirements.txt

COPY . .

RUN useradd admin && \
    chown -R admin:admin ./
USER admin

CMD python3 ${FILE_NAME}
