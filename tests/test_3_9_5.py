# 3_9_5 тест для задачи
def test_3_9_5(*args):
    # Ожидается
    expected = sorted(["del a[1][2][2]"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
