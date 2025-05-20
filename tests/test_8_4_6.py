# 8_4_6 тест для задачи
def test_8_4_6(*args):
    # Ожидается
    expected = sorted(["импортируется только модуль panda1"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
