# Окно статистики, прогресс решенных задач
import gettext
import math

import wx

from config import IMAGES_PATH, JSON_COMPLETED_TASKS
from task_tree.task_structure import lst_task_type
from utils.func_utils import read_json_file

_ = gettext.gettext


###########################################################################
## Class StatisticsDialog
###########################################################################
class StatisticsDialog(wx.Dialog):
    """Класс окна статистики с диаграммой прогресса"""

    def __init__(self, parent):
        wx.Dialog.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=_(u"Ваш прогресс"),
            pos=wx.DefaultPosition,
            size=wx.Size(400, 500),
            style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL,
        )
        self.SetSizeHints(wx.Size(400, 500), wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))

        # Устанавливаем иконку (как в ClearStatusTask)
        icon = wx.Icon(str(IMAGES_PATH / "baby.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Данные
        self.total_tasks = len(lst_task_type)
        # Считываем словарь решённых заданий
        self.solved_tasks = len(self.GetParent().task_tree.task_status) # len(read_json_file(JSON_COMPLETED_TASKS))
        print("Родитель окна статистики", self.GetParent())
        self.progress = (self.solved_tasks / self.total_tasks) * 100 if self.total_tasks > 0 else 0

        # Цвета
        self.text_color = wx.Colour(70, 70, 70)
        self.highlight_color = wx.Colour(30, 30, 30)
        self.solved_color = wx.Colour(76, 175, 80)
        self.remaining_color = wx.Colour(239, 83, 80)

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Заголовок
        title = wx.StaticText(panel, label="Статистика выполнения задач")
        title.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour(self.highlight_color)
        vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        # Статистика
        stats_grid = self.create_stats_grid(panel)
        vbox.Add(stats_grid, 0, wx.EXPAND | wx.ALL, 15)

        # Диаграмма
        vbox.Add(wx.StaticText(panel, label="Визуализация прогресса:"), 0, wx.LEFT | wx.TOP, 15)
        pie_chart = self.create_pie_chart(panel)
        vbox.Add(pie_chart, 1, wx.EXPAND | wx.ALL, 10)

        # Легенда
        legend = self.create_legend(panel)
        vbox.Add(legend, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        panel.SetSizer(vbox)
        self.Layout()
        self.Centre(wx.BOTH)

    def create_stats_grid(self, parent):
        """Создает сетку с показателями статистики"""
        grid = wx.FlexGridSizer(3, 2, 10, 15)
        grid.AddGrowableCol(1, 1)

        self.add_stat_row(parent, grid, "Всего задач:", f"{self.total_tasks}", self.text_color)
        self.add_stat_row(parent, grid, "Решено задач:", f"{self.solved_tasks}", self.text_color)
        self.add_stat_row(parent, grid, "Прогресс:", f"{self.progress:.1f}%", self.highlight_color)

        return grid

    def add_stat_row(self, parent, sizer, label, value, color):
        """Добавляет строку статистики"""
        lbl = wx.StaticText(parent, label=label)
        lbl.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        lbl.SetForegroundColour(wx.Colour(100, 100, 100))

        val = wx.StaticText(parent, label=value)
        val.SetForegroundColour(color)
        val.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        sizer.Add(lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        sizer.Add(val, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)

    def create_pie_chart(self, parent):
        """Создает панель с круговой диаграммой"""
        panel = wx.Panel(parent, size=(300, 300))
        panel.Bind(wx.EVT_PAINT, self.on_paint_chart)
        return panel

    def create_legend(self, parent):
        """Создает панель с легендой"""
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        items = [(self.solved_color, "Решено"), (self.remaining_color, "Осталось")]

        for color, label in items:
            color_box = wx.Panel(panel, size=(20, 15))
            color_box.SetBackgroundColour(color)
            sizer.Add(color_box, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)

            text = wx.StaticText(panel, label=label)
            text.SetForegroundColour(self.text_color)
            sizer.Add(text, 0, wx.ALIGN_CENTER | wx.RIGHT, 15)

        panel.SetSizer(sizer)
        return panel

    def on_paint_chart(self, event):
        """Отрисовка круговой диаграммы"""
        dc = wx.PaintDC(event.GetEventObject())
        gc = wx.GraphicsContext.Create(dc)
        if not gc:
            return

        width, height = event.GetEventObject().GetClientSize()
        diameter = min(width, height) * 0.8
        radius = diameter / 2
        center_x, center_y = width // 2, height // 2

        # Очистка фона
        gc.SetBrush(wx.Brush(wx.Colour(250, 250, 250)))
        gc.DrawRectangle(0, 0, width, height)

        if self.total_tasks == 0:
            gc.SetFont(
                wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD), wx.Colour(50, 50, 50)
            )
            gc.DrawText("Нет данных", center_x - 30, center_y - 10)
            return

        # Отрисовка секторов
        solved_angle = (self.solved_tasks / self.total_tasks) * 2 * math.pi
        self.draw_sector(gc, center_x, center_y, radius, 0, solved_angle, self.solved_color)

        if self.total_tasks > self.solved_tasks:
            self.draw_sector(gc, center_x, center_y, radius, solved_angle, 2 * math.pi, self.remaining_color)

        # Текст в центре
        gc.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD), wx.Colour(50, 50, 50))
        text = f"{self.progress:.1f}%"
        text_width, _ = gc.GetTextExtent(text)
        gc.DrawText(text, center_x - text_width / 2, center_y - 10)

    def draw_sector(self, gc, cx, cy, radius, start_angle, end_angle, color):
        """Рисует сектор диаграммы"""
        path = gc.CreatePath()
        path.MoveToPoint(cx, cy)
        path.AddArc(cx, cy, radius, start_angle, end_angle, True)
        path.CloseSubpath()
        gc.SetBrush(wx.Brush(color))
        gc.SetPen(wx.Pen(wx.Colour(120, 120, 120), 1))
        gc.FillPath(path)
        gc.StrokePath(path)
