# 7_5_4 тест для задачи
import ast
import importlib.util

from utils.code_security_check import check_code_safety


def test_7_5_4(path_tmp_file: str, task_num_test: str):
    """Тестирование структуры"""
    result = []  # Список для накопления результатов тестов

    try:
        result.append("-------------Тест structure -------------")

        with open(path_tmp_file, "r", encoding="utf-8") as f:
            user_code = f.read()

        # Безопасность кода пользователя
        check_code_safety(user_code)

        # Разбор кода в дерево AST
        tree = ast.parse(user_code)

        find_func = False
        find_varargs = False
        find_kwargs = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == "get_data_fig":
                    find_func = node.name
                    # Проверяем наличие *args в аргументах функции
                    if node.args.vararg:
                        find_varargs = True
                        arg_name = node.args.vararg.arg  # имя переменной (обычно 'args')

                    # Проверяем наличие **kwargs в аргументах функции
                    if node.args.kwarg:
                        find_kwargs = True
                        kwarg_name = node.args.kwarg.arg

        if not find_func:
            raise ValueError("ОШИБКА: Не найдена функция 'get_data_fig'")

        if not find_varargs:
            raise ValueError("ОШИБКА: Функция get_data_fig должна принимать произвольное количество аргументов (*args)")

        if not find_kwargs:
            raise ValueError("ОШИБКА: Функция get_data_fig должна принимать произвольное количество именованных аргументов (*kwargs)")

        result.append(f"Функция найдена: '{find_func}' с параметрами *{arg_name} **{kwarg_name}")
        result.append("--------------OK structure -------------\n")

        # Дополнительно — тест выполнения кода
        try:
            res = test_7_5_4_1(path_tmp_file)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")


def test_7_5_4_1(path_tmp_file: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        (1, 2, 3, 4, 3, 2, 4, {}),
        (1, 2, 3, 4, 3, 2, 4, {'tp': True}),
        (1, 2, 3, 4, 3, 2, 4, {'tp': True, 'color': 7}),
        (1, 2, 3, 4, 3, 2, 4, {'tp': False, 'color': 7, 'width': 2.0}),
        (5, 4, 55, 3, 4, 66, {}),
        (5, 4, 55, 3, 4, 66, {'tp': True}),
        (5, 4, 55, 3, 4, 66, {'tp': True, 'color': 7}),
        (5, 4, 55, 3, 4, 66, {'tp': False, 'color': 7, 'width': 2.0}),
    )
    # Ожидаемый результат
    expected_output = (
        (19,),
        (19, True),
        (19, True, 7),
        (19, False, 7, 2.0),
        (137,),
        (137, True),
        (137, True, 7),
        (137, False, 7, 2.0),
    )

    result = []  # Список для накопления результатов тестов

    try:
        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
        # Получаем функцию для работы с ней
        func = user_module.get_data_fig

        for i in range(len(test_input)):
            # Разбиваем входные данные на позиционные и именованные
            *pos_args, kwargs = test_input[i]

            # Вызываем функцию, передавая позиционные и именованные аргументы
            output = func(*pos_args, **kwargs)

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected_output[i]}")

            # Сравниваем результат с ожидаемым значением
            if output == expected_output[i]:
                test_result.append(f"Получено: {output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\nно получен: {output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
