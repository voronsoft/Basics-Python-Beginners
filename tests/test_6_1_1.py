# 6_1_1 тест для задачи
def test_6_1_1(*args):
    expected = sorted(
        [
            'dict()',
            "dict([[1, 'one'], [2, 'two'], [3, 'three']])",
            "dict(you='ты', we='мы', they='они', us='нам')",
            "{river: река, 'road': 'Дорога', 'one': 1}",
            '{}',
        ]
    )
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
