# 7_6_7 тест для задачи
import importlib.util
import sys

from io import StringIO

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_7_6_7(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []  # Список для накопления результатов тестов

    try:
        with open(path_tmp_file, 'r', encoding='utf-8') as f:
            user_code = f.read()
        # Проверка кода на безопасность
        check_code_safety(user_code, allowed_imports=["sys"], allowed_calls=["sys.stdin.readlines"])

        result.append(f"-------------Тест structure ------------")

        test_input = "Города=about-cities\nМашины=read-of-cars\nСамолеты=airplanes"

        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Используем контекстный менеджер для подмены потоков
        with stream_interceptor(stdin_data=test_input, capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

        # Получаем перехваченный вывод из stdout
        captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

        # Проверяем что есть необходимые атрибуты в коде пользователя
        attr_search = {"menu": "dict", "lst_in": "list"}

        for item, expected_type in attr_search.items():
            if not hasattr(user_module, item):
                raise AttributeError(f"ОШИБКА '{item}' не найден(а) в коде пользователя")
            if item in attr_search:
                # Получаем сам атрибут
                attr = getattr(user_module, item)
                # Получаем его тип
                attr_type = type(attr).__name__

                # Проверяем тип
                if attr_type == expected_type:
                    result.append(f"Найдено: '{item}' (тип: {attr_type})")
                else:
                    # Для других типов проверяем соответствие
                    if attr_type != expected_type:
                        raise TypeError(
                            f"ОШИБКА: '{item}' имеет неверный тип. Ожидается {expected_type}, получен {attr_type}"
                        )
                    result.append(f"Найдено: '{item}' (тип: {attr_type})")

        result.append(f"--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_6_7_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_6_7_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Города=about-cities\nМашины=read-of-cars\nСамолеты=airplanes",
        "Корабли=ships-read\nСтраны=countries-about",
    )
    # Ожидаемый результат
    expected_output = (
        {
            'Главная': 'home',
            'Архив': 'archive',
            'Новости': 'news',
            'Города': 'about-cities',
            'Машины': 'read-of-cars',
            'Самолеты': 'airplanes',
        },
        {
            'Главная': 'home',
            'Архив': 'archive',
            'Новости': 'news',
            'Корабли': 'ships-read',
            'Страны': 'countries-about',
        },
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Подменяем stdin с тестовыми данными
            sys.stdin = StringIO(test_input[i])
            # Заглушка для sys.stderr
            original_stderr = sys.stderr  # сохраняем оригинал
            sys.stderr = StringIO()  # подменяем на буфер

            spec.loader.exec_module(user_module)

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            # Получаем словарь menu из модуля пользователя
            user_menu = getattr(user_module, 'menu', None)

            if user_menu == expected_output[i]:
                test_result.append(f"Получено:\n{user_menu}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{user_menu}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
