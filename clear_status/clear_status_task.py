import gettext

import wx

from config import IMAGES_PATH
from task_tree.task_structure import lst_task_type

_ = gettext.gettext
###########################################################################
## Class ClearStatusTask
###########################################################################


class ClearStatusTask(wx.Dialog):
    """Класс окна очистки статуса решенных заданий"""

    def __init__(self, parent):
        wx.Dialog.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=_(u"Сброс статуса заданий"),
            pos=wx.DefaultPosition,
            size=wx.Size(500, 500),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )
        self.SetSizeHints(wx.Size(500, 500), wx.DefaultSize)
        # Установка шрифта
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        # Устанавливаем иконку для окна
        icon = wx.Icon(str(IMAGES_PATH / "baby.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Главный родитель класса
        self.top_parent = self.Parent

        # Получаем ссылку на словарь статусов заданий из родительского класса
        self.task_status = self.top_parent.task_tree.task_status

        # Создаем ListCtrl с мультивыделением
        self.list_ctrl = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_LIST)

        # Заполняем список
        self.refresh_list()

        # Кнопки
        btn_reset = wx.Button(self, label="Сбросить статус полей? (Del)")
        btn_close = wx.Button(self, label="Закрыть (Esc)")

        # Разметка
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_reset, 0, wx.EXPAND | wx.ALL, 5)
        btn_sizer.Add(btn_close, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM)

        self.SetSizer(sizer)
        self.Layout()
        self.Centre(wx.BOTH)

        # Обработчики
        btn_reset.Bind(wx.EVT_BUTTON, self.on_reset)
        btn_close.Bind(wx.EVT_BUTTON, lambda e: self.Close())

        # Горячие клавиши
        accel_tbl = wx.AcceleratorTable(
            [(wx.ACCEL_NORMAL, wx.WXK_DELETE, wx.ID_DELETE), (wx.ACCEL_NORMAL, wx.WXK_ESCAPE, wx.ID_CANCEL)]
        )
        self.SetAcceleratorTable(accel_tbl)
        self.Bind(wx.EVT_MENU, self.on_reset, id=wx.ID_DELETE)
        self.Bind(wx.EVT_MENU, lambda e: self.Close(), id=wx.ID_CANCEL)

    def refresh_list(self):
        """Обновляет список заданий"""
        self.list_ctrl.DeleteAllItems()
        for task in sorted(self.task_status.keys()):  # Сортируем по алфавиту
            self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), task)

    def get_selected_tasks(self) -> list:
        """Возвращает список выделенных заданий"""
        selected = []
        index = self.list_ctrl.GetFirstSelected()
        while index != -1:
            selected.append(self.list_ctrl.GetItemText(index))
            index = self.list_ctrl.GetNextSelected(index)
        return selected

    def on_reset(self, event):
        selected = self.get_selected_tasks()
        if not selected:
            wx.MessageBox("Ничего не выбрано!", "Внимание", wx.ICON_WARNING)
            return

        # Подтверждение
        confirm = wx.MessageDialog(
            self, f"Сбросить статусы для {len(selected)} заданий?", "Подтверждение", wx.YES_NO | wx.ICON_QUESTION
        )
        if confirm.ShowModal() != wx.ID_YES:
            return

        # Удаляем выбранные задания из словаря статусов
        for task in selected:
            if task in self.task_status:
                del self.task_status[task]
                # Обновляем дерево заданий в родительском окне.
                # Возвращаем задаче иконку по умолчанию
                default_icon_task = lst_task_type[task + ".py"] if task + ".py" in lst_task_type else None
                print(9000, default_icon_task)
                self.top_parent.task_tree.set_default_task_icon(task, icon_type=default_icon_task)

        # Обновляем список с задачами после очистки статуса
        self.refresh_list()
        wx.MessageBox(f"Сброшено статусов: {len(selected)}", "Успех")
