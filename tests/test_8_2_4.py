# 8_2_4 тест для задачи
def test_8_2_4(*args):
    # Ожидается
    expected = sorted(['from panda import PND, panda_say', 'import panda'])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
