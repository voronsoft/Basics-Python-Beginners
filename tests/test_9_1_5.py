# 9_1_5 тест для задачи
def test_9_1_5(*args):
    # Ожидается
    expected = sorted(["меньший расход памяти", "возможность оперировать очень большими объемами данных"])
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
