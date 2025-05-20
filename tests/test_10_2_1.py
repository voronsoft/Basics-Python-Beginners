# 10_2_1 тест для задачи
def test_10_2_1(*args):

    expected = dict(
        sorted(
            {
                '&': 'битовое И',
                '<<': 'сдвиг бит влево',
                '>>': 'сдвиг бит вправо',
                '^': 'исключающее ИЛИ (XOR)',
                '|': 'битовое ИЛИ',
                '~': 'битовое НЕ',
            }.items()
        )
    )

    user_output = dict(sorted(args[0].items()))
    assert expected == user_output, "Нет, это неправильный ответ."
