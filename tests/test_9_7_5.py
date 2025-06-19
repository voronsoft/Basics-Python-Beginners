# 9_7_5 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_7_5(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""
    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Чтение пользовательского кода
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code, allowed_imports=["sys"], allowed_calls=["sys.stdin.readlines"])

        # Разбор в AST
        tree = ast.parse(code)

        sort_used = False
        key_used = False
        lst_used = False

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "lst":
                        value = node.value
                        # Простой список [1, 2, 3]
                        if isinstance(value, ast.List):
                            lst_used = True
                        # Генератор списка [x for x in y]
                        elif isinstance(value, ast.ListComp):
                            lst_used = True
                        # Вызов функции list(...)
                        elif isinstance(value, ast.Call):
                            if isinstance(value.func, ast.Name) and value.func.id == "list":
                                lst_used = True
                        # Опционально: можно добавить проверку распаковки
                        elif isinstance(value, ast.BinOp) and isinstance(value.op, ast.Add):
                            # lst = [1, 2] + [3, 4]
                            lst_used = True

            # Поиск "sort", "sorted", "key"
            if isinstance(node, ast.Call):
                func_name = ""

                # Определяем имя функции, даже если это mylist.sort(...)
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name in {"sort", "sorted"}:
                    sort_used = True

                    # Проверяем, используется ли аргумент key
                    if any(kw.arg == "key" for kw in node.keywords):
                        key_used = True

        if not lst_used:
            raise RuntimeError("ОШИБКА: В коде не найден lst (список).")

        result.append("Найден список lst")

        # Проверка, были ли найдены нужные вызовы
        if not sort_used:
            raise ValueError("ОШИБКА: В коде не найден вызов функции sort() или sorted().")

        result.append("Найден вызов функции sort()/sorted()")

        if key_used:
            result.append("Отлично! Параметр 'key' используется.")
        else:
            raise ValueError("ОШИБКА: Вызов sort()/sorted() без параметра 'key'.")

        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_9_7_5_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_7_5_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Атос=лейтенант\nПортос=прапорщик\nд'Артаньян=капитан\nАрамис=лейтенант\nБалакирев=рядовой",
        "Атос=сержант\nПортос=прапорщик\nд'Артаньян=капитан\nАрамис=подполковник\nБалакирев=полковник",
    )

    # Ожидаемые данные вывода
    expected_output = (
        [
            ['Балакирев', 'рядовой'],
            ['Портос', 'прапорщик'],
            ['Атос', 'лейтенант'],
            ['Арамис', 'лейтенант'],
            ["д'Артаньян", 'капитан'],
        ],
        [
            ['Атос', 'сержант'],
            ['Портос', 'прапорщик'],
            ["д'Артаньян", 'капитан'],
            ['Арамис', 'подполковник'],
            ['Балакирев', 'полковник'],
        ],
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

            # Получаем из модуля список
            user_lst = getattr(user_module, "lst")

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Проверка формирования списка
            if user_lst == expected_output[i]:
                test_result.append(f"Получено: {user_lst}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Ошибка: список lst формируется НЕ правильно.\n"
                    f"Ожидалось:\n{expected_output}\nно получено:\n{user_lst}"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
