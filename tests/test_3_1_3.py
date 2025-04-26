# 3_1_3 тест для задачи
def test_3_1_3(*args):

    expected = sorted([r'\n'])
    user_output = sorted(args[0].split(";_"))
    print(111, user_output)
    print(222, expected)
    assert expected == user_output, "Нет, это неправильный ответ."
