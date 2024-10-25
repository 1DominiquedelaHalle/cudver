# server.py
import sqlite3
import socket

# Настройки для сервера
HOST = '127.0.0.1'  # Локальный хост
PORT = 65432        # Порт для прослушивания

# Создание и настройка таблицы в базе данных
def create_database():
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    
    # Создание таблицы продуктов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id_product INTEGER PRIMARY KEY,
            name_product TEXT NOT NULL,
            type TEXT NOT NULL
        )
    ''')
    
    # Инициализация таблицы продуктов
    products = [
        (1, 'Apple', 'Food'),
        (2, 'Bread', 'Food'),
        (3, 'Milk', 'Food'),
        (4, 'Cheese', 'Food'),
        (5, 'Orange Juice', 'Food'),
        (6, 'Smartphone X', 'Electronics'),
        (7, 'Laptop Pro', 'Electronics'),
        (8, 'Gaming Console Z', 'Entertainment'),
        (9, 'Wireless Headphones', 'Accessories'),
        (10, 'Smartwatch 5', 'Wearables')
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO products VALUES (?, ?, ?)', products)
    connection.commit()
    connection.close()

# Функция обработки запроса SQL и возврата данных клиенту
def process_request(query):
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result

# Запуск сервера
def run_server():
    create_database()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен на {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Подключен клиент: {addr}")
                
                # Получение запроса от клиента
                query = conn.recv(1024).decode()
                print(f"Запрос от клиента: {query}")
                
                # Выполнение SQL-запроса и отправка данных обратно
                try:
                    result = process_request(query)
                    conn.sendall(str(result).encode())
                except sqlite3.Error as e:
                    conn.sendall(f"Ошибка: {e}".encode())

if __name__ == "__main__":
    run_server()

