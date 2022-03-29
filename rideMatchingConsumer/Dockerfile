# https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
# https://x-team.com/blog/set-up-rabbitmq-with-docker-compose/

FROM python:3.8.10-alpine3.13

RUN mkdir -p /usr/src
WORKDIR /usr/src

COPY . /usr/src

ARG PRODUCER_IP
ENV IP_PROD $PRODUCER_IP
ARG PRODUCER_PORT
ENV PORT_PROD $PRODUCER_PORT
ARG CONSUMER1_IP
ENV IP_CONSUMER $CONSUMER1_IP
ARG CONSUMER1_NAME
ENV NAME_CONSUMER $CONSUMER1_NAME

#set python
RUN python3 -m pip install --upgrade pip
RUN pip3 install virtualenv
RUN virtualenv cc_env
RUN . cc_env/bin/activate

# install dependencies 
RUN pip3 install pika
RUN pip3 install requests
RUN pip3 install uuid

#RUN Python
CMD python3 -u consumer.py ${IP_PROD} ${PORT_PROD} ${IP_CONSUMER} ${NAME_CONSUMER}