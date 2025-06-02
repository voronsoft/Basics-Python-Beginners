# 6_6_6 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety
from utils.stdin_stdout_stderr_interceptor import stream_interceptor


def test_6_6_6(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры кода"""

    result = []

    try:
        result.append("-------------Тест structure -------------")

        # Парсим AST
        with open(path_tmp_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Безопасность кода пользователя: читаем код и проверяем его до запуска
        check_code_safety(code, allowed_imports=["sys"], allowed_calls=["sys.stdin.readlines"])

        # Разбор кода в дерево AST
        tree = ast.parse(code)

        find_d_dict = False
        find_generator = False

        for node in ast.walk(tree):
            # Проверка наличия словаря с именем 'd'
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'd':
                        # Словарь через литерал
                        if isinstance(node.value, ast.Dict):
                            find_d_dict = True
                        # Словарь через вызов dict()
                        elif (
                            isinstance(node.value, ast.Call)
                            and isinstance(node.value.func, ast.Name)
                            and node.value.func.id == "dict"
                        ):
                            find_d_dict = True
                        # Словарь через dict comprehension
                        elif isinstance(node.value, ast.DictComp):
                            find_d_dict = True

            # Проверка наличия генератора (генераторное выражение или функция-генератор)
            # Генераторное выражение: или comprehension (list/set/dict)
            if isinstance(node, (ast.GeneratorExp, ast.ListComp, ast.SetComp, ast.DictComp)):
                find_generator = True

            # Функция-генератор: def ... с yield или yield from
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for subnode in ast.walk(node):
                    if isinstance(subnode, (ast.Yield, ast.YieldFrom)):
                        find_generator = True

        if not find_d_dict:
            raise ValueError("ОШИБКА: Словарь 'd' не найден в коде")
        if not find_generator:
            raise ValueError("ОШИБКА: Применение генератора или comprehension (list/set/dict) не найдено в коде")

        result.append("Словарь 'd' найден")
        result.append("Найдено применение генератора или comprehension (list/set/dict) в коде")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_6_6_6_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_6_6_6_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные (3 варианта)
    test_input = (
        "Пушкин: Сказка о рыбаке и рыбке\nЕсенин: Письмо к женщине\nТургенев: Муму\nПушкин: Евгений Онегин\nЕсенин: Русь",
        "Толстой: Война и мир\nТолстой: Анна Каренина\nЧехов: Вишнёвый сад\nТолстой: Воскресение\nЧехов: Чайка",
        "Достоевский: Преступление и наказание\nДостоевский: Идиот\nДостоевский: Братья Карамазовы",
    )

    # Ожидаемые результаты (в виде словарей с отсортированными списками вместо множеств)
    expected_output = (
        {
            'Пушкин': {'Евгений Онегин', 'Сказка о рыбаке и рыбке'},
            'Есенин': {'Письмо к женщине', 'Русь'},
            'Тургенев': {'Муму'},
        },
        {
            'Толстой': {'Анна Каренина', 'Война и мир', 'Воскресение'},
            'Чехов': {'Вишнёвый сад', 'Чайка'},
        },
        {
            'Достоевский': {'Братья Карамазовы', 'Идиот', 'Преступление и наказание'},
        },
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
            user_module = importlib.util.module_from_spec(spec)

            # Используем контекстный менеджер для подмены потоков
            with stream_interceptor(stdin_data=test_input[i], capture_stdout=True, capture_stderr=True) as streams:
                spec.loader.exec_module(user_module)  # Выполняем код модуля

            # Получаем словарь из модуля
            dict_user = getattr(user_module, "d")

            # Формирование отчета
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            # Проверяем результат
            if dict_user == expected_output[i]:
                test_result.append(f"Получено:\n{dict_user}")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{dict_user}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)
    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
