FROM python:3

WORKDIR /app
COPY . /app

RUN apt-get update
COPY ./requirements1.txt /app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 2827

ENTRYPOINT ["python3"]
CMD ["routes.py"]

