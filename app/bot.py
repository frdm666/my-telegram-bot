import os
import psycopg2
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("Доступ запрещён")
        return
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id != 179788438:  # Замените на ваш Telegram user_id
        await update.message.reply_text("Только админ может добавлять пользователей")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Использование: /add_user <user_id>")
        return
    try:
        new_user_id = int(context.args[0])
        conn = psycopg2.connect(os.getenv('DB_URL'))
        cur = conn.cursor()
        cur.execute("INSERT INTO allowed_users (user_id, username) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (new_user_id, 'Unknown'))
        conn.commit()
        cur.close()
        conn.close()
        await update.message.reply_text(f"Пользователь {new_user_id} добавлен")
    except ValueError:
        await update.message.reply_text("Неверный user_id")

def is_allowed(user_id: int) -> bool:
    conn = psycopg2.connect(os.getenv('DB_URL'))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM allowed_users WHERE user_id = %s", (user_id,))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count > 0

def main() -> None:
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise ValueError("BOT_TOKEN not set in environment")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("add_user", add_user))
    app.run_polling()

if __name__ == '__main__':
    main()