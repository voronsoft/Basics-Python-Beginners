# 2_4_6 тест для задачи
def test_2_4_6(*args):
    expected = sorted(["d = int(input())"])
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
