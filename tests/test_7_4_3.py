# 7_4_3 тест для задачи
import importlib.util
import inspect


def test_7_4_3(path_tmp_file: str, task_num_test: str):
    """Функция тестирования функции check_password из пользовательского файла"""

    # Входные данные
    test_input = (
        ("12345678!"),
        ("4364#"),
        ("dfghfgh8gf7h6f"),
        ("5657dfgfh098A!@#"),
    )

    # Ожидаемые результаты
    expected_output = (
        True,
        False,
        False,
        True,
    )

    result = []  # Результаты тестов

    try:
        # Загружаем модуль
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)

        # Проверяем наличие функции
        if not hasattr(user_module, "check_password"):
            raise AttributeError("Функция 'check_password' не найдена в коде пользователя")

        func = user_module.check_password

        # --- ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА параметров функции ---
        sig = inspect.signature(func)
        params = sig.parameters  # словарь параметров

        # Проверка количества параметров у функции
        if len(params) != 2:
            raise ValueError(f"Ожидалось 2 параметра в функции, но найдено: {len(params)}")
        # Проверка, что chars есть в параметрах функции
        if "chars" not in params:
            raise ValueError("Параметр 'chars' не найден в списке параметров функции")

        # Проверяем, что chars имеет значение по умолчанию "$%!?@#"
        chars_param = params["chars"]
        if chars_param.default != '$%!?@#':
            raise ValueError("Параметр 'chars' должен иметь значение по умолчанию '$%!?@#'")

        # Проходим по каждому тесту
        for i in range(len(test_input)):
            args = test_input[i]
            expected = expected_output[i]

            # Вызываем функцию и передаем входные значения для теста
            output = func(args)

            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные: {test_input[i]}")
            test_result.append(f"Ожидалось: {expected}")

            if output == expected:
                test_result.append(f"Получено: {output}\n")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected}\nно получен: {output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)

    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
