import ast
import importlib
import json
import multiprocessing
import os
import socket
import sys
import tempfile

from pathlib import Path
from typing import Any, Dict, Union

import autopep8
import wx

from config import JSON_COMPLETED_TASKS, VIDEO_CACHE, VIDEO_PATH
from task_tree.task_structure import lst_task_type
from tasks_video_links.tasks_video_links import tasks_video_links


def get_class():
    """Получаем экземпляр класса динамически импортируя его из директории /tasks"""
    # Преобразуем имя задачи в имя класса (первая буква заглавная)
    class_name = "BaseTask"
    # Формируем имя модуля
    module_name = f"tasks.base_task"

    try:
        # Импортируем модуль
        module = importlib.import_module(module_name)
        # Получаем базовый класс
        task_class = getattr(module, class_name)

        return task_class  # Возвращаем класс

    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Ошибка при импорте модуля или класса: {e}")
        return None  # Возвращаем None, если произошла ошибка


def get_test_func(task_name):
    """Получает тестовую функцию используя динамический импорт"""

    # Формируем имя модуля тестов
    module_name = f"tests.{task_name.lower().replace('descr', 'test')}"
    print("module_name", module_name)
    # Формируем имя тестовой функции
    test_func = task_name.lower().replace('descr', 'test')
    print("test_func", test_func)

    # Динамически импортируем модуль с тестом
    try:
        module = importlib.import_module(module_name)
        print(f"(get_test_func) Модуль {module_name} успешно импортирован!")
    except ImportError as e:
        print(f"(get_test_func) Ошибка импорта модуля: {e}")
        raise ImportError(f"(get_test_func) Ошибка импорта модуля: {e}")

    # Получаем тестовую функцию
    try:
        test_function = getattr(module, test_func)
        print("Функция найдена и импортирована")
        return test_function  # Возвращаем тестовую функцию

    except AttributeError as e:
        print(f"(get_test_func) Функция {test_func} не найдена в модуле\n({e})")
        raise AttributeError(f"(get_test_func) Функция {test_func} не найдена в модуле\n({e})")


def check_syntax(code: str):
    """
    Проверяет код на синтаксические ошибки с использованием модуля ast.
    Выводит результат проверки в wx.MessageBox.

    :param code: Код для проверки.
    """
    try:
        # Пытаемся разобрать код с помощью ast на синтаксические ошибки
        ast.parse(code)
    except SyntaxError as e:
        # Выводим информацию об ошибке
        raise SyntaxError(f"{e.msg}\n\nLine {e.lineno}:\n{e.text}")


def formated_code_pep8(user_code: str) -> str:
    """
    Форматирует код с помощью autopep8 с шириной строки 120 символов.

        :param user_code: (str) код пользователя.
        :returns: (str) форматированный код.
    """
    # Форматируем код пользователя по PEP 8
    # Параметры форматирования передаем как словарь
    options = {'max_line_length': 120}
    formatted_code_pep8 = autopep8.fix_code(user_code, options=options)
    return formatted_code_pep8


def save_code_to_temp_file(user_code: str, task_num: str) -> tuple[str, str]:
    """
    Сохраняет код пользователя во временный файл с расширением .py,
    автоматически форматируя его по нормам PEP 8.

    :param user_code: (str) Многострочный код пользователя.
    :param task_num: (str) Название файла
    :return: (tuple) (путь к файлу, имя файла).
    """
    # Удаляем символы возврата каретки \r, если они присутствуют
    # Что бы при записи в файл пользовательского кода скопированного из текстовых полей или редакторов
    # на ОС Windows не появлялось излишних пустых строк при записи в файл
    # !!! Простое правило при записи текста в файл удалить \r
    # Во избежании появления лишних строк при отображении считанного текста
    user_code = user_code.replace('\r', '')

    # Создаем временный файл с префиксом названия задачи и расширением .py
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        prefix=task_num,  # Задаём начало имени
        delete=False,
        encoding='utf-8',
    ) as temp_file:
        # Записываем отформатированный код пользователя в файл
        temp_file.write(user_code)
        # Получаем путь к временному файлу
        file_path = temp_file.name
        # Получаем имя временного файла
        file_name = os.path.basename(file_path)

    return file_path, file_name


