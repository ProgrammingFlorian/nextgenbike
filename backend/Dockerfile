FROM python:3.9
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY ./cloudprocessing/*.py /app/cloudprocessing/
COPY ./server /app/server/

ENV FLASK_APP=server/app/__init__.py
CMD flask run