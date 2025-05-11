# 9_8_1 тест для задачи
def test_9_8_1(*args):
    # Ожидается
    expected = sorted(
        [
            "пример вызова функции: type(x) == bool",
            "пример вызова функции: type(x) in (float, int)",
            "функция isinstance выполняет проверку типов с учетом их наследования",
            "пример вызова функции: isinstance(x, float)",
            "пример вызова функции: isinstance(x, (str, float))",
            "функция type возвращает фактический тип для переданного ей аргумента (без учета наследования)",
            "пример вызова функции: type(x) is int",
        ]
    )
    # Получено
    user_output = sorted(args[0].split(";_"))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
