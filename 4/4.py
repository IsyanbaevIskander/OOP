from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
import sys


class Shape:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._is_selected = False
        self.color = QtGui.QColor(255, 255, 255)

    def get_status(self):
        return self._is_selected

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def set_status(self, flag):
        self._is_selected = flag

    def draw(self, painter):
        pass

    def highlight_checking(self, x, y, pressed):
        if not pressed:
            self._is_selected = False
        if self.in_area(x, y):
            self._is_selected = True
            return True

    def in_area(self, x, y):
        pass

    def set_brush_settings(self, painter):
        painter.setBrush(self.color)

        if self._is_selected:
            pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
            pen.setStyle(QtCore.Qt.DashLine)
            pen.setWidth(2)
        else:
            pen = QtGui.QPen(QtGui.QColor(0, 0, 0))

        painter.setPen(pen)

    def _borders(self, half_width, half_height):
        width = window.drawing_widget.width()
        height = window.drawing_widget.height()
        if half_width * 2 >= width or half_height * 2 >= height:
            if width > height:
                self._y = height / 2
            else:
                self._x = width / 2
        else:
            if self._x - half_width <= 0:
                self._x = half_width
            if self._x + half_width > width:
                self._x = width - half_width

            if self._y - half_height <= 0:
                self._y = half_height
            if self._y + half_height > height:
                self._y = height - half_height

    def _increase(self):
        pass

    def _reduce(self):
        pass


