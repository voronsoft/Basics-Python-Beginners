# 2_5_4 тест для задачи
def test_2_5_4(*args):

    expected = sorted(["True"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
