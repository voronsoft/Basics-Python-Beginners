# 3_2_3 тест для задачи
def test_3_2_3(*args):
    expected = sorted(["и"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
