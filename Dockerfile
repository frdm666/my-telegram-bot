FROM python:3.12-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/bot.py .
COPY app/init_db.py .
CMD ["python", "bot.py"]
