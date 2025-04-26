# 7_9_2 тест для задачи
def test_7_9_2(*args):
    # Ожидается
    expected = sorted(['чтобы из одной лок/области обращаться к лок переменной из внешней лок/области для ее изменения'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
