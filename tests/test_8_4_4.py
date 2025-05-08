# 8_4_4 тест для задачи
def test_8_4_4(*args):
    # Ожидается
    expected = sorted(["from .panda import *", "from panda_pack.panda import *", "import panda_pack.panda"])
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
