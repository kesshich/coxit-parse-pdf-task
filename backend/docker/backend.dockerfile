FROM pdf-parser-deps:latest

WORKDIR /app

COPY . .

CMD ["python", "-m", "backend"]
