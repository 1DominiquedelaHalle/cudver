# client.py
import socket

# Настройки для подключения к серверу
HOST = '127.0.0.1'  # IP-адрес сервера
PORT = 65432        # Порт сервера

def send_query(query):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(query.encode())
        
        # Получение результата от сервера
        data = s.recv(1024).decode()
        print("Результат запроса:", data)

if __name__ == "__main__":
    # Пример запроса: получение всех продуктов типа "Food"
    query = "SELECT * FROM products WHERE type = 'Food';"
    send_query(query)
