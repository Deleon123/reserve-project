FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python manage.py makemigrations app && python manage.py migrate && python manage.py runserver 0.0.0.0:8000" ]
ENTRYPOINT ["/app/django.sh"]