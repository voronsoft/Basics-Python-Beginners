# 3_6_5 тест для задачи
def test_3_6_5(*args):
    expected = sorted(["3", "-3"])
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
