#%Y_%m_%d_%H_%M_%S
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import datetime
import time

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

proxy = xmlrpc.client.ServerProxy("http://localhost:8018")
stat_server = xmlrpc.client.ServerProxy("http://localhost:7000")
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)
print("Listening on port 8000...")
def toFixed(numObj, digits=3):
    return f"{numObj:.{digits}f}"

def stats(cashe):
    try:
        stat_server.stats(cashe)
    except Exception as e:
        return 'Ошибка, срервер вне зоны доступа'

# Тест
def ping():
    cashe = []
    start_time = time.time()
    date_received = datetime.datetime.now().strftime('%Y_%m_%d')
    cashe.append(date_received)
    type = ('ping')  # Отправляем тип операции перед началом
    cashe.append(type)
    ping_result = proxy.ping()
    end_time = time.time()
    res = end_time - start_time
    cashe.append(toFixed(res))
    stats(cashe)
    return ping_result
server.register_function(ping, 'ping')

# Время сервера
def now():
    cashe = []
    start_time = time.time()
    date_received = datetime.datetime.now().strftime('%Y_%m_%d')
    cashe.append(date_received)
    type = ('now')  # Отправляем тип операции перед началом
    cashe.append(type)
    result = proxy.now()
    end_time = time.time()
    res = end_time - start_time
    cashe.append(toFixed(res))
    stats(cashe)
    return result
server.register_function(now, 'now')

# Отображение строкового вида, типа и значений
def show_type(arg):
    cashe = []
    start_time = time.time()
    date_received = datetime.datetime.now().strftime('%Y_%m_%d')
    cashe.append(date_received)
    type = ('show_type')  # Отправляем тип операции перед началом
    cashe.append(type)
    View, type, value = proxy.type(arg)
    end_time = time.time()
    res = end_time - start_time
    cashe.append(toFixed(res))
    stats(cashe)
    return View, type, value
server.register_function(show_type, 'type')

# Сумма
def summa(a, b):
    cashe = []
    start_time = time.time()
    date_received = datetime.datetime.now().strftime('%Y_%m_%d')
    cashe.append(date_received)
    type = ('summa')  # Отправляем тип операции перед началом
    cashe.append(type)
    result = proxy.summa(a,b)
    end_time = time.time()
    res = end_time - start_time
    cashe.append(toFixed(res))
    stats(cashe)
    return result
server.register_function(summa, 'summa')

# Степень
def pow(a, b):
    cashe = []
    start_time = time.time()
    date_received = datetime.datetime.now().strftime('%Y_%m_%d')
    cashe.append(date_received)
    type = ('pow')  # Отправляем тип операции перед началом
    cashe.append(type)
    result = proxy.pow(a,b)
    end_time = time.time()
    res = end_time - start_time
    cashe.append(toFixed(res))
    stats(cashe)
    return result
server.register_function(pow, 'pow')

# Проверка нахождения клиента в черном списке c использованием Pandas Data Frame
def black_list_check(list):
    cashe = []
    start_time = time.time()
    date_received = datetime.datetime.now().strftime('%Y_%m_%d')
    cashe.append(date_received)
    type = ('black_list_check')  # Отправляем тип операции перед началом
    cashe.append(type)
    result = proxy.black_list_check(list)
    end_time = time.time()
    res = end_time - start_time
    cashe.append(toFixed(res))
    stats(cashe)
    return result
server.register_function(black_list_check, 'black_list_check')

# Бинарная передача данных
# def send_back_binary(bin_data):
#     cashe = []
#     start_time = time.time()
#     date_received = datetime.datetime.now().strftime('%Y_%m_%d')
#     cashe.append(date_received)
#     type = ('send_back_binary')  # Отправляем тип операции перед началом
#     cashe.append(type)
#     result = proxy.send_back_binary(bin_data)
#     end_time = time.time()
#     res = end_time - start_time
#     cashe.append(toFixed(res))
#     stats(cashe)
#     return result
# server.register_function(send_back_binary, 'send_back_binary')

# Инверсия цвета
# На вход изображение RGB размерности (M, N, 3) со значениями 0-255
def color_inversion(input_file):
    cashe = []
    start_time = time.time()
    date_received = datetime.datetime.now().strftime('%Y_%m_%d')
    cashe.append(date_received)
    type = ('color_inversion')  # Отправляем тип операции перед началом
    cashe.append(type)
    result1, result2 = proxy.color_inversion(input_file)
    end_time = time.time()
    res = end_time - start_time
    cashe.append(toFixed(res))
    stats(cashe)
    return result1, result2
server.register_function(color_inversion, 'color_inversion')


# Бинаризация изображения по порогу
def binarize_image(file_name, threshold):
    cashe = []
    start_time = time.time()
    date_received = datetime.datetime.now().strftime('%Y_%m_%d')
    cashe.append(date_received)
    type = ('binarized_image')  # Отправляем тип операции перед началом
    cashe.append(type)
    result = proxy.binarize_image(file_name, threshold)
    end_time = time.time()
    res = end_time - start_time
    cashe.append(toFixed(res))
    stats(cashe)
    return result
server.register_function(binarize_image,'binarize_image')

# Поворот изображения
def rotated_image(image_path):
    cashe = []
    start_time = time.time()
    date_received = datetime.datetime.now().strftime('%Y_%m_%d')
    cashe.append(date_received)
    type = ('rotated_image')  # Отправляем тип операции перед началом
    cashe.append(type)
    result = proxy.rotated_image(image_path)
    end_time = time.time()
    res = end_time - start_time
    cashe.append(toFixed(res))
    stats(cashe)
    return result
server.register_function(rotated_image,'rotated_image')

server.serve_forever()