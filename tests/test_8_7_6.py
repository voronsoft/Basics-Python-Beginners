# 8_7_6 тест для задачи
def test_8_7_6(*args):
    # Ожидается
    expected = sorted(["для дозаписи информации в файл и считывания ранее записанных данных"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
