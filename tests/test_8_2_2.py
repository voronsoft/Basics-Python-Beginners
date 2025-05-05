# 8_2_2 тест для задачи
def test_8_2_2(*args):
    # Ожидается
    expected = sorted(['from libs.panda import *', 'import libs.panda'])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."