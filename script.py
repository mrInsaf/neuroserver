import os

def combine_files_by_suffix(suffix, exclude_dirs=None, output_file='combined.txt', use_relative_path=True):
    """
    Рекурсивно проходит по текущей директории и объединяет содержимое файлов с заданным суффиксом.
    
    :param suffix: Расширение файлов для поиска, например '.txt' или '.suffix'
    :param exclude_dirs: Список названий папок, которые нужно исключить из поиска
    :param output_file: Имя файла, в который будет записан результат
    :param use_relative_path: Если True — выводит относительный путь, иначе — абсолютный
    """
    if exclude_dirs is None:
        exclude_dirs = ['venv']

    current_dir = os.getcwd()
    output_path = os.path.join(current_dir, output_file)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(current_dir):
            # Исключаем нужные папки
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not any(d.startswith(excl) for excl in exclude_dirs)]

            for file in files:
                if file.endswith(suffix):
                    file_path = os.path.join(root, file)
                    try:
                        # Вычисляем путь для вывода
                        if use_relative_path:
                            display_path = os.path.relpath(file_path, current_dir)
                        else:
                            display_path = file_path

                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            outfile.write(f"--- {display_path} ---\n")
                            outfile.write(content + '\n\n')
                    except Exception as e:
                        print(f"Ошибка при чтении файла {file_path}: {e}")

    print(f"Файлы с суффиксом '{suffix}' успешно объединены в '{output_path}'.")

# Пример вызова функции
combine_files_by_suffix('.py')