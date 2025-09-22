import psycopg2
import os

# Подключение к БД через переменную окружения
conn = psycopg2.connect(os.getenv('DB_URL'))
cur = conn.cursor()

# Создание таблицы для whitelist
cur.execute("""
CREATE TABLE IF NOT EXISTS allowed_users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(255)
)
""")

conn.commit()
cur.close()
conn.close()
print("Table created successfully")