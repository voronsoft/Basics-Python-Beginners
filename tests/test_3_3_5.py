# 3_3_5 тест для задачи
def test_3_3_5(*args):
    expected = sorted(["значение -1"])
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
