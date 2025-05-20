# 7_2_7 тест для задачи
import importlib.util
import io
import sys


def test_7_2_7(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные и ожидаемые результаты (как у вас)
    test_input = (
        "Пекин Сеул Джакарта Бангкок Дели",
        "Токио Берлин Париж Мадрид Рим Лиссабон Сидней",
    )
    # Ожидаемый результат
    expected_output = (
        "Джакарта Бангкок",
        "Берлин Мадрид Лиссабон Сидней",
    )

    result = []  # Список для накопления результатов тестов

    # Настройка модуля
    spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
    user_module = importlib.util.module_from_spec(spec)
    sys.modules["user_module"] = user_module

    try:
        for i in range(len(test_input)):
            test_result = [
                f"--------------- Тест {i + 1} --------------",
                f"Входные данные: {test_input[i]}",
                f"Ожидалось: {expected_output[i]}",
            ]

            # Имитируем ввод и выполняем код
            sys.stdin = io.StringIO(test_input[i])
            # Заглушка для sys.stderr
            original_stderr = sys.stderr  # сохраняем оригинал
            sys.stderr = io.StringIO()  # подменяем на буфер

            spec.loader.exec_module(user_module)

            # Проверяем наличие переменных
            if not hasattr(user_module, "cities"):
                raise ValueError(f"------------- FAIL Тест {i + 1} --------\nПеременная cities не найдена")
            elif not hasattr(user_module, "lst"):
                raise ValueError(f"------------- FAIL Тест {i + 1} --------\nПеременная lst не найдена")

            # Получаем результат
            output = ' '.join(user_module.lst)
            test_result.append(f"Получено: {output}\n")

            # Сравниваем результат с ожидаемым значением
            if output != expected_output[i]:
                raise ValueError(
                    f"------------- FAIL Тест {i + 1} --------\n"
                    f"Входные данные: {test_input[i]}\n"
                    f"Ожидалось: {expected_output[i]}\n"
                    f"Получено: {output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)
    except Exception as e:
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
    finally:
        sys.stdin = sys.__stdin__
