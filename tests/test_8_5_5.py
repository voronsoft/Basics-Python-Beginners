# 8_5_5 тест для задачи
def test_8_5_5(*args):
    # Ожидается
    expected = sorted(
        ["из файла text.dat будут прочитаны первые 4 символа (символы могут состоять из нескольких байтов)"]
    )
    # Получено
    user_output = sorted(args[0].split(";_"))
    # print(expected)
    # print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
