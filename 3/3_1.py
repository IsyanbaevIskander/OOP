from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
import sys


class CCircle:
    RADIUS = 25

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__is_selected = False

    def get_status(self):
        return self.__is_selected

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_status(self, flag):
        self.__is_selected = flag

    def draw(self, painter):
        color = QtGui.QColor(0, 0, 255) if self.__is_selected else QtGui.QColor(255, 255, 255)
        painter.setBrush(color)
        x = self.__x - self.RADIUS
        y = self.__y - self.RADIUS
        painter.drawEllipse(x, y, self.RADIUS * 2, self.RADIUS * 2)

    def highlight_checking(self, x, y, pressed):
        if not pressed:
            self.__is_selected = False
        if ((self.__x - x)**2 + (self.__y - y)**2) <= self.RADIUS**2:
            self.__is_selected = True
            return True

    def in_area(self, x, y):
        if ((self.__x - x) ** 2 + (self.__y - y) ** 2) <= self.RADIUS ** 2:
            return True


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
                self.container.add(CCircle(event.x(), event.y()))
            else:
                ctrl_pressed = event.modifiers() and Qt.ControlModifier
                self.highlight(event.x(), event.y(), ctrl_pressed)
        self.update()

    def highlight(self, x, y, pressed):
        for i in self.container:
            i.highlight_checking(x, y, pressed)

    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.SelectAll):
            self.select_all()
        if event.key() == Qt.Key_Delete:
            self.delete_selected()
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
        self.drawing_widget = PaintWindow(self.container)
        self.setCentralWidget(self.drawing_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

    # пример использования контейнера
    # cont = Container()
    # cont.add(3)
    # cont.add(2)
    # cont.add(4)
    # for i in cont:
    #     print(i)
