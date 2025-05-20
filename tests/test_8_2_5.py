# 8_2_5 тест для задачи
def test_8_2_5(*args):
    # Ожидается
    expected = sorted(["модуль panda импортируется только один (первый) раз"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
