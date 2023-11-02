FROM python:3.9
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY ./cloudprocessing/*.py cloudprocessing/

COPY ./server/app/ server/app/
COPY ./server/migrations/ server/migrations/
COPY ./server/*.py server/

COPY ./entrypoint.sh ./entrypoint.sh

RUN chmod u+x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]