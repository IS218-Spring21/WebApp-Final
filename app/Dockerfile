FROM python:3.8

EXPOSE 443

WORKDIR /app

COPY requirements.txt /app
RUN pip install  -r requirements.txt --upgrade pip

COPY . /app

RUN pylint --load-plugins pylint_flask app
RUN pylint --load-plugins pylint_flask main
RUN pylint --load-plugins pylint_flask chatroom

CMD python app.py