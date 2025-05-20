# 5_5_5 тест для задачи
def test_5_5_5(*args):
    # Ожидается
    expected = sorted(['ошибка StopIteration'])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
