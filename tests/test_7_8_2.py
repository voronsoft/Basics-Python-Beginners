# 7_8_2 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_7_8_2(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    # Сохраняем оригинальные потоки ввода/вывода
    original_stdin = sys.stdin
    original_stdout = sys.stdout
    # Подменяем stdin на фейковый с тестовыми данными
    test_input = "7"
    sys.stdin = StringIO(test_input)
    # Заглушка для sys.stderr
    original_stderr = sys.stderr  # сохраняем оригинал
    sys.stderr = StringIO()  # подменяем на буфер
    # Перенаправляем stdout, чтобы не засорять вывод тестов
    sys.stdout = StringIO()

    result = []

    try:
        result.append(f"-------------Тест structure ------------")

        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
        # Восстановим стандартные потоки
        sys.stdin = original_stdin
        sys.stdout = original_stdout

        # Проверяем что есть необходимые атрибуты в коде пользователя
        if not hasattr(user_module, "get_sq"):
            raise AttributeError("ОШИБКА: переменная 'get_sq' не найдена в коде пользователя")

        # Читаем исходный код
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        lambda_found = False

        # Проверка что 'get_sq' присвоена лямбда функция
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "get_sq":
                        if isinstance(node.value, ast.Lambda):
                            lambda_found = True

                            # Проверка: один параметр
                            if len(node.value.args.args) != 1:
                                raise ValueError("ОШИБКА: лямбда-функция должна иметь ровно один параметр")

                            result.append("Переменной 'get_sq' присвоена лямбда-функция с одним параметром")

        if not lambda_found:
            raise TypeError("ОШИБКА: переменной 'get_sq' не присвоена лямбда-функция")

        result.append("--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_8_2_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_8_2_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        6,
        -2,
        11,
    )
    # Ожидаемый результат
    expected_output = (
        36,
        4,
        121,
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(user_module)

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Получаем get_sq из модуля пользователя
            user_func = getattr(user_module, 'get_sq')

            # Получаем результат
            res = user_func(test_input[i])
            if res == expected_output[i]:
                test_result.append(f"Получено: {res}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {res}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
