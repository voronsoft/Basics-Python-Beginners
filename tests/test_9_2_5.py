# 9_2_5 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_2_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Считываем код из временного файла
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()
        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code)

        # Разбор кода в дерево AST
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
        if generator_funcs:
            result.append(f"Найдены генераторные функции:\n{'\n'.join(generator_funcs)}")
        if generator_exprs:
            result.append(f"Найдены генераторные выражения:\n{'\n'.join(generator_exprs)}")
        if len(args_param) > 0:
            raise ValueError("ОШИБКА: Неверное количество параметров.")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_9_2_5_1(path_tmp_file, generator_funcs[0])
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_2_5_1(path_tmp_file: str, generator_funcs: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = ""
    # Ожидаемый результат
    stdout_output = '2 3 5 7 11 13 17 19 23 29'
    # Ожидаемый результат при прямом выполнении
    yield_output = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)

    result = []  # Список для накопления результатов тестов

    try:
        # Импортируем модуль пользователя
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Используем контекстный менеджер для подмены потоков
        with stream_interceptor(stdin_data=test_input, capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

        # Получаем перехваченный вывод из stdout
        captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

        # Проверяем результат
        test_result = list()
        test_result.append(f"--------------OK Тест: 1 (вывод print())-------")
        test_result.append(f"Ожидалось: {stdout_output}\n")

        # Получаем функцию из модуля
        funcs = getattr(user_module, generator_funcs)
        g = funcs()
        # Выполняем функцию, что бы получить первые 10ть результатов для проверки
        answer = tuple(next(g) for _ in range(10))

        # Проверяем результат
        if captured_output == stdout_output:
            test_result.append(f"Получено: {captured_output}\n")
        else:
            raise ValueError(
                f"-------------- FAIL Тест --------\n" f"Ожидалось: {stdout_output}\nно получен: {captured_output}\n"
            )
        if answer == yield_output:
            test_result.append(f"-------------OK Тест: 2 (что возвращает функция)--------------\n")
            test_result.append(f"Ожидалось: {yield_output}\n")
            test_result.append(f"Получено: {answer}\n")

        else:
            raise ValueError(
                f"------------- FAIL Тест проверка что возвращает функция: --------\n"
                f"Ожидалось: {yield_output}\nно получен:{answer}\n"
            )

        result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
