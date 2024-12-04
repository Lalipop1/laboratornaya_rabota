from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import datetime
import pandas as pd
import pickle
from PIL import Image


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = SimpleXMLRPCServer(("localhost", 8008))
print("Listening on port 8008...")


stats_server = xmlrpc.client.ServerProxy("http://localhost:8018")

# Добавление в лог через сервер
def add_log(log_line):
    try:  stats_server.add_log(log_line)
    except Exception as e:
        print('нет соединения'+log_line+'\n'+str(e))

# Тест
def ping():
    add_log('ping')
    return True
server.register_function(ping, 'ping')

# Время сервера
def now():
    add_log('now')
    return datetime.datetime.now()
server.register_function(now, 'now')

# Отображение строкового вида, типа и значений
def show_type(arg):
    add_log('show_type')
    return (str(arg), str(type(arg)), arg)
server.register_function(show_type, 'type')

# Сумма
def summa(a, b):
    add_log('summa')
    return a + b
server.register_function(summa, 'summa')

# Степень
def pow(a, b):
    add_log('pow')
    return a ** b
server.register_function(pow, 'pow')

# Проверка нахождения клиента в черном списке c использованием Pandas Data Frame
def black_list_check(list):
    add_log('black_list_check')
    frame = pd.read_csv('bad_boys2.csv', header=0, sep=',', encoding='utf8')
    exist = [(frame['Surname'] == list[0]) & (frame['Name'] == list[1]) & (frame['Patronym'] == list[2]) | (frame['Birth'] == list[3])]
    yes = (frame.index[frame['Surname'] == list[0]]) == (frame.index[frame['Name'] == list[1]]) == (frame.index[frame['Patronym'] == list[2]]) == (frame.index[frame['Birth'] == list[3]])
    if yes and exist:
        return (f"{' '.join(list[:3])}: bad_boy")
    else:
        return(f"{' '.join(list[:3])}: good_boy")
server.register_function(black_list_check, 'black_list_check')

# Бинарная передача данных
def send_back_binary(bin_data):
    add_log('send_back_binary')
    data = bin_data.data
    return xmlrpc.client.Binary(data)
server.register_function(send_back_binary, 'send_back_binary')

# Инверсия цвета
# На вход изображение RGB размерности (M, N, 3) со значениями 0-255
def send_back_inversion(input_file):
    add_log('send_back_inversion')
    file = open(input_file, 'rb')
    header = file.read(54)  # прочитать первые 54 байта (заголовок файла BMP)

    bits_per_pixel = int.from_bytes(header[28:30], byteorder='little')

    if bits_per_pixel == 24:
        pixel_data = file.read()
        inverted_data = bytearray()
        for i in range(0, len(pixel_data), 3):
            red = pixel_data[i]
            green = pixel_data[i + 1]
            blue = pixel_data[i + 2]

            # Инвертируем цвета
            inverted_data.extend((255 - red, 255 - green, 255 - blue))
        serialized_data = pickle.dumps(inverted_data)
    else:
        image_data = bytearray(file.read())  # Чтение пиксельных данных

        # Инверсия цветов
        inverted_data = bytearray()
        for byte in image_data:
            inverted_data.append(255 - byte)
        serialized_data = pickle.dumps(inverted_data)

    header = pickle.dumps(header)
    return xmlrpc.client.Binary(serialized_data), header
server.register_function(send_back_inversion, 'color_inversion')


# Бинаризация изображения по порогу
def binarize_image(file_name, threshold):
    add_log('binarize_image')
    file = open(file_name, 'rb')
    header = file.read(54)
    data = file.read()
    binarized_data = bytearray()
    bits_per_pixel = int.from_bytes(header[28:30], byteorder='little')

    if bits_per_pixel == 24:
        for i in range(0, len(data), 3):
            pixel_value = sum(data[i:i+3]) // 3
            if pixel_value > threshold:
                binarized_data.extend(bytes([255, 255, 255]))  # Белый цвет
            else:
                binarized_data.extend(bytes([0, 0, 0]))  # Черный цвет
        serialized_data = pickle.dumps(binarized_data)
        header = pickle.dumps(header)
        return xmlrpc.client.Binary(serialized_data), header
    else:
        file.close()
        image = Image.open(file_name)
        image = image.convert('L')  # Преобразование изображения в черно-белое

        pixel_data = image.load()
        for i in range(image.width):
            for j in range(image.height):
                if pixel_data[i, j] < threshold:
                    pixel_data[i, j] = 0
                else:
                    pixel_data[i, j] = 255

        binarized_image = image
        serialized_data = pickle.dumps(binarized_image)
        return serialized_data
server.register_function(binarize_image,'binarize_image')

# Поворот изображения
def rotated_image(image_path):
    add_log('rotated_image')
    with open(image_path, 'rb') as file:
        data = file.read()

    header_size = int.from_bytes(data[10:14], byteorder='little')
    width = int.from_bytes(data[18:22], byteorder='little')
    height = int.from_bytes(data[22:26], byteorder='little')
    row_padded = (width * 3 + 3) & (~3)
    rotate_data = bytearray(data)

    for i in range(height):
        for j in range(width):
            pixel_start = header_size + i * row_padded + (width - j - 1) * 3
            rotated_pixel_start = header_size + i * row_padded + j * 3
            rotate_data[rotated_pixel_start:rotated_pixel_start + 3] = data[pixel_start:pixel_start + 3]
    rotate_data = pickle.dumps(rotate_data)
    return xmlrpc.client.Binary(rotate_data)
server.register_function(rotated_image,'rotated_image')

server.serve_forever()
