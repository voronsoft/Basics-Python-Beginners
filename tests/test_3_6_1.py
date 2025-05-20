# 3_6_1 тест для задачи
def test_3_6_1(*args):
    expected = sorted(["к изменяемым"])
    user_output = sorted(args[0].split(";_"))
    # print(expected)
    # print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
