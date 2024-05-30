FROM python:3

WORKDIR /usr/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

ENV PYTHONUNBUFFERED=1
ENV SERIAL_PORT /dev/ttyUSB0

CMD [ "python", "./main.py" ]