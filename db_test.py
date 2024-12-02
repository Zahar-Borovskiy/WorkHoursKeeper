import sqlite3

def view_data():
    conn = sqlite3.connect('work_hours.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM work_hours')
    rows = c.fetchall()  # Извлекаем все записи
    
    for row in rows:
        print(row)  # Печатаем каждую запись
    
    conn.close()

if __name__ == '__main__':
    view_data()