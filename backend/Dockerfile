FROM python:3.9
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY ./cloudprocessing/*.py /cloudprocessing/
COPY ./server server/

RUN chmod u+x server/entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]