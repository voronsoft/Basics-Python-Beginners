# 8_4_2 тест для задачи
def test_8_4_2(*args):
    # Ожидается
    expected = sorted(["from panda_pack import *", "import panda_pack"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
