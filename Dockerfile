FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
