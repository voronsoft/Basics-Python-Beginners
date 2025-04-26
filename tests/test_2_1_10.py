# 2_1_10 тест для задачи
def test_2_1_10(*args):
    expected = sorted(['b = True', 'b = 5.8', 'b = hello'])
    user_output = sorted((args[0].split(";_")))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
