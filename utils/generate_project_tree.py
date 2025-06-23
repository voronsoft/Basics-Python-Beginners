from pathlib import Path
from urllib.parse import quote

from config import PROJECT_ROOT


def create_project_tree_files(
    root_path,
    md_file='README_project_tree.md',
    ignore=None,
):
    """
    Создаёт визуальное дерево проекта и сохраняет его в файл:
    Markdown (с кликабельными ссылками и отступами)

    :param root_path: Путь к корню проекта.
    :param md_file: Имя Markdown-файла.
    :param ignore: Список имён файлов/папок, которые нужно игнорировать.
    """
    root = Path(root_path).resolve()
    if ignore is None:
        ignore = []

    def is_ignored(entry: Path) -> bool:
        return entry.name in ignore

    def walk_tree_md_list(path: Path, level=0) -> list[str]:
        """
        Генерирует Markdown с раскрывающимися папками.
        Названия файлов кликабельны, но отображаются только как текст.
        """
        lines = []
        try:
            entries = sorted(
                [e for e in path.iterdir() if not is_ignored(e)],
                key=lambda x: (not x.is_dir(), x.name.lower()),
            )
        except PermissionError:
            return lines

        indent = '  ' * level

        for entry in entries:
            relative_path = quote(entry.relative_to(root).as_posix())
            if entry.is_dir():
                # Начало сворачиваемого блока
                lines.append(f'{indent}<details>')
                lines.append(f'{indent}  <summary>📁 {entry.name}/</summary>\n')
                # Рекурсивно добавляем содержимое
                lines.extend(walk_tree_md_list(entry, level + 1))
                lines.append(f'{indent}</details>\n')
            else:
                # Добавляем файл с отступом
                indent = '&nbsp;&nbsp;' * (level * 4)
                lines.append(f"{indent} -📄 [{entry.name}]({relative_path})  ")
        return lines

    # Markdown
    tree_lines = walk_tree_md_list(root)
    with (root / md_file).open('w', encoding='utf-8') as f_md:
        f_md.write(f"# Структура проекта (Basics Python Beginners)\n\n")
        f_md.writelines(line + '\n' for line in tree_lines)


if __name__ == '__main__':
    """Запуск генерации дерева файлов в проекте"""
    create_project_tree_files(
        root_path=PROJECT_ROOT,
        md_file='README_project_tree.md',
        ignore=[
            '.venv',
            '__pycache__',
            '.git',
            '.idea',
            'build',
            'dist',
            'installer_files',
            'README_project_tree.md',
            'project_notes.txt',
        ],
    )
