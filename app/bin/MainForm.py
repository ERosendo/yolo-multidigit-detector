import kivy

kivy.require("1.9.0")

from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Line
from kivy.graphics import Color, InstructionGroup
from kivy.core.window import Window
from detect import Detector
from PIL import Image


class CalcGridLayout(GridLayout):
    filePath = StringProperty('')
    weights = r'weights\best-100.pt'
    grafic_list = []
    label_list = []
    weights_description = [
        'Red entrenada 100 ciclos con dataset SVHN',
        'Red entrenada 1000 ciclos con dataset SVHN',
        'Red entrenada 1000 ciclos con dataset UNO Cards',
        "Red entrenada 1000 ciclos con dataset SVHN con datos incrementados"
    ]

    def __init__(self, **kwargs):
        super(CalcGridLayout, self).__init__(**kwargs)
        Window.bind(on_dropfile=self._on_file_drop)
        self.detector = Detector(self.weights, self.filePath)
        self.ids.model_label.text = self.weights_description[0]

    def reduced_image(self):
        pass

    def _on_file_drop(self, window, file_path):
        self.reset_canvas()
        self.filePath = file_path.decode("utf-8")
        self.ids.img.source = self.filePath
        self.ids.img.reload()
        self.ids.message_label.text = ' '
        self.ids.start.visible = True
        self.detector.change_source(self.filePath)

    def change_weight(self, value):
        self.ids.model_label.text = self.weights_description[value]
        if value == 0:
            self.weights = 'weights/best-100.pt'
        if value == 1:
            self.weights = 'weights/best-1000.pt'
        if value == 2:
            self.weights = 'weights/uno.pt'
        if value == 3:
            self.weights = 'weights/best-fused.pt'

        self.detector.change_weights(self.weights)

    def start_detection(self):
        self.reset_canvas()
        self.coordinates = self.detector.detect()
        self.draw_rectangle(self.coordinates)

    def reset_canvas(self):
        for item in self.grafic_list:
            self.canvas.remove(item)

        for item in self.label_list:
            self.ids.float_canvas.remove_widget(item)

        for item in self.canvas.children:
            if 'Line' in repr(item):
                self.canvas.remove(item)

    def draw_rectangle(self, coordinates):
        print(coordinates)
        full_size_x = self.ids.img.size[0]
        full_size_y = self.ids.img.size[1]
        center = (full_size_x / 2, full_size_y / 2)
        image = Image.open(self.filePath)
        image_width = int(image.size[0])
        image_height = int(image.size[1])
        for coordinate in coordinates:
            rectangle_size_x = coordinate['bottom_right'][0] - coordinate['top_left'][0]
            rectangle_size_y = coordinate['bottom_right'][1] - coordinate['top_left'][1]

            relative_x_position = (center[0] - image_width / 2 + coordinate['top_left'][0])
            relative_y_position = (center[1] + image_height / 2 - coordinate['top_left'][1]-rectangle_size_y)

            with self.canvas:
                self.obj = InstructionGroup()
                self.obj.add(Color(0, 1, 0, 0.3, mode="rgba"))
                self.obj.add(Line(rectangle=(relative_x_position,
                                                relative_y_position,
                                                rectangle_size_x,
                                                rectangle_size_y),
                                             width=3))
                self.grafic_list.append(self.obj)


            label_position_x = relative_x_position - center[0] + rectangle_size_x / 2
            label_position_y = relative_y_position - center[1] + rectangle_size_y * 1.2

            label = Label(text=coordinate['label'],
                          pos_hint={'x': label_position_x / full_size_x,
                                    'y': label_position_y / full_size_y},
                          size=(self.ids.float_canvas.size[0], self.ids.float_canvas.size[1]),
                          size_hint=(None, None),
                          bold=True,
                          outline_color=[1, 0, 0, 0.5],
                          outline_width=2
                          )
            self.ids.float_canvas.add_widget(label)
            self.label_list.append(label)
