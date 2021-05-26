FROM python:3.8-alpine
ENV  PYTHONUNBUFFERED=1
RUN  pip install --no-cache requests
COPY reloader /reloader
CMD  ["python3","-m","reloader"]
