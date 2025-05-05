# 8_2_6 тест для задачи
def test_8_2_6(*args):
    # Ожидается
    expected = sorted(["модуль импортируется и строчка с функцией print будет выполнена"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."