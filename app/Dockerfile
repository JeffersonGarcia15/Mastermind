# Credits to Zoltan Buzas: https://stackoverflow.com/questions/62715570/failing-to-install-psycopg2-binary-on-new-docker-container
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
