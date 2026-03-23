ARG DEPS_TAG=latest
FROM pdf-parser-backend-deps:${DEPS_TAG}

WORKDIR /app

# Copy the full project source on top of the pre-built deps layer
COPY . .

CMD ["python", "-m", "backend"]

