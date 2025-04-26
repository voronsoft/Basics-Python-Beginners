# 3_1_6 тест для задачи
def test_3_1_6(path_tmp_file: str, task_num_test: str):
    """Функция тестирования кода пользователя"""
    expected = "787878"
    try:
        with open(path_tmp_file, 'r', encoding='utf-8') as file:
            user_output = file.read()  # Читаем весь файл целиком
            user_output = user_output.replace("# Форматирование кода Ctrl+Alt+l или Ctrl+Alt+f", "").strip()
            assert expected == user_output, "Нет, это неправильный ответ."
            return True, user_output
    except Exception as e:
        raise e
