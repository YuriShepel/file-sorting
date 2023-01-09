# Программа "Сортировщик файлов"

## Работа программы
Пользователь указывает такие данные:
 - одну или несколько директорий, в которых нужно навести порядок;
 - [опционально] общую директорию, в которую нужно перенести файлы из всех исходных директорий;
 - словарь вот такого вида:
 ```
 {
     'music': ('mp3', 'wav', 'aiff'),
     'images': ('jpg', 'png', 'bmp'),
     'docs': ('pdf', 'doc', 'docx'),
     'archives': ('zip', 'rar')
 }
 ```
 Программа сортирует файлы в указанной директории (-ях), то есть распределить файлы по субдиректориям в зависимости от их типа.
 ------------------------------------------------------------------------------------
 files_to_sort_dir1 = r'D:\test\dir1' (пример пути к папке с файлами для сортировки)

 files_to_sort_dir2 = r'D:\test\dir2' (пример пути к папке с файлами для сортировки)

 files_to_sort_dir3 = r'D:\test\dir3' (пример пути к папке с файлами для сортировки)