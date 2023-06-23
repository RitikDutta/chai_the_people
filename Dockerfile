FROM python:3.7-alpine

COPY . /app
WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev linux-headers

CMD ["python", "app.py"]

