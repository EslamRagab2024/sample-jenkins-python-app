FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir psycopg2-binary redis
COPY app.py .
EXPOSE 8000
CMD ["python", "app.py"]