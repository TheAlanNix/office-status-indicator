FROM python:3-bookworm

WORKDIR /app

ADD requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /app/data

ADD *.py /app/

CMD ["python", "-u", "office_status_indicator.py"]
