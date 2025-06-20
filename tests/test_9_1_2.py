# 9_1_2 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_1_2(path_tmp_file: str, task_num_test: str):
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

        # Обход всех узлов дерева
        for node in ast.walk(tree):
            # Генераторные функции (содержат yield или yield from)
            if isinstance(node, ast.FunctionDef):
                if any(isinstance(n, (ast.Yield, ast.YieldFrom)) for n in ast.walk(node)):
                    generator_funcs.append(node.name)

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
            result.append(f"Найдены генераторные функции: {', '.join(generator_funcs)}")
        if generator_exprs:
            result.append(f"Найдены генераторные выражения: {', '.join(generator_exprs)}")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_9_1_2_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_1_2_1(path_tmp_file: str):
    """Тест генератора и кортежа квадратов в диапазоне [a; b]"""
    # Входные данные
    test_input = "3 7"  # Значит, ожидаем квадраты: 9, 16, 25, 36, 49
    # Ожидаемый результат
    expected_output = tuple(x**2 for x in range(3, 8))

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

        # Проверяем наличие переменной
        if not hasattr(user_module, "tp"):
            raise ValueError("ОШИБКА: Переменная 'tp' не найдена в коде.")

        tp = getattr(user_module, "tp")

        # Проверка, что это кортеж
        if not isinstance(tp, tuple):
            raise ValueError("ОШИБКА: Переменная 'tp' не является кортежем.")

        # Проверка содержимого
        if tp != expected_output:
            raise ValueError(
                f"------------- FAIL Тест --------\n"
                f"Входные данные: {test_input}\n"
                f"Ожидалось: {expected_output}\nно получен: {tp}"
            )

        result.append("-------------- OK генератор --------------")
        result.append("Переменная 'tp' найдена и содержит корректные значения.")
        result.append("Проверка диапазона пройдена успешно.")
        return "\n".join(result)

    except Exception as e:
        raise RuntimeError(f"Ошибка выполнения кода:\n{e}")
