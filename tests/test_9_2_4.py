# 9_2_4 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_2_4(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Считываем код из временного файла
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Преобразуем код в AST
        tree = ast.parse(code)

        # Контейнеры для найденных генераторов
        generator_funcs = []
        generator_exprs = []
        args_param = []

        # Обход всех узлов дерева
        for node in ast.walk(tree):
            # Генераторные функции (содержат yield или yield from)
            if isinstance(node, ast.FunctionDef):
                if any(isinstance(n, (ast.Yield, ast.YieldFrom)) for n in ast.walk(node)):
                    generator_funcs.append(node.name)
                    # Собираем аргументы, функции генератора
                    args_param = [arg.arg for arg in node.args.args]
            # Генераторные выражения: (x for x in ...)
            elif isinstance(node, ast.GeneratorExp):
                # Попробуем восстановить текст выражения (если доступна ast.unparse)
                try:
                    gen_expr = ast.unparse(node)
                except AttributeError:
                    gen_expr = "<генераторное выражение>"
                generator_exprs.append(gen_expr)

        # Проверка наличия генераторов
        if not generator_funcs and not generator_exprs:
            raise ValueError("ОШИБКА: В коде не найдено ни одной генераторной функции или выражения.")
        if "max_size" not in args_param:
            raise ValueError("Параметр 'max_size' не найден.")
        if len(args_param) != 1:
            raise ValueError("Неверное количество параметров.")
        if generator_funcs:
            result.append(f"Найдены генераторные функции:\n{'\n'.join(generator_funcs)}")
        if generator_exprs:
            result.append(f"Найдены генераторные выражения:\n{'\n'.join(generator_exprs)}")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_9_2_4_1(path_tmp_file, generator_funcs[0])
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_2_4_1(path_tmp_file: str, generator_funcs: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "8",
        "5",
    )
    # Ожидаемый результат
    expected_output = (
        ('iKZWeqhF@mail.ru\nWCEPyYng@mail.ru\nFbyBMWXa@mail.ru\nSCrUZoLg@mail.ru\nubbbPIay@mail.ru'),
        ('iKZWe@mail.ru\nqhFWC@mail.ru\nEPyYn@mail.ru\ngFbyB@mail.ru\nMWXaS@mail.ru'),
    )
    # Ожидаемый результат при прямом выполнении
    expected_output2 = (
        ('RnBUbHoW@mail.ru', 'CFJowoRo@mail.ru', 'WDsbAJPg@mail.ru', 'lOUshVvU@mail.ru', 'TGBGQmts@mail.ru'),
        ('CrUZo@mail.ru', 'Lgubb@mail.ru', 'bPIay@mail.ru', 'RnBUb@mail.ru', 'HoWCF@mail.ru'),
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Импортируем модуль пользователя
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data=test_input[i], capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля

            # Получаем перехваченный вывод из stdout
            captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_output[i]}\n")

            # Проверяем результат
            if captured_output == expected_output[i]:
                test_result.append(f"Получено:\n{captured_output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{captured_output}\n"
                )

            # Получаем функцию из модуля
            funcs = getattr(user_module, generator_funcs)
            # Выполняем функцию, что бы получить первые 5ть результатов для проверки
            answer = tuple(next(funcs(int(test_input[i]))) for _ in range(5))

            if answer != expected_output2[i]:
                raise ValueError(
                    f"------------- FAIL Тест проверка что возвращает функция: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось:\n{expected_output2[i]}\nно получен:\n{answer}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
