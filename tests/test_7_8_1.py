# 7_8_1 тест для задачи
def test_7_8_1(*args):
    # Ожидается
    expected = sorted(['lambda a: -a', 'lambda x, y: x+y', 'lambda x: x', 'lambda: hello lambda'])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
