# 8_1_1 тест для задачи
def test_8_1_1(*args):
    # Ожидается
    expected = sorted(['from time import *', 'import time', 'import time as tm'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
