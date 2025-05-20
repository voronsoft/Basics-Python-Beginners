# 2_1_9 тест для задачи
def test_2_1_9(*args):
    expected = sorted(["да"])
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
