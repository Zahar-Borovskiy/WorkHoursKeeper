import sqlite3
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext



# Создание или подключение к базе данных
conn = sqlite3.connect('work_hours.db', check_same_thread=False)
cursor = conn.cursor()

# Проверяем существование таблицы и создаем ее, если нужно
cursor.execute("""
CREATE TABLE IF NOT EXISTS hours (
    user_id INTEGER,
    date TEXT,
    hours INTEGER,
    PRIMARY KEY (user_id, date)
)
""")
conn.commit()

# Функция добавления рабочего времени
def add_hours(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    date = datetime.now().strftime('%Y-%m-%d')
    try:
        hours = int(context.args[0])
    except (IndexError, ValueError):
        update.message.reply_text('Пожалуйста, укажите количество часов в формате "/add_hours X", где X - число.')
        return

    cursor.execute("INSERT OR REPLACE INTO hours (user_id, date, hours) VALUES (?, ?, COALESCE((SELECT hours FROM hours WHERE user_id = ? AND date = ?) + ?, 0))", (user_id, date, user_id, date, hours))
    conn.commit()
    update.message.reply_text(f'Добавлено {hours} часа(ов) за {date}.')

# Функция подсчета часов за период
def calculate_hours(user_id, days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    cursor.execute("SELECT SUM(hours) FROM hours WHERE user_id = ? AND date BETWEEN ? AND ?", (user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    result = cursor.fetchone()[0]
    return result if result else 0

# Команды для подсчета
def get_week_hours(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    hours = calculate_hours(user_id, 7)
    update.message.reply_text(f'Вы отработали {hours} часов за последнюю неделю.')

def get_two_weeks_hours(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    hours = calculate_hours(user_id, 14)
    update.message.reply_text(f'Вы отработали {hours} часов за последние две недели.')

def get_month_hours(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    hours = calculate_hours(user_id, 30)
    update.message.reply_text(f'Вы отработали {hours} часов за последний месяц.')

# Настройка бота
def main():
    updater = Updater("YOUR_BOT_TOKEN")

    updater.dispatcher.add_handler(CommandHandler("add_hours", add_hours))
    updater.dispatcher.add_handler(CommandHandler("week_hours", get_week_hours))
    updater.dispatcher.add_handler(CommandHandler("two_weeks_hours", get_two_weeks_hours))
    updater.dispatcher.add_handler(CommandHandler("month_hours", get_month_hours))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
