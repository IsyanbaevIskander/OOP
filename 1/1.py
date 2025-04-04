from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
import sys

colors = {'Красный': QtGui.QColor(255, 0, 0), 'Зелёный': QtGui.QColor(0, 255, 0), 'Синий': QtGui.QColor(0, 0, 255)}


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.menu = QtWidgets.QMenuBar()
        self.close_menu = self.menu.addAction('Close')
        self.close_menu.setCheckable(True)
        self.close_menu.changed.connect(exit)
        self.menu.addMenu('Nothing')

        self.gps_label = QtWidgets.QLabel('0, 0')
        self.size_label = QtWidgets.QLabel('')

        self.init_first_block()
        self.init_second_block()
        
        self.tab = QtWidgets.QTabWidget()
        self.tab.addTab(self.frame1, 'Основа')
        self.tab.addTab(self.frame2, 'Рисование')

        self.main_layout.addWidget(self.menu)
        self.main_layout.addWidget(self.gps_label)
        self.main_layout.addWidget(self.size_label)
        self.main_layout.addWidget(self.tab)
        self.setLayout(self.main_layout)

    def init_first_block(self):
        self.frame1 = QtWidgets.QFrame()
        self.layout1 = QtWidgets.QVBoxLayout()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.init_checkbox()
        self.init_emoji()
        self.init_slider()
        self.init_progressbar()
        self.init_text_block()
        self.init_exit_button()
        self.frame1.setLayout(self.layout1)

    def init_second_block(self):
        self.frame2 = QtWidgets.QFrame()
        self.layout2 = QtWidgets.QVBoxLayout()

        self.figure_text = QtWidgets.QLabel('Выбрать фигуру')
        self.figure_box = QtWidgets.QComboBox()
        self.figure_layout = QtWidgets.QVBoxLayout()
        self.figure_box.addItems(['Круг', 'Прямоугольник'])
        self.figure_group = QtWidgets.QGroupBox('Выбор фигуры')
        self.figure_layout.addWidget(self.figure_text)
        self.figure_layout.addWidget(self.figure_box)
        self.figure_group.setLayout(self.figure_layout)

        self.color_group = QtWidgets.QGroupBox('Выбор цвета')
        self.color_layout = QtWidgets.QVBoxLayout()
        self.color_text = QtWidgets.QLabel('Выбрать цвет')
        self.color_box = QtWidgets.QComboBox()
        self.color_box.addItems(['Красный', 'Синий', 'Зелёный'])
        self.color_layout.addWidget(self.color_text)
        self.color_layout.addWidget(self.color_box)
        self.color_group.setLayout(self.color_layout)

        self.paint_button = QtWidgets.QPushButton('Нарисовать')
        self.paint_button.setCheckable(True)
        self.paint_button.clicked.connect(self.open_paint)

        self.layout2.addWidget(self.figure_group)
        self.layout2.addWidget(self.color_group)
        self.layout2.addWidget(self.paint_button)
        self.frame2.setLayout(self.layout2)

    def exit(self):
        sys.exit(app.exec())

    def init_checkbox(self):
        # чекбокс, меняющий название
        self.title_checkbox = QtWidgets.QCheckBox('Показывать название')
        self.title_checkbox.stateChanged.connect(self.change_title)
        self.title_checkbox.toggle()
        self.layout1.addWidget(self.title_checkbox)

    def change_title(self):
        if self.title_checkbox.isChecked():
            self.setWindowTitle('Useless GUI')
        else:
            self.setWindowTitle(' ')

    def init_emoji(self):
        self.emoji_group = QtWidgets.QGroupBox('Emoji')
        self.emoji_text = QtWidgets.QLabel('Выбери свою эмоцию)')
        self.emoji_text.setStyleSheet('font-size: 20px')
        # кнопки для эмодзи
        self.angry_button = QtWidgets.QRadioButton('Злой')
        self.angry_button.toggle()
        self.angry_button.toggled.connect(self.change_emoji)

        self.sad_button = QtWidgets.QRadioButton('Грустный')
        self.sad_button.toggled.connect(self.change_emoji)

        self.happy_button = QtWidgets.QRadioButton('Весёлый')
        self.happy_button.toggled.connect(self.change_emoji)

        self.emoji_layout1 = QtWidgets.QVBoxLayout()
        self.emoji_layout1.addWidget(self.emoji_text)
        self.emoji_layout1.addWidget(self.angry_button)
        self.emoji_layout1.addWidget(self.sad_button)
        self.emoji_layout1.addWidget(self.happy_button)

        # картинки эмоджи
        self.angry_emoji = QtGui.QPixmap('angry.png')
        self.sad_emoji = QtGui.QPixmap('sad.jpg')
        self.happy_emoji = QtGui.QPixmap('happy.jpg')

        self.emoji_label = QtWidgets.QLabel()
        self.emoji_label.setPixmap(self.angry_emoji)

        self.emoji_layout2 = QtWidgets.QHBoxLayout()
        self.emoji_layout2.addLayout(self.emoji_layout1)
        self.emoji_layout2.addWidget(self.emoji_label)
        self.emoji_group.setLayout(self.emoji_layout2)

        self.layout1.addWidget(self.emoji_group)

    def change_emoji(self):
        if self.angry_button.isChecked():
            self.emoji_label.setPixmap(self.angry_emoji)
        if self.sad_button.isChecked():
            self.emoji_label.setPixmap(self.sad_emoji)
        if self.happy_button.isChecked():
            self.emoji_label.setPixmap(self.happy_emoji)

    def init_text_block(self):
        # отображение написанного пользователем текста
        self.text_group = QtWidgets.QGroupBox('Повторюшка-хрюшка')
        self.text_layout = QtWidgets.QVBoxLayout()

        self.text_label = QtWidgets.QLabel()
        self.text_label.setMaximumWidth(535)
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setMaxLength(60)
        self.line_edit.setMaximumWidth(535)
        self.line_edit.textChanged[str].connect(self.text_editing)
        self.text_layout.addWidget(self.line_edit)
        self.text_layout.addWidget(self.text_label)
        self.text_group.setLayout(self.text_layout)
        self.layout1.addWidget(self.text_group)

    def text_editing(self, text):
        self.text_label.setText(text)

    def init_slider(self):
        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.slider.setMinimum(600)
        self.slider.setMaximum(800)
        self.slider.sliderMoved.connect(self.change_size)
        self.layout1.addWidget(self.slider)

    def change_size(self, value):
        self.resize(value, 600)
        self.text_label.setMaximumWidth(value - 65)
        self.line_edit.setMaximumWidth(value - 65)

    def init_progressbar(self):
        self.progress_group = QtWidgets.QGroupBox()

        self.progressbar = QtWidgets.QProgressBar()
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(10)

        self.timer = QtCore.QBasicTimer()
        self.count = 0

        self.progress_button = QtWidgets.QPushButton('Старт')
        self.progress_button.setCheckable(True)
        self.progress_button.clicked.connect(self.progress_func)

        self.restart_button = QtWidgets.QPushButton('Сброс')
        self.restart_button.setCheckable(True)
        self.restart_button.clicked.connect(self.restart_timer)
        self.restart_button.setStyleSheet('background-color: black; color: white;')

        self.progress_layout = QtWidgets.QHBoxLayout()
        self.progress_layout.addWidget(self.progressbar)
        self.progress_layout.addWidget(self.progress_button)
        self.progress_layout.addWidget(self.restart_button)
        self.layout1.addLayout(self.progress_layout)

    def progress_func(self):
        self.progress_button.toggle()
        if self.timer.isActive():
            self.timer.stop()
            self.progress_button.setText('Продолжить')
        else:
            if self.progress_button.text() != 'Завершено':
                self.timer.start(1000, self)
                self.progress_button.setText('Стоп')

    def timerEvent(self, a):
        if self.count >= 10:
            self.progress_button.setText('Завершено')
            self.progress_button.setCheckable(False)
            self.timer.stop()
            return
        self.count += 1
        self.progressbar.setValue(self.count)

    def restart_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        self.restart_button.toggle()
        self.count = 0
        self.progress_button.setText('Старт')
        self.progress_button.setCheckable(True)
        self.progressbar.reset()

    def init_exit_button(self):
        # кнопка для выхода из приложения
        self.exit_button = QtWidgets.QPushButton('Закрыть')
        self.exit_button.setCheckable(True)
        self.exit_button.clicked.connect(self.exit_func)
        self.layout1.addWidget(self.exit_button)

    def exit_func(self):
        self.exit_button.toggle()
        self.close_window = ApprovalWindow()

    def open_paint(self):
        self.paint_button.toggle()
        figure = self.figure_box.currentText()
        color = self.color_box.currentText()
        self.window = PaintWidget(color, figure)

    def mouseMoveEvent(self, event, /):
        p = event
        self.gps_label.setText(f'{p.x()}, {p.y()}')

    def mousePressEvent(self, event, /):
        if event.button() == Qt.RightButton:
            self.exit_func()

    def keyPressEvent(self, event, /):
        self.line_edit.setText(self.line_edit.text() + event.text())

    def resizeEvent(self, event, /):
        self.size_label.setText(f'{self.width()}, {self.height()}' )


class ApprovalWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ApprovalWindow, self).__init__()
        self.setWindowTitle('Выход')
        self.setFixedSize(self.sizeHint())
        self.saveGeometry()

        self.widget = QtWidgets.QWidget()
        self.layout1 = QtWidgets.QVBoxLayout()
        self.layout2 = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel('Вы точно хотите выйти из приложения?')
        self.button_yes = QtWidgets.QPushButton('Да')
        self.button_yes.setCheckable(True)
        self.button_yes.clicked.connect(self.all_exit)
        self.button_no = QtWidgets.QPushButton('Нет')
        self.button_no.setCheckable(True)
        self.button_no.clicked.connect(self.dialog_exit)

        self.layout2.addWidget(self.button_yes)
        self.layout2.addWidget(self.button_no)

        self.layout1.addWidget(self.label)
        self.layout1.addLayout(self.layout2)
        self.setLayout(self.layout1)
        self.show()

    def all_exit(self):
        self.button_yes.toggle()
        sys.exit(app.exec())

    def dialog_exit(self):
        self.button_no.toggle()
        self.close()


class PaintWidget(QtWidgets.QWidget):
    def __init__(self, color, figure):
        super().__init__()
        self.setWindowTitle('Paint')
        self.resize(300, 300)
        self.color = color
        self.figure = figure
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setBrush(colors[self.color])
        if self.figure == 'Прямоугольник':
            painter.drawRect(100, 100, 100, 70)
        elif self.figure == 'Круг':
            painter.drawEllipse(100, 100, 100, 100)
        painter.end()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    widget = Window()
    widget.setWindowTitle('Useless GUI')
    widget.resize(600, 600)
    widget.show()
    sys.exit(app.exec())
