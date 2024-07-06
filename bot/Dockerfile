FROM python:3.10

ENV TZ Europe/Moscow

RUN addgroup --system app && adduser --system --group app

WORKDIR /bot
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt && chmod 777 .
COPY . .

USER app
CMD ["python3", "-u", "main.py"]