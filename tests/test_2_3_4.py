# 2_3_4 тест для задачи
def test_2_3_4(*args):
    expected = sorted(['import math'])
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Увы, это неправильный ответ."
