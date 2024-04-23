FROM python:3
COPY . /code
WORKDIR /code
EXPOSE 80
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]
