# 8_2_9 тест для задачи
def test_8_2_9(*args):
    # Ожидается
    expected = sorted(["позволяет повторно импортировать модули"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
