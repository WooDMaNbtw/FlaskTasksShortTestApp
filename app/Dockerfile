FROM python:3.10-slim

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

ENV FLASK_APP=app.py

EXPOSE 8090

CMD ["flask", "run", "--host=0.0.0.0"]
