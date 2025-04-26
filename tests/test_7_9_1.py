# 7_9_1 тест для задачи
def test_7_9_1(*args):
    # Ожидается
    expected = sorted(['чтобы менять глобальные переменные в локальном окружении (например, внутри функций)'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