# TODO [2] Зарезервирована на момент реализации тестов для задач
def delete_code_temp_file(file_path: str) -> None:
    """
    Удаляет временный файл кода пользователя из Temp папки ОС

    :param file_path: Путь к файлу.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Файл {file_path} удален.")
    else:
        print(f"Файл {file_path} не существует.")


def check_ide_thonny_pc():
    """Проверка есть ли на пк установленный Ide Thonny"""
    # 1 Путь к директории текущего пользователя
    user_home = Path.home()
    # Строим путь к установленному Thonny
    thonny_path = user_home / 'AppData' / 'Local' / 'Programs' / 'Thonny' / 'thonny.exe'

    # 2 Альтернативный путь установки.
    system_drive = os.environ.get('SystemDrive', 'C:')  # Получаем системный диск
    alternative_path = Path(system_drive + '\\') / 'Program Files (x86)' / 'Thonny' / 'thonny.exe'

    # Проверяем, существует ли файл
    if thonny_path.exists():
        return True
    elif alternative_path.exists():
        return True

    return False


def check_connect_internet():
    """Проверка связи с интернетом на пк"""
    try:
        # Попытка подключиться к Google
        socket.create_connection(("www.google.com", 80), timeout=0.5)
        return True
    except OSError:
        return False


def video_file_run(task_name):
    """Запускает видео файл встроенным проигрывателем в ОС"""
    answer = next((f for f in VIDEO_CACHE if task_name in f), False)
    if isinstance(answer, str):
        path_video_file = VIDEO_PATH / answer
        try:
            os.startfile(str(path_video_file))
        except OSError as e:
            error_msg = (
                f"Ошибка при открытии видео!\n\n"
                f"▸ Файл: {path_video_file.name}\n"
                f"▸ Ошибка Windows: {e}\n\n"
                f"ВОЗМОЖНЫЕ ПРИЧИНЫ:\n"
                f"1. Нет программы для открытия .mp4\n"
                f"2. Ассоциация файлов .mp4 не назначена для плеера по умолчанию в ОС\n"
                f"3. Файл .mp4 повреждён\n\n"
                f"РЕШЕНИЕ:\n"
                f"В ОС нужно указать приложение которое воспроизводит видео файлы .mp4\n"
                f"Если по какой то причине на ОС нет назначенного по умолчанию плеера\n"
                f"для воспроизведения видео файлов формата .mp4\n"
                f"Необходимо его установить и назначить плеером по умолчанию для вашей ОС\n"
                f"Важно что бы плеер/приложение мог воспроизводить файлы формата .mp4\n"
                f"После этого воспроизведение видео из приложения будет запускаться."
            )
            wx.MessageBox(error_msg, "Ошибка запуска", wx.OK | wx.ICON_ERROR)
    else:
        # Видео НЕ найдено в кеше
        dlg = wx.MessageDialog(
            None,
            f"Не удалось найти видео: '{task_name}'\n\n" f"Хотите открыть его в браузере для просмотра?",
            "Видео не найдено",
            wx.YES_NO | wx.ICON_QUESTION,
        )
        if dlg.ShowModal() == wx.ID_YES:
            link = next((link for key, link in tasks_video_links.items() if task_name.lower() in key.lower()), None)
            print("link:", link)
            if link:
                if not wx.LaunchDefaultBrowser(link):
                    wx.MessageBox(
                        "Не удалось открыть браузер.\n" "Проверьте настройки системы.",
                        "Ошибка открытия браузера",
                        wx.OK | wx.ICON_ERROR,
                    )
            else:
                wx.MessageBox(
                    f"Ссылка для видео '{task_name}' не найдена!", "Ссылка отсутствует", wx.OK | wx.ICON_WARNING
                )
        dlg.Destroy()


def read_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Читает данные из JSON-файла и возвращает словарь.

    Параметры:
        file_path (str или Path): Путь к JSON-файлу

    Возвращает:
        Dict[str, Any]: Словарь с данными из файла

    Исключения:
        FileNotFoundError: Если файл не найден
        json.JSONDecodeError: Если файл содержит невалидный JSON
    """
    file_path = Path(file_path)  # Приводим к Path

    if getattr(sys, 'frozen', False):
        # Если запущено как EXE
        exe_dir = Path(sys.executable).parent
        alternative_path = exe_dir / "data" / file_path.name  # Используем имя файла из переданного пути

        if file_path.is_file():
            print(f"[INFO (.exe)- по переданному пути в функцию] Найден файл по переданному пути: {file_path}")
            target_path = file_path
        elif alternative_path.is_file():
            print(f"[INFO (.exe)- по альтернативному пути] Найден файл рядом с EXE: {alternative_path}")
            target_path = alternative_path
        else:
            raise FileNotFoundError(
                f"Файл не найден ни рядом с exe ({alternative_path}), ни по переданному пути ({file_path})"
            )
    else:
        # Если запущено как обычный скрипт
        target_path = file_path  # Используем имя файла из переданного пути
        # print(f"[INFO (script Python)- найден в папке проекта: {file_path}")

        if not target_path.is_file():
            raise FileNotFoundError(f"Файл не найден в папке проекта: {target_path}")

    # После того как определили верный путь, читаем файл
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Ошибка парсинга JSON в файле {target_path}", e.doc, e.pos)


