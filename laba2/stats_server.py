import xmlrpc.server
import csv
import os
import glob
import datetime
import pandas as pd

MAX_RECORDS = 4
data_file = 'archive.csv'
archive_file = 'archive.csv'
headers = ['Value', 'Time']

class MyXMLRPCServer(xmlrpc.server.SimpleXMLRPCServer):
    def __init__(self, address):
        super().__init__(address)

        if not os.path.exists(data_file):
            with open(data_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

    def save_data(self, value):
        with open(data_file, 'a', newline='') as file:
            writer = csv.writer(file)
            data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Исправлено здесь
            writer.writerow([value, data])

        if sum(1 for _ in open(data_file)) -1 >= MAX_RECORDS: # -1 потому что заголовок тоже считается
            self.archive_data()

        return True

    def archive_data(self):
        today = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        os.rename(data_file, f'{archive_file[:-4]}_{today}.csv')
        with open(data_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

def find_csv_files_glob(directory):
    try:
        csv_files = glob.glob(os.path.join(directory, "*.csv"))
        return [os.path.basename(f) for f in csv_files]
    except FileNotFoundError:
        print(f"Директория '{directory}' не найдена.")
        return []  # Возвращаем пустой список, а не None


def list_check(check, direct, directory):
    csv_filenames = find_csv_files_glob(directory)
    if not csv_filenames:
        return []  # Возвращаем пустой список, если файлов нет

    note = []
    parts1 = [int(x) for x in direct.split('_')[1:]]

    for filename in csv_filenames:
            filename_without_extension = filename[:-4]
            parts2 = [int(x) for x in filename_without_extension.split('_')[1:]]
            if all(p1 < p2 for p1, p2 in zip(parts1, parts2)): #Сравнение всех элементов
                filepath = os.path.join(directory, filename)
                try:
                    df = pd.read_csv(filepath)
                    matching_rows = df[df['Value'] == check] #Используем векторизованные операции
                    note.extend(matching_rows.to_dict(orient='records'))
                except KeyError:
                    print(f"Столбец 'Value' не найден в файле '{filepath}'.")
                except pd.errors.EmptyDataError:
                    print(f"Файл '{filepath}' пустой.")
    return note



server = MyXMLRPCServer(('localhost', 8018))
server.register_function(server.save_data, 'add_log')
server.register_function(list_check, 'list_check')

print("Server is running...")
server.serve_forever()