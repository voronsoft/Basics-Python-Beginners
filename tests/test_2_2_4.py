# 2_2_4 тест для задачи
def test_2_2_4(*args):
    expected = sorted(["float"])
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
