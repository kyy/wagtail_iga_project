import csv
import sqlite3


conn = sqlite3.connect(r'C:\db.sqlite3')
c = conn.cursor()
print("подключен к SQLite")

def insert_db(name):
    try:
        c.execute("""INSERT INTO products_productpage VALUES (?,?,?)""", name)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
# путь к БД которую нужно спарсить
file = r'C:\load.txt'
with open(file, 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE)
    i = 1
    for row in spamreader:
        row.insert(0, i)
        insert_db(row)
        print(i)
        i += 1
    conn.commit()
    print("Записи успешно вставлены в таблицу", c.rowcount)
if conn:
    conn.close()
    print("Соединение с SQLite закрыто")