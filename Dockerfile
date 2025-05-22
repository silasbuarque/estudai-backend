FROM python:3.13.2-slim

WORKDIR /apps

COPY requirements.txt .

RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--reload"]