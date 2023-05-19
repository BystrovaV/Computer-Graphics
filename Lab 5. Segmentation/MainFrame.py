from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Segmentation import Segmentation
from KirusBack import KirusBack


class MainFrame:
    def __init__(self):
        self.kirus_back = KirusBack("Кирус-Бек 1")
        self.koen = Segmentation("Сазерленд-Коен 1")
        self.root_frame = Frame()

        self.val_koen = ["Сазерленд-Коен 1", "Сазерленд-Коен 2"]
        self.val_kirus = ["Кирус-Бек 1", "Кирус-Бек 2"]

        figure = Figure(figsize=(8, 7), dpi=100)
        self.plot = figure.add_subplot(111)
        self.config_plot("Отсечение отрезков")

        self.canvas = FigureCanvasTkAgg(figure, master=self.root_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)

        right_panel = Frame(master=self.root_frame)
        right_panel.pack(side=RIGHT)

        self.filename = StringVar(value=self.val_koen[0])

        radio_buttons = []
        for i in range(len(self.val_koen)):
            radio_buttons.append(Radiobutton(right_panel, text=self.val_koen[i],
                                             value=self.val_koen[i],
                                             variable=self.filename))
            radio_buttons[i].grid(row=i, column=0, columnspan=2)

        row = len(self.val_koen)
        for i in range(len(self.val_kirus)):
            radio_buttons.append(Radiobutton(right_panel, text=self.val_kirus[i],
                                             value=self.val_kirus[i],
                                             variable=self.filename))
            radio_buttons[row + i].grid(row=row + i, column=0, columnspan=2)

        row += len(self.val_kirus)
        # create_line_button = Button(right_panel, text="Koen", command=self.segmentation)
        # create_line_button.grid(row=row, column=0, columnspan=2)

        create_line_button = Button(right_panel, text="Segmentation", command=self.segmentation)
        create_line_button.grid(row=row + 1, column=0, columnspan=2)

    def draw_borders(self, b):
        # b = self.borders
        # print(b)
        self.plot.plot([b[1], b[0]], [b[3], b[3]], color='blue')
        self.plot.plot([b[1], b[1]], [b[3], b[2]], color='blue')
        self.plot.plot([b[0], b[0]], [b[3], b[2]], color='blue')
        self.plot.plot([b[0], b[1]], [b[2], b[2]], color='blue')

        self.canvas.draw()

    def segmentation(self):
        filename = self.filename.get()
        try:
            self.val_kirus.index(filename)
            self.kirus_back = KirusBack(filename)
            self.execute_kirus_beck()
        except ValueError:
            self.koen = Segmentation(filename)
            self.execute_koen()

    def execute_koen(self):
        self.config_plot("Алгоритм Сазерленда-Коэна")
        self.draw_borders(self.koen.get_borders())

        result = self.koen.execute()
        for line in self.koen.segments:
            # ans = segm.koen(line[0], line[1], line[2], line[3])
            self.plot.plot([line[0], line[2]], [line[1], line[3]], color='black')

        for ans in result:
            self.plot.plot([ans[0], ans[2]], [ans[1], ans[3]], color='red')

        self.canvas.draw()

    def execute_kirus_beck(self):
        self.config_plot("Алгоритм Кируса-Бека")
        result = self.kirus_back.execute()
        polygon = self.kirus_back.polygon
        segments = self.kirus_back.segments

        for i in range(len(polygon)):
            edge_start = polygon[i]
            edge_end = polygon[(i + 1) % len(polygon)]

            self.plot.plot([edge_start.x, edge_end.x], [edge_start.y, edge_end.y], color='blue')

        for i in segments:
            self.plot.plot([i[0], i[2]], [i[1], i[3]], color='black')

        for i in result:
            self.plot.plot([i[0], i[2]], [i[1], i[3]], color='red')

        self.canvas.draw()

    def config_plot(self, title):
        self.plot.clear()
        self.plot.grid()

        self.plot.set_xlabel("x")
        self.plot.set_ylabel("y")
        self.plot.set_title(title)