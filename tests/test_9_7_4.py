# 9_7_4 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_9_7_4(path_tmp_file: str, task_num_test: str):
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

        tuple_name = None

        for node in ast.walk(tree):

            # Поиск tple через:
            if isinstance(node, ast.Assign):
                value = node.value

                is_tuple = isinstance(value, ast.Tuple) or (
                    isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'tuple'
                )

                if is_tuple:
                    if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                        tuple_name = node.targets[0].id

        if not tuple_name:
            raise ValueError("ОШИБКА: Не найдено присваивание кортежа или вызов tuple()).")

        result.append(f"Найден кортеж с именем: {tuple_name}")
        result.append("--------------OK structure -------------\n")

        # Функциональный тест
        try:
            res = test_9_7_4_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_9_7_4_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "Номер;Имя;Оценка;Зачет\n1;Портос;5;Да\n2;Арамис;3;Да\n3;Атос;4;Да\n4;д'Артаньян;2;Нет\n5;Балакирев;1;Нет",
        "Номер;Имя;Оценка;Зачет\n1;Сидоров;5;Да\n2;Балакирев;3;Да\n3;Петров;4;Да\n4;Камалов;2;Нет",
    )

    # Ожидаемые данные
    expected_tuple = (
        (
            ('Имя', 'Зачет', 'Оценка', 'Номер'),
            ('Портос', 'Да', 5, 1),
            ('Арамис', 'Да', 3, 2),
            ('Атос', 'Да', 4, 3),
            ("д'Артаньян", 'Нет', 2, 4),
            ('Балакирев', 'Нет', 1, 5),
        ),
        (
            ('Имя', 'Зачет', 'Оценка', 'Номер'),
            ('Сидоров', 'Да', 5, 1),
            ('Балакирев', 'Да', 3, 2),
            ('Петров', 'Да', 4, 3),
            ('Камалов', 'Нет', 2, 4),
        ),
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

            # Получаем из модуля кортеж
            user_tuple = getattr(user_module, "t_sorted")

            # Формируем отчет по тесту
            test_result = []
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_tuple[i]}")

            # Проверка формирования кортежа
            if user_tuple == expected_tuple[i]:
                test_result.append(f"Получено:\n{user_tuple}\n")
            else:
                raise RuntimeError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Ошибка: Кортеж формируется НЕ правильно.\n"
                    f"Ожидалось:\n{expected_tuple[i]}\nно получено:\n{user_tuple}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n{error_info}")
