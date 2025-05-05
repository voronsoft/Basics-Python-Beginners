# 8_5_4 тест для задачи
def test_8_5_4(*args):
    # Ожидается
    expected = sorted(["файл text.dat открывается на чтение в кодировке UTF-8"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
