from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sqlite3
from datetime import datetime, timedelta

TOCEN: Final = "8074876908:AAH5nB7FL-t99PkIP-JZXfAt_DvSA3YWNNk"

BOT_USERNAME: Final = '@employee_comedor_bot'

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('work_hours.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS work_hours (
            user_id INTEGER,
            date TEXT,
            hours INTEGER,
            PRIMARY KEY (user_id, date)
        )
    ''')
    conn.commit()
    conn.close()

async def add_hours_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if len(context.args) == 1 and context.args[0].isdigit():
        hours = int(context.args[0])
        date = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect('work_hours.db')
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO work_hours (user_id, date, hours)
            VALUES (?, ?, ?)
        ''', (user_id, date, hours))
        conn.commit()
        conn.close()
        await update.message.reply_text(f'Добавлено {hours} часов за сегодняшний день.')
    else:
        await update.message.reply_text('Используйте: /add_hours X, где X - число рабочих часов.')

async def week_hours_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    conn = sqlite3.connect('work_hours.db')
    c = conn.cursor()
    c.execute('''
        SELECT SUM(hours) FROM work_hours
        WHERE user_id = ? AND date BETWEEN ? AND ?
    ''', (user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    total_hours = c.fetchone()[0]
    conn.close()
    await update.message.reply_text(f'Общее количество часов за последнюю неделю: {total_hours or 0}.')

async def two_weeks_hours_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)
    conn = sqlite3.connect('work_hours.db')
    c = conn.cursor()
    c.execute('''
        SELECT SUM(hours) FROM work_hours
        WHERE user_id = ? AND date BETWEEN ? AND ?
    ''', (user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    total_hours = c.fetchone()[0]
    conn.close()
    await update.message.reply_text(f'Общее количество часов за последние две недели: {total_hours or 0}.')

async def month_hours_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    conn = sqlite3.connect('work_hours.db')
    c = conn.cursor()
    c.execute('''
        SELECT SUM(hours) FROM work_hours
        WHERE user_id = ? AND date BETWEEN ? AND ?
    ''', (user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    total_hours = c.fetchone()[0]
    conn.close()
    await update.message.reply_text(f'Общее количество часов за последний месяц: {total_hours or 0}.')

# Основной блок для запуска бота
if __name__ == '__main__':
    init_db()
    app = Application.builder().token("YOUR_TOKEN_HERE").build()

    app.add_handler(CommandHandler('add_hours', add_hours_command))
    app.add_handler(CommandHandler('week_hours', week_hours_command))
    app.add_handler(CommandHandler('two_weeks_hours', two_weeks_hours_command))
    app.add_handler(CommandHandler('month_hours', month_hours_command))

    # Запуск polling
    app.run_polling(poll_interval=3)
