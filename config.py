import os
import sys

from pathlib import Path

# Определяем базовый путь
if getattr(sys, 'frozen', False):
    # ЕСЛИ ПРИЛОЖЕНИЕ ЗАПУЩЕНО КАК .EXE ИСПОЛЬЗУЕМ ДИРЕКТОРИЮ КУДА БЫЛО УСТАНОВЛЕНО ПРИЛОЖЕНИЕ Basics Python Beginners.EXE
    PROJECT_ROOT = Path(sys.executable).parent
    # Путь к json если приложение собрано в .exe
    JSON_COMPLETED_TASKS = Path(os.getenv('LOCALAPPDATA')) / "Basics Python Beginners" / "data" / "completed_tasks.json"
    # Путь к файлу json - сохранение состояния активного (выбранного) элемента
    # (для запуска приложения с пункта на котором в прошлый раз была закрыта программа).
    JSON_FILE_TREE_CONDITION = Path(os.getenv('LOCALAPPDATA')) / "Basics Python Beginners" / "data" / "tree_condition.json"
else:
    # ЕСЛИ ПРИЛОЖЕНИЕ ЗАПУЩЕНО КАК СКРИПТ PYTHON, ИСПОЛЬЗУЕМ ДИРЕКТОРИЮ СКРИПТА
    PROJECT_ROOT = Path(__file__).resolve().parent
    # Путь к json, режим разработки - используем папку проекта/data
    JSON_COMPLETED_TASKS = PROJECT_ROOT / "data" / "completed_tasks.json"
    # Путь к файлу json - сохранение состояния активного (выбранного) элемента
    # (для запуска приложения с пункта на котором в прошлый раз была закрыта программа).
    JSON_FILE_TREE_CONDITION = PROJECT_ROOT / "data" / "tree_condition.json"

# Путь к папке с заданиями/задачами
TASKS_PATH = PROJECT_ROOT / "tasks"
# Путь к папке с описанием(.html) для заданий
TASKS_DESCR_HTML_PATH = PROJECT_ROOT / "tasks_descriptions_html"
# Путь к папке с видео файлами для занятий
VIDEO_PATH = PROJECT_ROOT / "tasks_video"
# Путь к папке с детальными решениями задач
VIDEO_PATH_DTL_SOL = VIDEO_PATH / "detailed_solutions"
# Путь к папке с изображениями
IMAGES_PATH = PROJECT_ROOT / "img"
# Путь к папке с временными файлами
TESTS_PATH = PROJECT_ROOT / "tests"

# Кеш файлов в директории с описанием заданий
TASK_FILES_CACHE = {f.name for f in TASKS_DESCR_HTML_PATH.iterdir() if f.is_file()}
# Кеш файлов в директории с видео
VIDEO_CACHE = {f.name for f in VIDEO_PATH.iterdir() if f.is_file()}

if __name__ == "__main__":
    # Выводим пути в консоль для проверки
    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("JSON_COMPLETED_TASKS:", JSON_COMPLETED_TASKS)
    print("JSON_FILE_TREE_CONDITION:", JSON_FILE_TREE_CONDITION)
    print("TASKS_PATH:", TASKS_PATH)
    print("TASKS_DESCR_HTML_PATH:", TASKS_DESCR_HTML_PATH)
    print("VIDEO_PATH:", VIDEO_PATH)
    print("VIDEO_PATH_DTL_SOL:", VIDEO_PATH_DTL_SOL)
    print("IMAGES_PATH:", IMAGES_PATH)
    print("TESTS_PATH:", TESTS_PATH)

    # Если нужно вывести, где ищется CSS, JS или HTML файлы
    print("Path to .HTML file:", TASKS_DESCR_HTML_PATH / "index.html")
    print("Path to .CSS file:", TASKS_DESCR_HTML_PATH / "css" / "style.css")
    print("Path to .JS file:", TASKS_DESCR_HTML_PATH / "js" / "style.js")
