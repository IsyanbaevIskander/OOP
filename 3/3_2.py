from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from blinker import Signal
import sys


class Numbers(QtCore.QObject):
    signal = Signal()

    def __init__(self, _a, _b, _c):
        super().__init__()
        self.__a = a
        self.__b = b
        self.__c = c

    def set_a(self, value):
        if type(value) is str:
            if value.isdigit():
                value = int(value)
            else:
                return

        if value == self.__a:
            return

        if value >= 100:
            self.__a = 100
            self.__b = 100
            self.__c = 100
            print("A")
            self.signal.send(self.get())
            return

        self.__a = value
        if value > self.__b:
            self.__b = value
            if value > self.__c:
                self.__c = value

        print("A")
        self.signal.send(self.get())

    def set_b(self, value):
        if type(value) is str:
            if value.isdigit():
                value = int(value)
            else:
                return

        if value == self.__b:
            return

        if value < self.__a:
            self.__b = self.__a
        elif value > self.__c:
            self.__b = self.__c
        else:
            self.__b = value
        print("B")
        self.signal.send(self.get())

    def set_c(self, value):
        if type(value) is str:
            if value.isdigit():
                value = int(value)
            else:
                return

        if value == self.__c:
            return

        if value <= 0:
            self.__a = 0
            self.__b = 0
            self.__c = 0
            print("C")
            self.signal.send(self.get())
            return

        if value >= 100:
            self.__c = 100
            print("C")
            self.signal.send(self.get())
            return

        self.__c = value
        if value < self.__b:
            self.__b = value
            if value < self.__a:
                self.__a = value
        print("C")
        self.signal.send(self.get())

    def get(self):
        return self.__a, self.__b, self.__c


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(800, 300)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("A <= B <= C")
        self.label.setStyleSheet("{font-size: 20px}")
        self.label.setFont(QtGui.QFont("Arial", 80))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label)

        # создание Lineedit`ов
        self.first_layout = QtWidgets.QHBoxLayout()
        self.text_a = QtWidgets.QLineEdit()
        self.first_layout.addWidget(self.text_a)
        self.text_b = QtWidgets.QLineEdit()
        self.first_layout.addWidget(self.text_b)
        self.text_c = QtWidgets.QLineEdit()
        self.first_layout.addWidget(self.text_c)

        # создание SpinBox`ов
        self.second_layout = QtWidgets.QHBoxLayout()
        self.spin_a = QtWidgets.QSpinBox()
        self.spin_a.setMinimum(0)
        self.spin_a.setMaximum(100)
        self.second_layout.addWidget(self.spin_a)
        self.spin_b = QtWidgets.QSpinBox()
        self.spin_b.setMinimum(0)
        self.spin_b.setMaximum(100)
        self.second_layout.addWidget(self.spin_b)
        self.spin_c = QtWidgets.QSpinBox()
        self.spin_c.setMinimum(0)
        self.spin_c.setMaximum(100)
        self.second_layout.addWidget(self.spin_c)

        # создание Slider`ов
        self.third_layout = QtWidgets.QHBoxLayout()
        self.flag_a = False
        self.slider_a = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.slider_tuning(self.slider_a)
        self.flag_b = False
        self.slider_b = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.slider_tuning(self.slider_b)
        self.flag_c = False
        self.slider_c = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.slider_tuning(self.slider_c)
        self.is_updating = False

        self.main_layout.addLayout(self.first_layout)
        self.main_layout.addLayout(self.second_layout)
        self.main_layout.addLayout(self.third_layout)
        self.setLayout(self.main_layout)
        self.array = (self.text_a, self.text_b, self.text_c,
                      self.spin_a, self.spin_b, self.spin_c,
                      self.slider_a, self.slider_b, self.slider_c)
        self.connecting()

    def slider_tuning(self, slider):
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setSingleStep(1)
        slider.setPageStep(1)
        self.third_layout.addWidget(slider)

    def connecting(self):
        numbers.signal.connect(self.updating)
        numbers.signal.send(numbers.get())
        self.text_a.editingFinished.connect(lambda: self.check_line_edits(self.text_a, self.spin_a, numbers.set_a))
        self.text_b.editingFinished.connect(lambda: self.check_line_edits(self.text_b, self.spin_b, numbers.set_b))
        self.text_c.editingFinished.connect(lambda: self.check_line_edits(self.text_c, self.spin_c, numbers.set_c))

        self.spin_a.editingFinished.connect(lambda: self.check_spins(self.spin_a, self.text_a, numbers.set_a))
        self.spin_b.editingFinished.connect(lambda: self.check_spins(self.spin_b, self.text_b, numbers.set_b))
        self.spin_c.editingFinished.connect(lambda: self.check_spins(self.spin_c, self.text_c, numbers.set_c))

        self.slider_a.valueChanged.connect(
            lambda: self.check_sliders(self.slider_a, self.spin_a, numbers.set_a, self.flag_a))
        self.slider_a.sliderPressed.connect(lambda: self.slider_pressed(self.slider_a))
        self.slider_a.sliderReleased.connect(lambda: self.slider_released(self.slider_a))

        self.slider_b.valueChanged.connect(
            lambda: self.check_sliders(self.slider_b, self.spin_b, numbers.set_b, self.flag_b))
        self.slider_b.sliderPressed.connect(lambda: self.slider_pressed(self.slider_b))
        self.slider_b.sliderReleased.connect(lambda: self.slider_released(self.slider_b))

        self.slider_c.valueChanged.connect(
            lambda: self.check_sliders(self.slider_c, self.spin_c, numbers.set_c, self.flag_c))
        self.slider_c.sliderPressed.connect(lambda: self.slider_pressed(self.slider_c))
        self.slider_c.sliderReleased.connect(lambda: self.slider_released(self.slider_c))

    def check_line_edits(self, lineedit, spin, method):
        text = lineedit.text()
        if not text.isdigit():
            lineedit.setText(str(spin.value()))
            return

        if lineedit == self.text_b:
            if int(text) < int(self.text_a.text()):
                if spin.value() == self.spin_a.value():
                    self.text_b.setText(str(self.text_a.text()))
                    return

            if int(text) > int(self.text_c.text()):
                if spin.value() == self.spin_c.value():
                    self.text_b.setText(str(self.text_c.text()))
                    return

        method(text)

    def check_spins(self, spin, lineedit, method):
        value = spin.value()

        if lineedit == self.text_b:
            if value < self.spin_a.value():
                if int(lineedit.text()) == int(self.text_a.text()):
                    self.spin_b.setValue(self.spin_a.value())
                    return

            if value > self.spin_c.value():
                if int(lineedit.text()) == int(self.text_c.text()):
                    self.spin_b.setValue(self.spin_c.value())
                    return

        method(value)

    def check_sliders(self, slider, spin, method, flag):
        if self.is_updating:
            return

        if flag:
            return

        value = slider.value()

        if slider == self.slider_b:
            if value < self.slider_a.value():
                if spin.value() == self.spin_a.value():
                    self.slider_b.setValue(self.slider_a.value())
                    return

            if value > self.slider_c.value():
                if spin.value() == self.spin_c.value():
                    self.slider_b.setValue(self.slider_c.value())
                    return

        method(value)

    def slider_pressed(self, slider):
        if slider == self.slider_a:
            self.flag_a = True
            return

        if slider == self.slider_b:
            self.flag_b = True
            return

        if slider == self.slider_c:
            self.flag_c = True
            return

    def slider_released(self, slider):
        if slider == self.slider_a:
            self.flag_a = False
            self.check_sliders(self.slider_a, self.spin_a, numbers.set_a, self.flag_a)
            return

        if slider == self.slider_b:
            self.flag_b = False
            self.check_sliders(self.slider_b, self.spin_b, numbers.set_b, self.flag_b)
            return

        if slider == self.slider_c:
            self.flag_c = False
            self.check_sliders(self.slider_c, self.spin_c, numbers.set_c, self.flag_c)

    def updating(self, nums):
        self.is_updating = True
        self.text_a.setText(str(nums[0]))
        self.text_b.setText(str(nums[1]))
        self.text_c.setText(str(nums[2]))

        self.spin_a.setValue(nums[0])
        self.spin_b.setValue(nums[1])
        self.spin_c.setValue(nums[2])

        self.slider_a.setValue(nums[0])
        self.slider_b.setValue(nums[1])
        self.slider_c.setValue(nums[2])
        self.is_updating = False


def rewrite_file(result):
    with open("numbers.txt", 'w', encoding='utf-8') as file:
        file.write(f'{result[0]}\n{result[1]}\n{result[2]}')


if __name__ == "__main__":
    with open("numbers.txt", 'r', encoding='utf-8') as file:
        a = int(file.readline())
        b = int(file.readline())
        c = int(file.readline())
    numbers = Numbers(a, b, c)
    numbers.signal.connect(rewrite_file)
    app = QtWidgets.QApplication(sys.argv)
    widget = Window()
    widget.setWindowTitle('MVC')
    widget.show()
    sys.exit(app.exec())
