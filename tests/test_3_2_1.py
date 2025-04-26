# 3_2_1 тест для задачи
def test_3_2_1(*args):

    expected = sorted(["к неизменяемым типам"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
