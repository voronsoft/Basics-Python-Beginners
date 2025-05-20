# 2_1_8 тест для задачи
def test_2_1_8(*args):
    expected = sorted(['S', 'TT1', '__arg_c__', '_b', 'd25', 'var_a'])
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
