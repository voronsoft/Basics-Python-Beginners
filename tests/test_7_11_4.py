# 7_11_4 тест для задачи
import ast
import importlib.util
import sys

from io import StringIO


def test_7_11_4(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода (наличие декоратора и двух параметров у декорируемой функции)"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение и разбор кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code)

        # Ищем все функции, у которых есть декораторы
        decorated_funcs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.decorator_list:
                decorated_funcs.append((node.name, len(node.args.args)))

        if not decorated_funcs:
            raise ValueError("ОШИБКА: Не найдена ни одна задекорированная функция.")

        # Ищем функцию с двумя параметрами
        target_funcs = [f for f in decorated_funcs if f[1] == 2]

        if not target_funcs:
            raise ValueError("ОШИБКА: Нет задекорированной функции с двумя параметрами.")
        elif len(target_funcs) > 1:
            raise ValueError(
                f"ОШИБКА: Найдено несколько задекорированных функций с двумя параметрами: {[f[0] for f in target_funcs]}"
            )
        else:
            result.append(f"Функция '{target_funcs[0][0]}' найдена, задекорирована и принимает 2 параметра.")

        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_11_4_1(path_tmp_file, target_funcs[0][0])
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_11_4_1(path_tmp_file: str, fnc_name):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "7 5 3 1\n8 6 4 2",
        "house river tree car\nдом река дерево машина",
        "house tree car mouse\nдом дерево машина мышь",
        "house tree\nдом дерево",
    )
    # Ожидаемый результат
    expected_output = (
        "('1', '2') ('3', '4') ('5', '6') ('7', '8')",
        "('car', 'машина') ('house', 'дом') ('river', 'река') ('tree', 'дерево')",
        "('car', 'машина') ('house', 'дом') ('mouse', 'мышь') ('tree', 'дерево')",
        "('house', 'дом') ('tree', 'дерево')",
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
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Восстанавливаем оригинальный stdout
            sys.stdout = original_stdout

            func = getattr(user_module, fnc_name)  # Получаем функцию из модуля
            # Выполняем функцию
            a, b = test_input[i].split("\n")
            func(a, b)
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
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