class CCircle(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._radius = 25

    def draw(self, painter):
        self._borders(self._radius, self._radius)
        self.set_brush_settings(painter)
        x = self._x - self._radius
        y = self._y - self._radius
        painter.drawEllipse(x, y, self._radius * 2, self._radius * 2)

    def in_area(self, x, y):
        if ((self._x - x) ** 2 + (self._y - y) ** 2) <= self._radius ** 2:
            return True

    def _increase(self):
        width = window.drawing_widget.width()
        height = window.drawing_widget.height()
        if self._radius >= width or self._radius >= width:
            self._radius = min(width, height)
        else:
            self._radius += 1

    def _reduce(self):
        if self._radius <= 5:
            return
        self._radius -= 1


class Ellipse(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._width_radius = 50
        self._height_radius = 25

    def draw(self, painter):
        self._borders(self._width_radius, self._height_radius)
        self.set_brush_settings(painter)
        x = self._x - self._width_radius
        y = self._y - self._height_radius
        painter.drawEllipse(x, y, self._width_radius * 2, self._height_radius * 2)

    def in_area(self, x, y):
        if (((self._x - x) ** 2) / self._width_radius ** 2 + ((self._y - y) ** 2) / self._height_radius ** 2) <= 1:
            return True


class Square(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._half_width = 25

    def draw(self, painter):
        self._borders(self._half_width, self._half_width)
        self.set_brush_settings(painter)
        x = self._x - self._half_width
        y = self._y - self._half_width
        painter.drawRect(x, y, self._half_width * 2, self._half_width * 2)

    def in_area(self, x, y):
        if abs(self._x - x) <= self._half_width and abs(self._y - y) <= self._half_width:
            return True


class Rectangle(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._half_width = 50
        self._half_height = 25

    def draw(self, painter):
        self._borders(self._half_width, self._half_height)
        self.set_brush_settings(painter)
        x = self._x - self._half_width
        y = self._y - self._half_height
        painter.drawRect(x, y, self._half_width * 2, self._half_height * 2)

    def in_area(self, x, y):
        if abs(self._x - x) <= self._half_width and abs(self._y - y) <= self._half_height:
            return True


class Triangle(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._half_width = 25

    def draw(self, painter):
        self._borders(self._half_width, self._half_width)
        self.set_brush_settings(painter)

        painter.drawPolygon([QtCore.QPoint(self._x, self._y - self._half_width),
                             QtCore.QPoint(self._x - self._half_width, self._y + self._half_width),
                             QtCore.QPoint(self._x + self._half_width, self._y + self._half_width)])

    def in_area(self, x, y):
        a = [self._x - self._half_width, self._y + self._half_width]
        b = [self._x, self._y - self._half_width]
        c = [self._x + self._half_width, self._y + self._half_width]
        point = [x, y]
        square = self.square(a, b, c)
        first_square = self.square(point, a, b)
        second_square = self.square(point, b, c)
        third_square = self.square(point, a, c)
        return abs(square - first_square - second_square - third_square) == 0

    def square(self, a, b, c):
        return abs(a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1])) / 2.0


class Container:
    def __init__(self):
        self.__circles = []
        self.__size = 0

    def __iter__(self):
        return iter(self.__circles)

    def add(self, circle):
        self.__circles.append(circle)
        self.__size += 1

    def pop(self, index):
        self.__circles.pop(index)
        self.__size -= 1

    def clear(self):
        self.__circles.clear()
        self.__size = 0

    def index(self, object):
        return self.__circles.index(object)

    def size(self):
        return self.__size


class PaintWindow(QtWidgets.QWidget):
    def __init__(self, container):
        super().__init__()
        self.container = container
        self.setFocusPolicy(Qt.StrongFocus)
        self._selected_shape = CCircle

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        for i in self.container:
            i.draw(painter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            flag = False
            for i in self.container:
                if i.in_area(event.x(), event.y()):
                    flag = True
            if not flag:
                self.highlight(event.x(), event.y(), False)
                self.container.add(self._selected_shape(event.x(), event.y()))
            else:
                ctrl_pressed = event.modifiers() and Qt.ControlModifier
                self.highlight(event.x(), event.y(), ctrl_pressed)
        self.update()

    def highlight(self, x, y, pressed):
        for i in self.container:
            i.highlight_checking(x, y, pressed)

    def keyPressEvent(self, event):
        print(event.key())
        if event.matches(QtGui.QKeySequence.SelectAll):
            self.select_all()
        if event.key() == Qt.Key_Delete:
            self.delete_selected()

        if event.key() == Qt.Key_Equal:
            for curr in self.container:
                if curr.get_status():
                    pass
        if event.key() == Qt.Key_Minus:
            ...

        if event.key() == Qt.Key_Right:
            for curr in self.container:
                if curr.get_status():
                    curr.set_x(curr.get_x() + 1)
        if event.key() == Qt.Key_Left:
            for curr in self.container:
                if curr.get_status():
                    curr.set_x(curr.get_x() - 1)

        if event.key() == Qt.Key_Up:
            for curr in self.container:
                if curr.get_status():
                    curr.set_y(curr.get_y() - 1)

        if event.key() == Qt.Key_Down:
            for curr in self.container:
                if curr.get_status():
                    curr.set_y(curr.get_y() + 1)

        self.update()

    def select_all(self):
        for i in self.container:
            i.set_status(True)

    def delete_selected(self):
        selected = []
        for i in self.container:
            if i.get_status():
                selected.append(self.container.index(i))
        for i in range(len(selected) - 1, -1, -1):
            self.container.pop(selected[i])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circle Drawer")
        self.setGeometry(100, 100, 600, 400)

        self.container = Container()

        self.create_button_row()
        self.drawing_widget = PaintWindow(self.container)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.drawing_widget)
        self.central = QtWidgets.QWidget()
        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)

    def create_button_row(self):
        # Создает горизонтальный ряд кнопок для выбора фигуры
        self.button_layout = QtWidgets.QHBoxLayout()

        # Создаем кнопки для каждой фигуры
        self.buttons = {}  # Словарь для хранения кнопок
        for shape in shapes.keys():
            button = QtWidgets.QPushButton(shape, self)
            self.button_layout.addWidget(button)
            self.buttons[shape] = button
            print(self.buttons[shape].text())
            button.clicked.connect(lambda checked, s=shape: self.set_shape(self.buttons[s]))
            if shape == "Круг":
                button.setStyleSheet("background-color: lightblue; font-weight: bold;")

        self.color_button = QtWidgets.QPushButton("Изменить цвет", self)
        self.color_button.clicked.connect(self.change_color)
        self.button_layout.addWidget(self.color_button)

    def change_color(self):
        flag = False
        for curr in self.container:
            if curr.get_status():
                flag = True
        if not flag:
            return

        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            for curr in self.container:
                if curr.get_status():
                    curr.set_color(color)
            self.update()

    def set_shape(self, selected_button):
        print(selected_button.text())
        # Устанавливает выбранную фигуру и обновляет внешний вид кнопок
        for curr in self.buttons.keys():
            if curr == selected_button.text():
                self.buttons[curr].setStyleSheet("background-color: lightblue; font-weight: bold;")
                continue
            self.buttons[curr].setStyleSheet("")

        self.drawing_widget._selected_shape = shapes[selected_button.text()]


shapes = {"Круг": CCircle, "Эллипс": Ellipse, "Квадрат": Square,
          "Прямоугольник": Rectangle, "Треугольник": Triangle}

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
