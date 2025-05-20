# 10_6_3 тест для задачи
def test_10_6_3(*args):
    # Ожидается
    expected = sorted(
        [
            "case {'marks': ms, 'age': age} if ms.count(2) > 1: ...",
            "case {'marks': ms, 'fio': str(fio)} if ms.count(2) > 1: ...",
            "case {'marks': ms, 'age': age, 'fio': fio} if ms.count(2) > 1: ...",
            "case {'marks': ms, 'age': int() | float() as age, 'fio': fio} if ms.count(2) > 1: ...",
        ]
    )
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
