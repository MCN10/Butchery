FROM python:3.8-alpine 

ENX PATH="/scripts:${PATH}"

COPY ./requirements.txt /requiremnts.txt
RUN apk add -- uodate --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del . tmp

RUN mkdir /Butchery
COPY ./Butchery /Butchery
WORKDIR /Butchery
COPY ./scripts /scripts 

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static 

RUN adduser -D user 
RUN chown -R user:user /vol 
RUN chmod -R 755 /vol/web 
USER user 

CMD ["entrypoint.sh"]

