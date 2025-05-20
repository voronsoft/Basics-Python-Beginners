# 5_6_2 тест для задачи
import subprocess
import sys


def test_5_6_2(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    # Входные данные
    test_input = (
        "django chto  eto takoe    poryadok ustanovki\nmodel mtv   marshrutizaciya funkcii  predstavleniya\nmarshrutizaciya  obrabotka isklyucheniy       zaprosov perenapravleniya",
        "opredelenie  modeley   migracii sozdanie vypolnenie\ncrud      osnovy         orm po rabote s  modelyami\ndjango-shablony  templates-nachalo\npodklyuchenie-staticheskih-faylov-filtry-shablonov",
        "eto  ssilka na   etot  kurs\nglava    5 razdel   6   urok          2",
    )
    # Ожидаемый результат
    expected_output = (
        "django-chto-eto-takoe-poryadok-ustanovki\nmodel-mtv-marshrutizaciya-funkcii-predstavleniya\nmarshrutizaciya-obrabotka-isklyucheniy-zaprosov-perenapravleniya",
        "opredelenie-modeley-migracii-sozdanie-vypolnenie\ncrud-osnovy-orm-po-rabote-s-modelyami\ndjango-shablony-templates-nachalo\npodklyuchenie-staticheskih-faylov-filtry-shablonov",
        "eto-ssilka-na-etot-kurs\nglava-5-razdel-6-urok-2",
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
                test_result.append(f"Получено:\n{output}")
            else:
                raise ValueError(
                    f"------------- FAIL Тест: {i + 1} --------\n"
                    f"Входные данные:\n{test_input[i]}\n"
                    f"Ожидалось:\n{expected_output[i]}\nно получен:\n{output}\n"
                )

            result.append("\n".join(test_result))

        return True, "\n".join(result)  # Возвращаем статус и результаты тестов
    except Exception as e:
        # Добавляем информацию об ошибке к результатам
        error_info = "\n".join(result) + f"\n{e}"
        raise RuntimeError(f"Ошибка выполнения кода:\n\n{error_info}")
