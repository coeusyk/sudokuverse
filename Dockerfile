FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]