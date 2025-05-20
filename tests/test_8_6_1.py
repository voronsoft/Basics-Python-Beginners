# 8_6_1 тест для задачи
def test_8_6_1(*args):
    # Ожидается
    expected = sorted(["возникнет ошибка FileNotFoundError"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
