# 8_2_3 тест для задачи
def test_8_2_3(*args):
    # Ожидается
    expected = sorted(['from panda import *', 'import panda'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
