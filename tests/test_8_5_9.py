# 8_5_9 тест для задачи
def test_8_5_9(*args):
    # Ожидается
    expected = sorted(["список из всех строк файла"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."