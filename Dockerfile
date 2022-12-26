FROM python:3.9

ENV API_KEY a9780073

WORKDIR /app

VOLUME ["/app"]

COPY requirements.txt requirements.txt 

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "main.py"]