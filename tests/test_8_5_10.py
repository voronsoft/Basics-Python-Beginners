# 8_5_10 тест для задачи
def test_8_5_10(*args):
    # Ожидается
    expected = sorted(
        ["чтобы не потерялись записанные данные в файл", "для освобождения ресурсов, связанных с этим файлом"]
    )
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
