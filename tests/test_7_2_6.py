# 7_2_6 тест для задачи
import importlib.util
import io
import sys
import inspect


def test_7_2_6(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Тестовые данные: (ввод, ожидаемое кол-во аргументов, аргументы, ожидаемый результат)
    test_input = [
        ("RECT", 2, (5, 2), 10),
        ("SQ", 1, (5,), 25),
        ("OTHER", 1, (4,), 16),
    ]

    result = []  # Список для накопления результатов

    try:
        # Настройка модуля
        spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
        user_module = importlib.util.module_from_spec(spec)
        sys.modules["user_module"] = user_module

        for i in range(len(test_input)):
            input_data, expected_args, call_args, expected = test_input[i]

            # Подготовка теста
            test_result = [
                f"---------------OK Тест: {i + 1} --------------",
                f"Входные данные: tp='{input_data}'",
                f"Аргументы функции: {call_args}",
                f"Ожидалось аргументов: {expected_args}",
            ]

            # Имитация ввода и выполнение
            sys.stdin = io.StringIO(input_data)
            spec.loader.exec_module(user_module)

            # Проверка наличия функции
            if not hasattr(user_module, "get_sq"):
                raise ValueError("Функция 'get_sq' не найдена")

            # Проверка количества аргументов
            actual_args = len(inspect.getfullargspec(user_module.get_sq).args)
            test_result.append(f"Получено аргументов: {actual_args}")

            if actual_args != expected_args:
                raise ValueError(
                    f"------------- FAIL Тест {i+1} --------\n"
                    f"Неверное количество аргументов\n"
                    f"Ожидалось: {expected_args}\n"
                    f"Получено: {actual_args}\n"
                )

            # Проверка результата
            output = user_module.get_sq(*call_args)
            test_result.append(f"Ожидаемый результат: {expected}")
            test_result.append(f"Получено: {output}\n")

            # Сравниваем результат с ожидаемым значением
            if output != expected:
                raise ValueError(
                    f"------------- FAIL Тест {i+1} --------\n"
                    f"Неверный результат вычислений\n"
                    f"Ожидалось: {expected}\n"
                    f"Получено: {output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)
    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
    finally:
        sys.stdin = sys.__stdin__
