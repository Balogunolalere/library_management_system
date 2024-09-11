FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

# Add wait-for-it script
ADD https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Use wait-for-it to wait for the database before starting the app
CMD ["/wait-for-it.sh", "database:5432", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]