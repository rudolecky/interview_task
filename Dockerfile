FROM python:3.9-slim
RUN pip install --upgrade pip
COPY /app /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt
EXPOSE 5432

CMD python /usr/src/app/app.py