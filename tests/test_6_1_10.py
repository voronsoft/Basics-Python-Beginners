# 6_1_10 тест для задачи
import subprocess
import sys


def test_6_1_10(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "ustanovka-i-zapusk-yazyka\nustanovka-i-poryadok-raboty-pycharm\nperemennyye-operator-prisvaivaniya-tipy-dannykh\narifmeticheskiye-operatsii\nustanovka-i-poryadok-raboty-pycharm",
        "osnovy-raboty-so-strokami\nindeksy-i-srezy-strok\nalgoritmy-obrabotki-spiskov\nosnovy-raboty-so-strokami\nalgoritm-evklida\ninstrument-list-comprehensions\nindeksy-i-srezy-strok\ndekoratory-funkciy-i-zamykaniya",
        "osnovy-raboty-so-strokami\nindeksy-i-srezy-strok\nalgoritmy-obrabotki-spiskov\nosnovy-raboty-so-strokami\nalgoritm-evklida\ninstrument-list-comprehensions\nindeksy-i-srezy-strok\ndekoratory-funkciy-i-zamykaniya\nosnovy-raboty-so-strokami",
    )
    # Ожидаемый результат
    expected_output = (
        "HTML-страница для адреса ustanovka-i-zapusk-yazyka\nHTML-страница для адреса ustanovka-i-poryadok-raboty-pycharm\nHTML-страница для адреса peremennyye-operator-prisvaivaniya-tipy-dannykh\nHTML-страница для адреса arifmeticheskiye-operatsii\nВзято из кэша: HTML-страница для адреса ustanovka-i-poryadok-raboty-pycharm",
        "HTML-страница для адреса osnovy-raboty-so-strokami\nHTML-страница для адреса indeksy-i-srezy-strok\nHTML-страница для адреса algoritmy-obrabotki-spiskov\nВзято из кэша: HTML-страница для адреса osnovy-raboty-so-strokami\nHTML-страница для адреса algoritm-evklida\nHTML-страница для адреса instrument-list-comprehensions\nВзято из кэша: HTML-страница для адреса indeksy-i-srezy-strok\nHTML-страница для адреса dekoratory-funkciy-i-zamykaniya",
        "HTML-страница для адреса osnovy-raboty-so-strokami\nHTML-страница для адреса indeksy-i-srezy-strok\nHTML-страница для адреса algoritmy-obrabotki-spiskov\nВзято из кэша: HTML-страница для адреса osnovy-raboty-so-strokami\nHTML-страница для адреса algoritm-evklida\nHTML-страница для адреса instrument-list-comprehensions\nВзято из кэша: HTML-страница для адреса indeksy-i-srezy-strok\nHTML-страница для адреса dekoratory-funkciy-i-zamykaniya\nВзято из кэша: HTML-страница для адреса osnovy-raboty-so-strokami",
    )

    result = []  # Список для накопления результатов тестов

    try:
        for i in range(len(test_input)):
            # Запускаем код пользователя, передавая ему входные данные через stdin
            process = subprocess.run(
                ["python", "-I", "-E", "-X", "utf8", path_tmp_file],  # Запускаем временный файл
                input=test_input[i],  # Передаём input
                text=True,  # Режим работы с текстом
                capture_output=True,  # Захватываем stdout и stderr
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                encoding="utf-8",  # Явно указываем кодировку
                timeout=5,  # Важно: ограничение времени выполнения кода
            )

            # Получаем результат (stdout)
            output = process.stdout.strip()
            # Получаем сообщения об ошибках
            error = process.stderr.strip()
            if error:  # Если есть ошибки в коде выводим
                raise ValueError(error)

            test_result = list()
            test_result.append(f"---------------OK Тест: {i + 1} --------------")
            test_result.append(f"Входные данные:\n{test_input[i]}")
            test_result.append(f"Ожидалось:\n{expected_output[i]}")

            # Сравниваем результат с ожидаемым значением
            if output == expected_output[i]:
                test_result.append(f"Получено:\n{output}\n")

            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен: {output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
