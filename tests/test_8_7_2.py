# 8_7_2 тест для задачи
def test_8_7_2(*args):
    # Ожидается
    expected = sorted(["будет создан новый пустой файл"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
