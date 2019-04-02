FROM python:3.7

RUN git clone https://github.com/mysql/mysql-connector-python.git
WORKDIR mysql-connector-python
RUN python ./setup.py build
RUN python ./setup.py install

RUN mkdir /app

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["easy_book.py"]
