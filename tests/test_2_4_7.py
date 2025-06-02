# 2_4_7 тест для задачи
def test_2_4_7(*args):
    expected = sorted(["d = input()"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
