# 7_5_2 тест для задачи
import importlib.util
import inspect


def test_7_5_2(path_tmp_file: str, task_num_test: str):
    """Тестирование функции get_even структуры:
    - Проверка наличия функции get_even
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

        # Проверяем, что функция get_even присутствует
        if not hasattr(user_module, "get_even"):
            raise AttributeError("ОШИБКА функция 'get_even' не найдена в коде пользователя")
        else:
            result.append("Найдено: 'get_even'")

        # Получаем функцию для работы с ней
        func = user_module.get_even

        # --- Проверка параметров функции ---
        sig = inspect.signature(func)
        params = sig.parameters
        print("1212", params)

        # --- Проверяем наличие параметра *args или подобный
        var_positional_params = [name for name, p in params.items() if p.kind == inspect.Parameter.VAR_POSITIONAL]

        if var_positional_params:
            result.append(f"Найдено: *{var_positional_params[0]}")
        else:
            raise ValueError("ОШИБКА: Не найден параметр *args")

        result.append("")

        # Запускаем вторую часть теста (выполнение кода пользователя)
        try:
            res = test_7_5_2_1(path_tmp_file, task_num_test)
            result.append(res)
        except Exception as e:
            raise ValueError(str(e))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения теста:\n\n{error_info}")


def test_7_5_2_1(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        (45, 4, 8, 11, 12, 0),
        (54, -32, 11, 15, 13, 100),
    )
    # Ожидаемый результат
    expected_output = (
        [4, 8, 12, 0],
        [54, -32, 100],
    )

    result = []  # Список для накопления результатов тестов

    try:
        # Загружаем пользовательский модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
        # Получаем функцию для работы с ней
        func = user_module.get_even

        for i in range(len(test_input)):
            # Вызываем функцию напрямую, передавая аргументы
            output = func(*test_input[i])

            # Проверяем результат
            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            # Сравниваем результат с ожидаемым значением
            if output == expected_output[i]:
                test_result.append(f"Получено:\n{output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{output}\n"
                )

            result.append("\n".join(test_result))

        return "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
