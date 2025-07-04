# 2_2_7 тест для задачи
from utils.code_security_check import check_code_safety


def test_2_2_7(path_tmp_file: str, task_num_test: str):
    # Безопасность кода пользователя: читаем код и проверяем его до запуска
    with open(path_tmp_file, "r", encoding="utf-8") as f:
        user_code = f.read()
    check_code_safety(user_code)

    expected = "16"
    try:
        with open(path_tmp_file, 'r', encoding='utf-8') as file:
            user_output = file.read()  # Читаем весь файл целиком
            user_output = user_output.replace("# Форматирование кода Ctrl+Alt+l или Ctrl+Alt+f", "").strip()
            assert expected == user_output, "Нет, это неправильный ответ."
            return True, user_output
    except Exception as e:
        raise e
