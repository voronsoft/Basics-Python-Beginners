# 9_1_1 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_1_1(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры"""

    result = []

    try:
        result.append("-------------Тест structure (поиск генераторов) -------------")

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
            res = test_9_1_1_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_1_1_1(path_tmp_file: str):
    """Проверка генераторного выражения: gen = (x for x in range(2, 10001))"""

    result = []

    try:
        # Импортируем модуль пользователя
        spec = importlib.util.spec_from_file_location("user_code", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)

        # Используем контекстный менеджер для подмены потоков
        with stream_interceptor(stdin_data=" ", capture_stdout=True, capture_stderr=True) as streams:
            spec.loader.exec_module(user_module)  # Выполняем код модуля

        # Получаем перехваченный вывод из stdout
        captured_output = streams["stdout"].getvalue().rstrip() if streams["stdout"] else ""

        # Проверяем, что переменная 'gen' существует
        if not hasattr(user_module, "gen"):
            raise ValueError("ОШИБКА: Переменная 'gen' не найдена в коде.")

        gen = getattr(user_module, "gen")

        # Проверяем, что это генератор
        if not isinstance(gen, type((x for x in []))):
            raise ValueError("ОШИБКА: Переменная 'gen' не является генераторным выражением.")

        # Проверим первые 5 значений
        first_values = [next(gen) for _ in range(5)]

        if first_values != [2, 3, 4, 5, 6]:
            raise ValueError(f"ОШИБКА: Первые значения генератора некорректны: {first_values}")

        result.append("-------------- OK генератор --------------")
        result.append("Переменная 'gen' найдена и содержит корректное генераторное выражение.")
        result.append("Проверка диапазона пройдена успешно.")
        return "\n".join(result)

    except Exception as e:
        raise RuntimeError(f"Ошибка выполнения кода:\n{e}")
