FROM python:3.12-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY templates ./templates
ENV PYTHONPATH=. 
# Добавлено для указания корня пакета
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]