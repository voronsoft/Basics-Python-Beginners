# 8_5_1 тест для задачи
def test_8_5_1(*args):
    # Ожидается
    expected = sorted(["открывает файл на чтение или запись"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
