# 8_2_1 тест для задачи
def test_8_2_1(*args):
    # Ожидается
    expected = sorted(['from panda import *', 'import panda'])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
