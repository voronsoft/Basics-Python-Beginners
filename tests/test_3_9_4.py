# 3_9_4 тест для задачи
def test_3_9_4(*args):
    # Ожидается
    expected = sorted(["a[1][2][1][0]"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
