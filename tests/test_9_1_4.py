# 9_1_4 тест для задачи
def test_9_1_4(*args):
    # Ожидается
    expected = sorted(["list(gen)", "tuple(gen)", "max(gen)", "min(gen)", "set(gen)", "sum(gen)"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
