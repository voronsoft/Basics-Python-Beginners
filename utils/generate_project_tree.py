from pathlib import Path
from urllib.parse import quote

from config import PROJECT_ROOT


def create_project_tree_files(
    root_path,
    md_file='README_project_tree.md',
    html_file='README_project_tree.html',
    ignore=None,
):
    """
    Создаёт визуальное дерево проекта и сохраняет его в двух файлах:
    1. Markdown (с кликабельными ссылками и отступами)
    2. HTML (интерактивное дерево, где папки можно разворачивать)

    :param root_path: Путь к корню проекта.
    :param md_file: Имя Markdown-файла.
    :param html_file: Имя HTML-файла.
    :param ignore: Список имён файлов/папок, которые нужно игнорировать.
    """
    root = Path(root_path).resolve()
    if ignore is None:
        ignore = []

    def is_ignored(entry: Path) -> bool:
        return entry.name in ignore

    def walk_tree_md_list(path: Path, level=0) -> list[str]:
        """
        Создаёт Markdown-структуру через вложенные списки с кликабельными ссылками.
        """
        lines = []
        try:
            entries = sorted(
                [e for e in path.iterdir() if not is_ignored(e)],
                key=lambda x: (not x.is_dir(), x.name.lower())
            )
        except PermissionError:
            return lines

        indent = '  ' * level  # два пробела на уровень

        for entry in entries:
            relative_path = quote(entry.relative_to(root).as_posix())
            if entry.is_dir():
                lines.append(f"{indent}- 📁 **[{entry.name}/]({relative_path}/)**")
                lines.extend(walk_tree_md_list(entry, level + 1))
            else:
                lines.append(f"{indent}- 📄 [{entry.name}]({relative_path})")
        return lines

    def walk_tree_html(path: Path) -> str:
        """
        Создаёт HTML-древовидную структуру с кликабельными ссылками и collapsible-узлами.
        """
        html = ""
        try:
            entries = sorted(
                [e for e in path.iterdir() if not is_ignored(e)],
                key=lambda x: (not x.is_dir(), x.name.lower())
            )
        except PermissionError:
            return html

        for entry in entries:
            relative_path = entry.relative_to(root).as_posix()

            if entry.is_dir():
                html += f"<details><summary>📁 <a href='{relative_path}/' target='_blank'>{entry.name}/</a></summary>\n"
                html += walk_tree_html(entry)
                html += "</details>\n"
            else:
                html += f"<div style='margin-left:20px;'>📄 <a href='{relative_path}' target='_blank'>{entry.name}</a></div>\n"
        return html

    # Markdown
    tree_lines = walk_tree_md_list(root)
    with (root / md_file).open('w', encoding='utf-8') as f_md:
        f_md.write(f"# Структура проекта ({root.name})\n\n")
        f_md.writelines(line + '\n' for line in tree_lines)
    print(f"✅ Markdown-файл сохранён: {md_file}")

    # HTML
    html_tree = walk_tree_html(root)
    html_template = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Структура проекта ({root.name})</title>
    <style>
        body {{
            font-family: Consolas, monospace;
            background-color: #f9f9f9;
            padding: 20px;
        }}
        summary {{
            cursor: pointer;
            font-weight: bold;
        }}
        details {{
            margin-left: 20px;
        }}
    </style>
</head>
<body>
    <h1>Структура проекта: {root.name}</h1>
    {html_tree}
</body>
</html>
"""
    with (root / html_file).open('w', encoding='utf-8') as f_html:
        f_html.write(html_template)
    print(f"✅ HTML-файл сохранён: {html_file}")


if __name__ == '__main__':
    create_project_tree_files(
        root_path=PROJECT_ROOT,
        md_file='README_project_tree.md',
        html_file='README_project_tree.html',
        ignore=[
            '.venv',
            '__pycache__',
            '.git',
            '.idea',
            'build',
            'dist',
            'installer_files',
            'README_project_tree.md',
            'README_project_tree.html',
        ],
    )
    print("PROJECT_ROOT", PROJECT_ROOT)
