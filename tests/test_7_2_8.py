# 7_2_8 тест для задачи
import importlib.util
import io
import sys


def test_7_2_8(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Проверяем обязательные элементы в коде
    with open(path_tmp_file, "r", encoding="utf-8") as f:
        user_code = f.read()

    # Проверяем наличие ключевых конструкций
    required_elements = ('a = sorted(d, key=d.get', 'print(*a)')
    for elem in required_elements:
        if elem not in user_code:
            raise ValueError(f"------------- FAIL Тест -------------\nВ коде не найдено: {elem}")

    # Входные данные и ожидаемые результаты
    test_input = ("Копенгаген Амстердам Варшава Дублин Прага Рим",)
    expected_output = ("Рим Прага Дублин Варшава Амстердам Копенгаген",)

    result = []  # Список для накопления результатов тестов

    # Настройка модуля
    spec = importlib.util.spec_from_file_location("user_module", path_tmp_file)
    user_module = importlib.util.module_from_spec(spec)
    sys.modules["user_module"] = user_module

    try:
        for i in range(len(test_input)):
            test_result = [
                f"---------------OK Тест: {i + 1} --------------",
                f"Входные данные: {test_input[i]}",
                f"Ожидалось: {expected_output[i]}",
            ]

            # Имитируем ввод и выполняем код
            sys.stdin = io.StringIO(test_input[i])
            # Заглушка для sys.stderr
            original_stderr = sys.stderr  # сохраняем оригинал
            sys.stderr = io.StringIO()  # подменяем на буфер

            spec.loader.exec_module(user_module)

            # Проверяем наличие переменных (добавляем проверку словаря d)
            if not hasattr(user_module, "d"):
                raise ValueError(f"------------- FAIL Тест {i + 1} --------\nСловарь d не найден")
            if not hasattr(user_module, "a"):
                raise ValueError(f"------------- FAIL Тест {i + 1} --------\nСписок a не найден")

            # Проверяем корректность словаря d
            cities = test_input[i].split()
            for city in cities:
                if city not in user_module.d:
                    raise ValueError(f"Город '{city}' отсутствует в словаре d")
                if user_module.d[city] != len(city):
                    raise ValueError(f"Неверная длина для города '{city}'")

            # Получаем результат
            output = ' '.join(user_module.a)
            test_result.append(f"Получено: {output}")

            # Сравниваем результат с ожидаемым значением
            if output != expected_output[i]:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
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
