# 7_5_4 тест для задачи
import importlib.util
import inspect


def test_7_5_4(path_tmp_file: str, task_num_test: str):
    """Тестирование функции get_data_fig структуры:
    - Проверка наличия функции get_data_fig
    - Проверка параметра tag
    - Проверка значения параметра tag по умолчанию
    """

    result = []  # Список для накопления результатов тестов

    try:
        result.append(f"-------------Тест structure ------------")

        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        # Проверяем, что функция get_data_fig присутствует
        if not hasattr(user_module, "get_data_fig"):
            raise AttributeError("ОШИБКА функция 'get_data_fig' не найдена в коде пользователя")
        else:
            result.append("Найдено: 'get_data_fig'")

        # Получаем функцию для работы с ней
        func = user_module.get_data_fig

        # --- Проверка параметров функции ---
        sig = inspect.signature(func)
        params = sig.parameters

        # --- Проверяем наличие параметра *args или подобный
        var_positional_params = [name for name, p in params.items() if p.kind == inspect.Parameter.VAR_POSITIONAL]

        if var_positional_params:
            result.append(f"Найдено: *{var_positional_params[0]}")
        else:
            raise ValueError("ОШИБКА: Не найден параметр *args")

        # --- Проверяем наличие параметра *kwargs
        var_keyword_params = [name for name, p in params.items() if p.kind == inspect.Parameter.VAR_KEYWORD]

        if var_keyword_params:
            result.append(f"Найдено: **{var_keyword_params[0]}")
        else:
            raise ValueError("ОШИБКА: Не найден параметр **kwargs")

        result.append(f"--------------OK structure -------------\n")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_5_4_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_5_4_1(path_tmp_file: str, task_num_test: str):
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
