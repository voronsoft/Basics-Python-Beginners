from collections import deque

import wx

from config import IMAGES_PATH, JSON_COMPLETED_TASKS, JSON_FILE_TREE_CONDITION
from task_tree.task_structure import structure_task
from utils.func_utils import read_json_file, write_json_file


class TaskTree(wx.TreeCtrl):
    """Класс дерева заданий"""

    def __init__(self, parent, id=wx.ID_ANY):
        # Инициализация родительского класса (wx.TreeCtrl)
        super().__init__(parent, id=wx.ID_ANY)

        # Файл для хранения состояния дерева
        self.state_file = JSON_FILE_TREE_CONDITION

        # Загружаем статусы заданий
        self.task_status = read_json_file(JSON_COMPLETED_TASKS)

        # Создаем ImageList для хранения иконок
        self.il = wx.ImageList(16, 16)
        # Загрузка иконок
        self.icons = {
            "folder": self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16))),
            "home": self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, wx.ART_OTHER, (16, 16))),
            "file": self.il.Add(wx.Bitmap(str(IMAGES_PATH / "file.ico"), wx.BITMAP_TYPE_ICO)),
            "info": self.il.Add(wx.Bitmap(str(IMAGES_PATH / "info.ico"), wx.BITMAP_TYPE_ICO)),
            "question": self.il.Add(wx.Bitmap(str(IMAGES_PATH / "question.ico"), wx.BITMAP_TYPE_ICO)),
            "dragdrop": self.il.Add(wx.Bitmap(str(IMAGES_PATH / "dragdrop.ico"), wx.BITMAP_TYPE_ICO)),
            "success": self.il.Add(wx.Bitmap(str(IMAGES_PATH / "success.ico"), wx.BITMAP_TYPE_ICO)),
        }
        self.SetImageList(self.il)

        # Добавляем корневой элемент
        root = self.AddRoot(structure_task[0][0])
        # Устанавливаем иконку элементу
        self.SetItemImage(root, self.icons[structure_task[0][1]])
        # Строим дерево
        self.build_tree(root, structure_task[0][2])

        # Восстанавливаем состояние дерева
        self.restore_state()

        # Подключаем событие выбора элемента
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_item_selected)

    def build_tree(self, parent, items):
        """Создаёт дерево с заданиями на основе структуры данных с учетом статуса"""
        stack = [(parent, items)]
        while stack:
            current_parent, children = stack.pop()
            for child in children:
                # если элемент не имеет потомков
                if len(child) == 2:
                    label, icon = child
                    sub_items = []  # Нет вложенных элементов
                # если элемент имеет потомков
                else:
                    label, icon, sub_items = child

                # Проверяем статус задания (True = выполнено)
                lbl = label.split(" ")[0]  # формируем название задания
                if lbl in self.task_status and self.task_status[lbl] is True:
                    icon_index = self.icons["success"]  # Иконка "выполнено"
                else:
                    icon_index = self.icons.get(icon, self.icons["folder"])  # Стандартная иконка

                # Создаем элемент
                item = self.AppendItem(current_parent, label)
                self.SetItemImage(item, icon_index)

                # Если есть подэлементы, добавляем их в стек
                if sub_items:
                    stack.append((item, sub_items))

    def find_item_by_label(self, label: str):
        """Итеративный поиск элемента по метке (без рекурсии)"""
        queue = deque([self.GetRootItem()])  # Начинаем с корневого элемента

        while queue:
            item = queue.popleft()  # Берем первый элемент из очереди

            if label == self.GetItemText(item).split(" ")[0]:
                print("----------------")
                print(label, " - ", self.GetItemText(item).split(" ")[0])
                print("----------------")
                return item  # Нашли нужный элемент

            # Добавляем всех детей в очередь
            child, _ = self.GetFirstChild(item)
            while child.IsOk():
                queue.append(child)
                child, _ = self.GetNextChild(item, _)

        return None  # Если не нашли

    def update_task_icon(self, task_name: str, icon_type: str = "success"):
        """
        Изменяет статус задачи.
        - меняет иконку задания на 'success', 'file', 'question', 'dragdrop', 'success'
        - сохраняет статус в JSON
        """
        icon_type = icon_type
        item = self.find_item_by_label(task_name)
        if item:
            # Меняем иконку
            self.SetItemImage(item, self.icons[icon_type])
            # Обновляем статус задания
            lbl = task_name.split(" ")[0]
            self.task_status[lbl] = True

    def set_default_task_icon(self, task_name: str, icon_type: str = "file"):
        """
        Изменяет статус задачи.
        - меняет иконку задания на 'success', 'file', 'question', 'dragdrop', 'success'
        - сохраняет статус в JSON
        """
        icon_type = icon_type
        # Находим элемент в дереве
        item = self.find_item_by_label(task_name)
        if item:
            # Меняем иконку
            self.SetItemImage(item, self.icons[icon_type])

    def on_item_selected(self, event):
        """Обработчик выбора элемента в дереве"""
        # Сохраняем текущее состояние при каждом изменении выбора
        self.save_state()
        event.Skip()

    def save_state(self):
        """Сохраняет текущее состояние дерева (выбранный элемент) в файл"""
        selected_item = self.GetSelection()
        if selected_item.IsOk():
            # Получаем полный путь к выбранному элементу
            path = list()
            item = selected_item
            while item.IsOk():
                path.insert(0, self.GetItemText(item))
                item = self.GetItemParent(item)
            print()
            # Сохраняем путь в файл
            write_json_file(data={'state_select_path': path}, file_path=JSON_FILE_TREE_CONDITION)

    def restore_state(self):
        """Восстанавливает состояние дерева из файла"""
        # Если файл не существует или что-то пошло не так - выбираем корень
        if not self.state_file.exists():
            root = self.GetRootItem()
            self.Expand(root)
            self.SelectItem(root)
            # Прокручиваем влево
            self.SetScrollPos(wx.HORIZONTAL, 0)
            return

        try:
            data = read_json_file(file_path=self.state_file)
            path = data.get("state_select_path", [])

            if not path:
                root = self.GetRootItem()
                self.Expand(root)
                self.SelectItem(root)
                # Прокручиваем влево
                self.SetScrollPos(wx.HORIZONTAL, 0)
                return

            # Проверяем корневой элемент
            root = self.GetRootItem()
            if not root.IsOk() or self.GetItemText(root) != path[0]:
                print("Корневой элемент не совпадает")
                self.Expand(root)
                self.SelectItem(root)
                # Прокручиваем влево
                self.SetScrollPos(wx.HORIZONTAL, 0)
                return

            # Начинаем поиск с корня
            current_item = root
            parents_to_expand = []
            # Флаг метка состояния поиска нужного элемента
            found = False
            # Проходим по остальным элементам пути (начиная с индекса 1)
            for label in path[1:]:
                child, cookie = self.GetFirstChild(current_item)

                while child.IsOk():
                    child_text = self.GetItemText(child)
                    # print(f"Сравниваем: '{child_text}' с '{label}'")
                    if child_text == label:
                        parents_to_expand.append(current_item)
                        current_item = child
                        found = True
                        break
                    child, cookie = self.GetNextChild(current_item, cookie)

                if not found:
                    print(f"Элемент '{label}' не найден")
                    break

            # Если дошли до конца пути
            if current_item.IsOk() and found:
                # Разворачиваем всех родителей
                for parent in parents_to_expand:
                    self.Expand(parent)
                # Выбираем элемент
                self.SelectItem(current_item)
                self.EnsureVisible(current_item)
                # Прокручиваем влево
                self.SetScrollPos(wx.HORIZONTAL, 0)
                # Эмулируем событие выбора найденного элемента запустив(загружаем) задачу в основном окне
                event = wx.TreeEvent(wx.wxEVT_TREE_SEL_CHANGED, self, current_item)
                wx.PostEvent(self.GetEventHandler(), event)
            else:
                # Если что-то пошло не так - выбираем корень
                self.Expand(root)
                self.SelectItem(root)
                # Прокручиваем влево
                self.SetScrollPos(wx.HORIZONTAL, 0)

        except Exception as e:
            print(f"Ошибка при восстановлении состояния: {e}")
            # При ошибке выбираем корень
            root = self.GetRootItem()
            self.Expand(root)
            self.SelectItem(root)
            # Прокручиваем влево
            self.SetScrollPos(wx.HORIZONTAL, 0)
