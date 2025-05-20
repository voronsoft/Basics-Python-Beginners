# 8_6_6 тест для задачи
def test_8_6_6(*args):
    # Ожидается
    expected = sorted(["при возникновении соответствующих ошибок в блоке try"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
