FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
  pkg-config \
  build-essential \
  default-libmysqlclient-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install  -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]

