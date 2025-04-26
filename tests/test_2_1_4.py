# 2_1_4 тест для задачи
def test_2_1_4(*args):

    expected = sorted(["копирование ссылки и обе переменные ссылаются на один и тот же объект"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
