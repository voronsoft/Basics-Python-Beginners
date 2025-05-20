# 8_5_8 тест для задачи
def test_8_5_8(*args):
    # Ожидается
    expected = sorted(["t1 - первую строку, а t2 - вторую строку"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
