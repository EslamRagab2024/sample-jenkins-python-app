FROM python:3.11-alpine
WORKDIR /app
COPY app.py .
EXPOSE 8000
CMD ["python", "app.py"]