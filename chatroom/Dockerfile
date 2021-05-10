#Will be deleted
FROM python:3.8

EXPOSE 5000

WORKDIR /chatroom

COPY requirements.txt /chatroom
RUN pip install  -r requirements.txt --upgrade pip

COPY . /chatroom

RUN pylint --load-plugins pylint_flask chatroom

CMD flask run --host='0.0.0.0'