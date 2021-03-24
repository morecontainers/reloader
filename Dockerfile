FROM python:3.8-alpine
ENV  PYTHONUNBUFFERED=1
RUN  pip install --no-cache requests
COPY reloader.py .
CMD  ["python3", "reloader.py"]
