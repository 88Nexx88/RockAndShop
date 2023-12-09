import os
import re


def rename_files(directory):
    # Переходим в указанную директорию
    os.chdir(directory)

    # Получаем список файлов в текущей директории
    files = os.listdir()

    # Переименовываем файлы
    for file in files:
        filename, file_extension = os.path.splitext(file)
        new_name = filename.translate(str.maketrans("", "", r'!"№;%:?*().-,_+=/\|@#$^&')) + file_extension

        # Переименовываем файл
        if new_name != file:
            os.rename(file, new_name)
            print(f"{file} --------------  {new_name}")




# Пример использования
directory_path = 'Shops/All/img'
rename_files('Shops/All/img')
