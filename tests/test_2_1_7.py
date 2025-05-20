# 2_1_7 тест для задачи
def test_2_1_7(*args):
    expected = sorted(["для определения типа переменной или объекта"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
