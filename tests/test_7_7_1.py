# 7_7_1 тест для задачи
def test_7_7_1(*args):
    # Ожидается
    expected = sorted(['это функция, которая вызывает саму себя'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."