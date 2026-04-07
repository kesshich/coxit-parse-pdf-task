FROM pdf-parser-backend-deps:latest

WORKDIR /app

COPY . .

CMD ["python", "-m", "backend"]
