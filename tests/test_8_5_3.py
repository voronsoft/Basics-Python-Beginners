# 8_5_3 тест для задачи
def test_8_5_3(*args):
    # Ожидается
    expected = sorted(["чтение"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
