FROM python:3.6.3

LABEL Name=dw-findingstore Version=0.0.1
EXPOSE 5000

ENV ES_HOST="elasticsearch"
ENV ES_PORT="9200"
ENV FRONTEND_PORT="5000"

WORKDIR /app
ADD /frontend .
COPY requirements.txt /

RUN pip install -r /requirements.txt

ENTRYPOINT [ "python", "/app/app.py" ]
