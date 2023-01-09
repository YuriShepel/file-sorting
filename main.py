
import os
import shutil


class FileManager:
    def __init__(self):
        self._files_list = []  # список с экземплярами класса File.

    @property
    def files_list(self):
        return self._files_list

    def make_files_list(self, path):
        """
        Функция создает экземпляры класса File из всех файлов (без папок) из указанной папки. Добавляет их
        в `self._files_list`
        :param path: str (путь к папке с файлами)
        :return: str (__repr__ экземпляра класса File)
        """
        for file_name in os.listdir(path):
            file = File(path, file_name)
            if file.name != file.extension and file.extension != 'rollback':
                self._files_list.append(file)

    def make_dirs(self, names_dict, path):
        """
        Функция создает папки с названиями из ключей словаря, только если экземпляр класса File имеет такое же
        разрешение, что указано в значениях ключа.
        Также функция вносит в поле `self._destination_path` экземпляра класса File путь, куда будет перемещен
        файл.
        :param names_dict: dict (словарь с ключами (название папки) и значениями (типы расширений файлов))
        :param path: str (путь, где создавать папки)
        :return: None
        """
        for file in self._files_list:
            for key, value in names_dict.items():
                if file.extension in value:
                    dir = Dir(path, key)
                    dir.make_dir()
                    file.destination_path = os.path.join(path, key, file.name)

    def make_rollback_file(self, path):
        """
        Функция создает `backup` файл. Данные о первоначальном и конечном местоположении файла берутся из экземпляров
        класса File, которые находятся в `self._files_list`.
        Файл переводится в скрытый режим.
        :param path: str (путь, где создается `backup` файл)
        :return: None
        """
        os.chdir(path)
        backup_info = []
        for file in self._files_list:
            backup_info.append(f'{file.destination_path},{file.full_path}\n')
        with open('paths.rollback', 'a') as f:
            f.writelines(backup_info)
            os.system('attrib +h paths.rollback')


class File:
    def __init__(self, path_to_file, name):
        self.path_to_file = path_to_file
        self._name = name
        self._full_path = os.path.join(path_to_file, name)
        self._extension = name.rpartition('.')[2]
        self._destination_path = ''  # путь, куда будет перемещен файл.

    def __repr__(self):
        return f'({self._name}, {self.path_to_file}, {self._destination_path})'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def full_path(self):
        return self._full_path

    @property
    def extension(self):
        return self._extension

    @property
    def destination_path(self):
        return self._destination_path

    @destination_path.setter
    def destination_path(self, value):
        self._destination_path = value


class Dir:
    def __init__(self, path_to_dir, name):
        self._path_to_dir = path_to_dir
        self.name = name
        self._full_path = os.path.join(path_to_dir, name)

    def make_dir(self):
        if not os.path.exists(self._full_path):
            os.makedirs(self._full_path)


def input_data(message):
    """
    Функция запрашивает данные при ее вызове и возвращает результат.
    :param message: str (текст сообщения)
    :return: str (результат ввода пользователя)
    """
    data = input(message).lower()
    return data


def get_same_files_count(path, file_name):
    """
    Функция возвращает число файлов с одинаковыми именами в общей папке.
    :param path: str (путь к общей папке, в которой могут быть файлы с одинаковыми именами.)
    :param file_name: str (имя перемещаемого в общую папку файла.)
    :return: int (число файлов)
    """
    file_list = []
    count = 2
    for file in os.listdir(path):
        file_name = file.split()[0]
        file_extension = os.path.splitext(file)[-1]
        file_list.append(file_name + file_extension)
    for file in file_list:
        if file == file_name:
            count += 1
    return count


def rename_file(path, filename):
    """
    Функция создает и возвращает новое имя для перемещаемого файла.
    :param path: str (путь к папке с файлами)
    :param filename: str (имя, которое нужно переименовать)
    :return: str (новое имя)
    """
    count = get_same_files_count(path, filename)
    partition_filename = filename.rpartition('.')
    name = partition_filename[0]
    dot = partition_filename[1]
    extension = partition_filename[2]
    new_name = f'{name} ({count}){dot}{extension}'
    return new_name


def get_files_path():
    """
    Функция запрашивает количество и путь к файлам для сортировки.
    Возвращает список с путем или путями, если их несколько.
    :return: list (список путей)
    """
    dir_numbers = int(input('Сколько папок нужно сортировать? '))
    path_to_dir = []
    while len(path_to_dir) != dir_numbers:
        path = input('Введите путь к папке: ')
        if not os.path.exists(path):
            print('Такой папки нет')
            continue
        path_to_dir.append(path)
    return path_to_dir


def read_file(file):
    """
    Функция открывает и читает файл, возвращая список со строками.
    :param file: sts (путь к файлу, который нужно прочитать)
    :return: list (список, строк из прочитанного файла)
    """
    with open(file, 'r') as f:
        file_data = f.readlines()
    return file_data


def rollback():
    """
    Функция выполняет ряд действий по восстановлению перемещенных файлов.
    :return: None
    """
    rollback_file_path = input(
        'Введите путь, по которому находится .rollback файл: ')
    rollback_file_path = os.path.join(rollback_file_path, 'paths.rollback')
    if not os.path.exists(rollback_file_path):
        raise FileNotFoundError(
            f'.rollback файл по пути "{rollback_file_path}" отсутствует.')

    data = read_file(rollback_file_path)
    for path in data:
        split_paths = path.split(',')
        source = split_paths[0]
        destination = split_paths[1].rsplit('\\', maxsplit=1)[0].rstrip('\n')
        shutil.copy2(source, destination)
        print(f'File {source} was restored successfully.')


def sort():
    """
    Функция выполняет ряд действий по сортировке файлов.
    :return: None
    """
    path_to_files = get_files_path()
    path_to_dirs = input_data('Введите путь, куда сортировать файлы: ')

    for path in path_to_files:
        f_manager = FileManager()
        f_manager.make_files_list(path)
        f_manager.make_dirs(dict_with_names, path_to_dirs)
        f_manager.make_rollback_file(path)

        for file in f_manager.files_list:
            source = file.full_path
            destination = file.destination_path
            if os.path.isfile(file.destination_path):
                dir_path = file.destination_path.rsplit('\\', maxsplit=1)[0]
                file.name = rename_file(dir_path, file.name)
                destination = os.path.join(dir_path, file.name)
            os.rename(source, destination)
            print(f'File {source} removed to {destination} successfully')


def run(commands):
    while True:
        command = input_data(
            'Нужно сортировать (S) файлы или восстановить (R)? ').lower()
        if command == '':
            quit()

        try:
            f = commands[command]
        except KeyError:
            print('Нужно выбрать (S) или (R)')
            continue

        try:
            f()
        except Exception as e:
            print(e)


commands = {
    's': sort,
    'r': rollback,
}

dict_with_names = {
    'music': ('mp3', 'wav', 'aiff'),
    'images': ('jpg', 'png', 'bmp'),
    'docs': ('pdf', 'doc', 'docx'),
    'archives': ('zip', 'rar')
}

run(commands)

files_to_sort_dir1 = r'D:\test\dir1'  # пример пути к папке с файлами для сортировки
files_to_sort_dir2 = r'D:\test\dir2'  # пример пути к папке с файлами для сортировки
files_to_sort_dir3 = r'D:\test\dir3'  # пример пути к папке с файлами для сортировки

