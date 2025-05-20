# 8_7_4 тест для задачи
def test_8_7_4(*args):
    # Ожидается
    expected = sorted(['две строчки Hello одна за другой (в строчку)'])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
