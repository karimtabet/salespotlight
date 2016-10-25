FROM python:3

COPY ["__init__.py", "main.py", "mq.py", "requirements.txt", "./"]

COPY ["spiders/", "/spiders/"]

RUN pip install -r requirements.txt

CMD python main.py