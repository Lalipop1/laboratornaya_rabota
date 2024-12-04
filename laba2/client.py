import xmlrpc.client
import pickle
import pandas as pd
server = xmlrpc.client.ServerProxy("http://localhost:8008")
server_stats = xmlrpc.client.ServerProxy("http://localhost:8018")

print('Ping:', server.ping())
print('Server datetime:', server.now())

print('View, type, value:', server.type(2))
print('View, type, value:', server.type(2.))
print('View, type, value:', server.type('My string'))
print('View, type, value:', server.type("My string"))
print('View, type, value:', server.type([1,2,3]))
print('View, type, value:', server.type(["one", "two", "three"]))
print('View, type, value:', server.type((1,2,"3")))

print('Sum 2 + 3 :', server.summa(2, 3))
print('Pow 2^3: ', server.pow(2, 3))
Surname, Name, Patronym, Birth = map(str, input("Введите ФИО и дату рождения:").split())
list = []  #Петров Иван Иванович 22.03.1989
list.extend((Surname, Name, Patronym, Birth))
print('Плохой ли ты парень?', server.black_list_check(list))

#инверсия цвета
input_file = 'Jellyfish.bmp'
output, header = server.color_inversion(input_file)
output = pickle.loads(output.data)
header = pickle.loads(header.data)

output_file = 'invers-jelly.bmp'
with open(output_file, 'wb') as f:
    f.write(header)
    f.write(output)

input_file = 'xxxxx.bmp'
output, header = server.color_inversion(input_file)
output = pickle.loads(output.data)
header = pickle.loads(header.data)

output_file = 'invers-xx.bmp'
with open(output_file, 'wb') as f:
    f.write(header)
    f.write(output)

#бинаризация изображения
file_name = 'Jellyfish.bmp'
threshold = int(input('Ведите значене порога бинаризации:'))
binarized_data, header = server.binarize_image(file_name, threshold)
binarized_data = pickle.loads(binarized_data.data)
header = pickle.loads(header.data)
output_file = 'binarized-jelly.bmp'
with open(output_file, 'wb') as f:
    f.write(header)
    f.write(binarized_data)

file_name = 'xxxxx.bmp'
threshold = int(input('Ведите значене порога бинаризации:'))
bin_data = server.binarize_image(file_name, threshold)
bin_data = pickle.loads(bin_data.data)
bin_data.save('binarized-xx.bmp')


#поворот изображения
file_name = 'Jellyfish.bmp'
rotated_data = server.rotated_image(file_name)
rotated_data = pickle.loads(rotated_data.data)
with open('rotated_image.bmp', 'wb') as file:
    file.write(rotated_data)

def check_server(check,direct, directory):
    try:
        print('статус сервер', server_stats.list_check(check,direct, directory))
    except Exception as e:
        print('Нет соединения')
check = str(input('Введите искомы тип операций'))# binarize_image
direct = 'archive.csv'
directory = 'C:/programs/laba2'
check_server(check,direct, directory)