FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1


WORKDIR /app


# dependências 
RUN apt-get update && apt-get install -y build-essential default-libmysqlclient-dev pkg-config && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


COPY app /app/app


EXPOSE 8000
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]