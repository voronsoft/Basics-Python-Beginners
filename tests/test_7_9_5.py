# 7_9_5 тест для задачи
import ast
import importlib.util
import inspect
import sys

from io import StringIO


def test_7_9_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    # Сохраняем оригинальные потоки ввода/вывода
    original_stdin = sys.stdin
    original_stdout = sys.stdout

    # Подменяем stdin на фейковый с тестовыми данными
    test_input = "Сергей Балакирев"
    sys.stdin = StringIO(test_input)

    # Перенаправляем stdout, чтобы не засорять вывод тестов
    sys.stdout = StringIO()

    result = []  # Список для накопления результатов тестов

    try:
        result.append(f"-------------Тест structure ------------")

        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
        # Восстанавливаем оригинальные потоки
        sys.stdin = original_stdin
        sys.stdout = original_stdout

        # Проверяем наличие функции
        if not hasattr(user_module, "create_global"):
            raise AttributeError("Функция 'create_global' не найдена")

        # Получаем исходный код функции
        source = inspect.getsource(user_module.create_global)

        # Парсим в AST дерево для анализа кода
        tree = ast.parse(source)

        # Проверяем, есть ли global TOTAL
        has_global_total = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Global) and "TOTAL" in node.names:
                has_global_total = True
                break

        if not has_global_total:
            raise SyntaxError("ОШИБКА: в функции 'create_global' не найден 'global TOTAL'")

        result.append("Проверка 'global TOTAL': OK")

        result.append(f"--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_9_5_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_9_5_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = ("Сергей Балакирев", "Разработчик молодец", "77", "10")
    # Ожидаемый результат
    expected_output = (
        "Сергей Балакирев",
        "Разработчик молодец",
        "77",
        "10",
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("module.name", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(user_module)

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: TOTAL={expected_output[i]}")

            # Получаем функцию create_global из модуля пользователя
            create_global = getattr(user_module, 'create_global')
            # Выполняем функцию
            create_global(test_input[i])

            if not hasattr(user_module, 'TOTAL'):
                raise AttributeError("ОШИБКА: глобальная переменная TOTAL не создана")

            if user_module.TOTAL == expected_output[i]:
                test_result.append(f"Получено: TOTAL={user_module.TOTAL}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: TOTAL={expected_output[i]}\nно получен: TOTAL={user_module.TOTAL}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