def write_json_file(data: Dict[str, Any], file_path: Union[str, Path]) -> bool:
    """
    Записывает данные в JSON-файл по указанному пути.

    Параметры:
        data: Словарь с данными для записи
        file_path: Путь к файлу (строка или Path)

    Возвращает:
        bool: True если запись прошла успешно, False если возникла ошибка
    """
    file_path = Path(file_path)  # Приводим к Path

    if getattr(sys, 'frozen', False):
        # Если запущено как EXE
        exe_dir = Path(sys.executable).parent
        alternative_path = exe_dir / "data" / file_path.name  # Используем имя файла из переданного пути

        # 1. Проверяем файл по переданному пути
        if file_path.is_file():
            print(f"[INFO] Запись в файл по переданному пути: {file_path}")
            target_path = file_path
        # 2. Если нет, проверяем по альтернативному пути рядом с EXE
        elif alternative_path.is_file():
            print(f"[INFO] Запись в файл рядом с EXE: {alternative_path}")
            target_path = alternative_path
        # 3. Если не нашли, выбрасываем исключение
        else:
            raise FileNotFoundError(
                f"Запись в файл невозможна, так как файл не был найден ни по переданному пути, ни рядом с EXE: {file_path}"
            )
    else:
        # Если запущено как обычный скрипт
        print(f"[INFO] Запись в файл по переданному пути (как скрипт): {file_path}")

        # Проверяем наличие файла по переданному пути
        if not file_path.is_file():
            raise FileNotFoundError(f"Запись в файл невозможна, так как файл не найден по пути: {file_path}")

        target_path = file_path

    # Записываем данные в файл
    try:
        with target_path.open('w', encoding='utf-8') as f:
            json.dump(
                data,
                f,  # type: ignore[arg-type]
                indent=4,
                ensure_ascii=False,
            )

        print(f"[INFO] Данные успешно записаны в файл: {target_path}")
        return True

    except (OSError, IOError) as e:
        print(f"[ERROR] Ошибка файловой системы: {e}")
        return False
    except TypeError as e:
        print(f"[ERROR] Ошибка сериализации JSON (неподдерживаемый тип данных): {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Неожиданная ошибка: {e}")
        return False


def status_completed_tasks():
    """Подсчёт выполнения всех задач в приложении"""
    # Количество всех задач приложения
    all_tasks_app = len(lst_task_type)
    # Количество решенных задач
    completed_tasks = len(read_json_file(JSON_COMPLETED_TASKS))

    if all_tasks_app == completed_tasks:
        return True

    return False


def _run_test_wrapper(queue, test_function, path, name):
    try:
        result = test_function(path, name)
        queue.put(("ok", result))
    except Exception as e:
        queue.put(("error", str(e)))


def run_test_function_with_timeout(test_function, path, name, timeout=10):
    """Запускает тестовую функцию в отдельном процессе с ограничением по времени"""
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=_run_test_wrapper, args=(queue, test_function, path, name))
    p.start()
    p.join(timeout=timeout)

    if p.is_alive():
        p.terminate()
        raise TimeoutError(f"Превышено время выполнения теста ({timeout} секунд)")

    if not queue.empty():
        status, result = queue.get()

        if status == "ok":
            return result
        else:
            raise TimeoutError(result)

    return False, "Не удалось получить результат из теста"
