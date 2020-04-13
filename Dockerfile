FROM python:slim

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y npm

ENV HOST=0.0.0.0
ENV PORT=5000
ENV NSSL_SERVER_URL=https://nssl.susch.eu

EXPOSE 5000

COPY requirements /app/requirements
COPY src/app /app/app
COPY src/base /app/base
COPY src/nssl /app/nssl
COPY src/config.py /app/config.py
COPY src/wsgi.py /app/wsgi.py
COPY run.sh /app/run.sh
COPY install.sh /app/install.sh

WORKDIR /app
RUN pip install -r requirements/production.txt
RUN sh install.sh

ENTRYPOINT [ "/bin/sh" ]

CMD [ "run.sh" ]
