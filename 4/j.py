from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QColorDialog
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QColor, QPainter, QAction


class Shape:
    def __init__(self, rect: QRect, color: QColor):
        self.rect = rect
        self.color = color
        self.selected = False
        self.resize_handle_size = 8  # Размер маркера для изменения размера

    def draw(self, painter: QPainter):
        painter.setBrush(self.color)
        if self.selected:
            painter.setPen(QColor(255, 0, 0))
            self.draw_resize_handles(painter)
        else:
            painter.setPen(QColor(0, 0, 0))
        self.draw_shape(painter)

    def draw_shape(self, painter: QPainter):
        # Этот метод будет переопределен в дочерних классах
        pass

    def draw_resize_handles(self, painter: QPainter):
        # Рисуем маркеры для изменения размера
        rect = self.rect
        handle_size = self.resize_handle_size
        handles = [
            QRect(rect.left() - handle_size // 2, rect.top() - handle_size // 2, handle_size, handle_size),
            # Левый верхний
            QRect(rect.right() - handle_size // 2, rect.top() - handle_size // 2, handle_size, handle_size),
            # Правый верхний
            QRect(rect.left() - handle_size // 2, rect.bottom() - handle_size // 2, handle_size, handle_size),
            # Левый нижний
            QRect(rect.right() - handle_size // 2, rect.bottom() - handle_size // 2, handle_size, handle_size),
            # Правый нижний
        ]
        painter.setBrush(QColor(255, 0, 0))
        for handle in handles:
            painter.drawRect(handle)

    def contains(self, point: QPoint) -> bool:
        return self.rect.contains(point)

    def move(self, dx: int, dy: int):
        self.rect.translate(dx, dy)

    def resize(self, width: int, height: int):
        self.rect.setWidth(width)
        self.rect.setHeight(height)

    def set_color(self, color: QColor):
        self.color = color

    def set_selected(self, selected: bool):
        self.selected = selected

    def is_resize_handle_hovered(self, point: QPoint) -> int:
        # Проверяем, находится ли курсор на одном из маркеров изменения размера
        rect = self.rect
        handle_size = self.resize_handle_size
        handles = [
            (QRect(rect.left() - handle_size // 2, rect.top() - handle_size // 2, handle_size, handle_size), 1),
            # Левый верхний
            (QRect(rect.right() - handle_size // 2, rect.top() - handle_size // 2, handle_size, handle_size), 2),
            # Правый верхний
            (QRect(rect.left() - handle_size // 2, rect.bottom() - handle_size // 2, handle_size, handle_size), 3),
            # Левый нижний
            (QRect(rect.right() - handle_size // 2, rect.bottom() - handle_size // 2, handle_size, handle_size), 4),
            # Правый нижний
        ]
        for handle, handle_id in handles:
            if handle.contains(point):
                return handle_id
        return 0

    def resize_by_mouse(self, handle_id: int, dx: int, dy: int):
        # Изменение размера в зависимости от выбранного маркера
        if handle_id == 1:  # Левый верхний
            self.rect.setLeft(self.rect.left() + dx)
            self.rect.setTop(self.rect.top() + dy)
        elif handle_id == 2:  # Правый верхний
            self.rect.setRight(self.rect.right() + dx)
            self.rect.setTop(self.rect.top() + dy)
        elif handle_id == 3:  # Левый нижний
            self.rect.setLeft(self.rect.left() + dx)
            self.rect.setBottom(self.rect.bottom() + dy)
        elif handle_id == 4:  # Правый нижний
            self.rect.setRight(self.rect.right() + dx)
            self.rect.setBottom(self.rect.bottom() + dy)


class Circle(Shape):
    def draw_shape(self, painter: QPainter):
        painter.drawEllipse(self.rect)


class Rectangle(Shape):
    def draw_shape(self, painter: QPainter):
        painter.drawRect(self.rect)


class Triangle(Shape):
    def draw_shape(self, painter: QPainter):
        points = [
            QPoint(self.rect.center().x(), self.rect.top()),
            QPoint(self.rect.left(), self.rect.bottom()),
            QPoint(self.rect.right(), self.rect.bottom())
        ]
        painter.drawPolygon(points)


class Ellipse(Shape):
    def draw_shape(self, painter: QPainter):
        painter.drawEllipse(self.rect)


class Line(Shape):
    def draw_shape(self, painter: QPainter):
        painter.drawLine(self.rect.topLeft(), self.rect.bottomRight())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Визуальный редактор")
        self.setGeometry(100, 100, 800, 600)

        self.shapes = []
        self.selected_shapes = []
        self.resize_handle_id = 0  # ID маркера для изменения размера
        self.is_resizing = False  # Флаг для изменения размера

        self.toolbar = QToolBar("Инструменты")
        self.addToolBar(self.toolbar)

        self.add_shape_action("Круг", Circle)
        self.add_shape_action("Прямоугольник", Rectangle)
        self.add_shape_action("Треугольник", Triangle)
        self.add_shape_action("Эллипс", Ellipse)
        self.add_shape_action("Отрезок", Line)

        self.color_action = QAction("Изменить цвет", self)
        self.color_action.triggered.connect(self.change_color)
        self.toolbar.addAction(self.color_action)

        self.delete_action = QAction("Удалить", self)
        self.delete_action.triggered.connect(self.delete_selected)
        self.toolbar.addAction(self.delete_action)

    def add_shape_action(self, name, shape_class):
        action = QAction(name, self)
        action.triggered.connect(lambda: self.add_shape(shape_class))
        self.toolbar.addAction(action)

    def add_shape(self, shape_class):
        rect = QRect(50, 50, 100, 100)
        color = QColor(0, 0, 255)
        shape = shape_class(rect, color)
        self.shapes.append(shape)
        self.update()

    def change_color(self):
        if self.selected_shapes:
            color = QColorDialog.getColor()
            if color.isValid():
                for shape in self.selected_shapes:
                    shape.set_color(color)
                self.update()

    def delete_selected(self):
        for shape in self.selected_shapes:
            self.shapes.remove(shape)
        self.selected_shapes.clear()
        self.update()

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        if event.button() == Qt.LeftButton:
            for shape in self.shapes:
                if shape.selected:
                    handle_id = shape.is_resize_handle_hovered(pos)
                    if handle_id:
                        self.resize_handle_id = handle_id
                        self.is_resizing = True
                        break
                if shape.contains(pos):
                    shape.set_selected(not shape.selected)
                    if shape.selected:
                        self.selected_shapes.append(shape)
                    else:
                        self.selected_shapes.remove(shape)
                    self.update()
                    break

    def mouseMoveEvent(self, event):
        if self.is_resizing and self.selected_shapes:
            dx = event.position().x() - event.oldPos().x()
            dy = event.position().y() - event.oldPos().y()
            for shape in self.selected_shapes:
                shape.resize_by_mouse(self.resize_handle_id, dx, dy)
            self.update()
        elif event.buttons() & Qt.LeftButton and self.selected_shapes:
            dx = event.position().x() - event.oldPos().x()
            dy = event.position().y() - event.oldPos().y()
            for shape in self.selected_shapes:
                shape.move(dx, dy)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_resizing = False
            self.resize_handle_id = 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            for shape in self.selected_shapes:
                shape.move(-10, 0)
        elif event.key() == Qt.Key_Right:
            for shape in self.selected_shapes:
                shape.move(10, 0)
        elif event.key() == Qt.Key_Up:
            for shape in self.selected_shapes:
                shape.move(0, -10)
        elif event.key() == Qt.Key_Down:
            for shape in self.selected_shapes:
                shape.move(0, 10)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for shape in self.shapes:
            shape.draw(painter)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
