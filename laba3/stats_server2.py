import sqlite3

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Создаем базу данных для хранения данных
conn = sqlite3.connect('log.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS transactions (operation TEXT, time TEXT, time_speed TEXT)')
conn.commit()


# Это создает наш прокси-сервер
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = SimpleXMLRPCServer(('localhost', 7000))
print("Listening on port 7000...")
def stats (cashe):
    c.execute("INSERT INTO transactions (operation,time,time_speed ) VALUES (?,?,?)", (cashe[1],cashe[0],cashe[2]))
    conn.commit()
    return True

def data_search(criteria1, criteria2, criteria3):

    # Подключение к базе данных
    conn = sqlite3.connect('log.db')
    cursor = conn.cursor()

    # Выполнение запроса с поиском по трем критериям
    query = f"SELECT * FROM transactions WHERE operation = ? AND time = ? AND time_speed < ?"
    cursor.execute(query, (criteria1, criteria2, criteria3))

    # Вывод результатов
    results = cursor.fetchall()
    return results

server.register_function(data_search, 'data_search')
server.register_function(stats, 'stats')
server.serve_forever()
