# 7_11_1 тест для задачи
import ast
import importlib.util
import inspect
import sys

from io import StringIO


def test_7_11_1(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие декоратора)"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        # Разбираем код с использованием ast читаем код из файла
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Парсим код в дерево
        tree = ast.parse(code)

        def check_decorator_in_code(tree_in, decorator_name):
            """Проверяет, что функция get_sq декорирована декоратором decorator_name=func_show"""
            for node in ast.walk(tree_in):
                if isinstance(node, ast.FunctionDef) and node.name == 'get_sq':
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == decorator_name:
                            return True
            return False

        # Проверка, что функция get_sq декорирована декоратором func_show
        if not check_decorator_in_code(tree, 'func_show'):
            raise ValueError("ОШИБКА: Функция get_sq не декорирована декоратором func_show")

        result.append("Функция get_sq декорирована декоратором func_show.")

        # Проверка, что функция get_sq принимает два параметра: width и height
        get_sq_func = getattr(user_module, 'get_sq', None)  # Получаем функцию из модуля
        if get_sq_func is None:
            raise ValueError("ОШИБКА: Функция get_sq не найдена")

        sig = inspect.signature(get_sq_func)
        if len(sig.parameters) != 2:
            raise ValueError("ОШИБКА: Функция get_sq должна принимать 2 параметра. (width, height)")

        result.append("Функция get_sq правильно принимает 2 параметра.")

        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_11_1_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_11_1_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        [10, 10],
        [5, 10],
        [1, 10],
    )
    # Ожидаемый результат
    expected_output = (
        "Площадь прямоугольника: 100",
        "Площадь прямоугольника: 50",
        "Площадь прямоугольника: 10",
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("module.name", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Создаем буфер для перехвата вывода
            output_buffer = StringIO()
            # Сохраняем оригинальный stdout
            original_stdout = sys.stdout
            # Перенаправляем stdout в буфер
            sys.stdout = output_buffer

            spec.loader.exec_module(user_module)

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            get_sq = getattr(user_module, "get_sq")  # Получаем функцию из модуля
            width, height = test_input[i]  # Готовим тестовые данные для передачи в функцию
            # Выполняем функцию
            get_sq(width, height)
            # Получаем перехваченный вывод из print()
            captured_output = output_buffer.getvalue().rstrip()
            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout

            # Проверяем результат перехваченного вывода
            if captured_output == expected_output[i]:
                test_result.append(f"Получено: {captured_output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {captured_output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
