# 2_5_3 тест для задачи
def test_2_5_3(*args):
    expected = sorted(["False"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
