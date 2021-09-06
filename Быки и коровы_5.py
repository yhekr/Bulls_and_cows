# -*- coding: utf-8 -*-


import sys
import random
from PySide2.QtCore import *
from PySide2.QtWidgets import *


def New_choice(x):
    Label_2.close()
    Label_ss2.close()
    Button21.close()
    Button22.close()
    Line2.close()
    Line.close()
    Button1.close()
    Button2.close()
    Button3.close()
    Label.close()
    Label_s.show()
    Button_s1.show()
    Button_s2.show()
    Button_end.close()




def Play_you(x):
    Label_2.show()
    Label_ss2.show()
    Button21.show()
    Button22.show()
    Line2.show()
    Cows = Cow_game()
    Label_s.close()
    Button_s1.close()
    Button_s2.close()
    Button_end.show()
    return Cows


def Play_comp(x):
    Line.show()
    Button1.show()
    Button2.show()
    Button3.show()
    Label.show()    
    Cows = MyCow()
    Label_s.close()
    Button_s1.close()
    Button_s2.close()
    Button_end.show()
    

def checked(x):
    return x.isdigit() and len(x) == 4 and len({x[0], x[1], x[2], x[3]}) == 4 and x[0] != "0"


def how_many(a, b):
    count_b = 0
    count_c = 0
    set1 = set(b)
    for i in range(4):
        if a[i] == b[i]:
            count_b += 1
        elif a[i] in set1:
            count_c += 1
    return str(count_b) + str(count_c)

SET = {"40", "01", "02", "03", "04", "31", "22", "21", "13", "12", "11", "30", "20", "10", "00", "04"}


class Cow_game(QObject):
    label_new = Signal(str)
    value_disappeared = Signal(str)
    disabled = Signal(bool)

    def __init__(self):
        QObject.__init__(self)
        self._set = set()
        for i in range(1, 10):
            for j in range(0, 10):
                for h in range(0, 10):
                    for k in range(0, 10):
                        if checked(str(i) + str(j) + str(h) + str(k)):
                            self._set.add(str(i) + str(j) + str(h) + str(k))
        self._pn = str(1234)
        self._pr = 0
    
    @Slot()
    def prog(self):
        set_1 = set()
        x = ""
        if self._pr in SET:
            if self._pr == "40":
                str1 = "Мы выиграли! Начать снова?"
                self.disabled.emit(False)
            else:
                for elem in self._set:      
                    if how_many(self._pn, str(elem)) == self._pr:
                        set_1.add(elem)
                        x = elem
                self._set = set_1
                self._pn = x
                str1 = "Это " + self._pn + "?"
                self.value_disappeared.emit("")
        else:
            str1 = "Введено неправильное число"
        self.label_new.emit(str1)
        return
    
    def setValue(self, value):
        self._pr = str(value)
        return    
    
    def new_game(self):
        self._set = set()
        for i in range(1, 10):
            for j in range(0, 10):
                for h in range(0, 10):
                    for k in range(0, 10):
                        if checked(str(i) + str(j) + str(h) + str(k)):
                            self._set.add(str(i) + str(j) + str(h) + str(k))
        self._pn = str(1234)
        self._pr = 0
        self.label_new.emit("Попробую угадать. Это 1234?")
        self.disabled.emit(True)
        return


class MyCow(QObject):
    value_changed_str = Signal(str)
    click_button1 = Signal(bool)
    name_changed_str = Signal(str)
    value_disappeared = Signal(str)
    new_value = Signal(list)
    win = Signal(int)
    
    def __init__(self):
        QObject.__init__(self)
        r_n = random.randint(1000, 9900)
        while not checked(str(r_n)):
            r_n = random.randint(1000, 9900)
        self._rn = str(r_n)
        self._pn = ""
        self._set = {self._rn[0], self._rn[1], self._rn[2], self._rn[3]}
        self._oldn = set()
        self._c = 0
        print(self._rn)
        return
        
    @Slot()    
    def setValue(self, value):
        self._pn = str(value)
        return
    
    def equal(self, other):
        self._rn = other[0]
        self._pn = other[1]
        self._set = other[2]
        self._oldn = other[3]
        self._c = other[4]

        return        
    
    
    def how_many(self):
        count_b = 0
        count_c = 0
        if not checked(self._pn):
            str1 = "Введено неправильное число"
        else:
            if self._pn not in self._oldn:
                self._c += 1
                self._oldn.add(self._pn)
            for i in range(4):
                if self._pn[i] == self._rn[i]:
                    count_b += 1
                elif self._pn[i] in self._set:
                    count_c += 1
            if count_b == 4:
                self.win.emit(self._c)
                str1 = "ВЫ ВЫИГРАЛИ! Количество попыток: " + str(self._c)
                self.click_button1.emit(False)
                self.name_changed_str.emit("Новая игра")
            else:
                str1 = "Количество быков: " + str(count_b) + " Количество коров: " + str(count_c)
        self.value_changed_str.emit(str1)
        return
    
    
    def if_win(self, other):
        try:
            f = open("results.txt", "r")
            res = f.readlines()
            res[0] = "В этой таблице хранятся лучшие результаты игры Быки и коровы" + "\n"
            i = 1
            while i < len(res) and other >= int(res[i][-2]):
                i += 1
            if i <= 5:
                result, status = QInputDialog.getText(None, "", "Ваш результат - один из лучших. Внести ваш результат в таблицу?" + "\n" + "Ваше имя:")
                if status:
                    res.insert(i, result + " " + str(other) + "\n")
            if len(res) > 6:
                res.pop()
            f.close()
            f = open("results.txt", "w")
            for i in range(len(res)):
                f.write(res[i])
            f.close()
        except FileNotFoundError:
            str1 = "В этой таблице хранятся лучшие результаты игры Быки и коровы" + "\n"
            result, status = QInputDialog.getText(None, "", "Ваш результат - один из лучших. Внести ваш результат в таблицу?" + "\n" + "Ваше имя:")
            if status:
                f = open("results.txt", "w")
                f.write(str1 + result + " " + str(other) + "\n")
                f.close()
        return

                
    def new_game(self):
        if Button2.text() == "Сдаться":
            self.value_changed_str.emit("Правильное число:" + str(self._rn) + " Попробовать снова?")
            self.click_button1.emit(False)
            self.name_changed_str.emit("Новая игра")
        else:
            other = MyCow()
            sign = True
            self.new_value.emit([other._rn, other._pn, other._set, other._oldn, other._c])
            self.click_button1.emit(True)
            self.name_changed_str.emit("Сдаться")
            self.value_disappeared.emit("")
        return

    def watch_res(self):
        try:
            f = open("results.txt", "r")
            res = f.read()
            msgBox = QMessageBox()
            msgBox.setText(res)
            msgBox.exec()
        except FileNotFoundError:
            msgBox = QMessageBox()
            msgBox.setText("Результатов пока нет. Станьте первым!")
            msgBox.exec()



app = QApplication(sys.argv)
Window = QMainWindow()
Window.resize(700, 500)
Button_end = QPushButton("Вернуться на главную страницу", Window)
Button_end.setGeometry(10, 130, 400, 30)
Cows = MyCow()
Cows1 = Cow_game()
Label_2 = QLabel("Попробую угадать. Это 1234?", Window)
Label_ss2 = QLabel("Введите число быков и коров без запятых и пробелов.", Window)
Button21 = QPushButton("Ввести", Window)
Button22 = QPushButton("Новая игра", Window)
Line2 = QLineEdit(Window)
Label_2.setGeometry(10, 10, 400, 30)
Label_ss2.setGeometry(10, 90, 450, 30)
Line2.setGeometry(10, 50, 100, 30)
Button21.setGeometry(150, 50, 100, 30)
Button22.setGeometry(255, 50, 100, 30)
Line2.textChanged.connect(Cows1.setValue)
Button21.clicked.connect(Cows1.prog)
Button22.clicked.connect(Cows1.new_game)
Cows1.label_new.connect(Label_2.setText)
Cows1.value_disappeared.connect(Line2.setText)
Cows1.disabled.connect(Button21.setEnabled)
Line = QLineEdit(Window)
Button1 = QPushButton("Проверить", Window)
Button2 = QPushButton("Сдаться", Window)
Button3 = QPushButton("Посмотреть лучшие результаты", Window)
Label = QLabel("Добро пожаловать!", Window)
Label.setGeometry(10, 10, 400, 30)
Line.setGeometry(10, 50, 100, 30)
Button1.setGeometry(150, 50, 100, 30)
Button2.setGeometry(255, 50, 100, 30)
Button3.setGeometry(125, 90, 255, 30)
Line.textChanged.connect(Cows.setValue)
Button1.clicked.connect(Cows.how_many)
Button2.clicked.connect(Cows.new_game)
Button3.clicked.connect(Cows.watch_res)
Cows.new_value.connect(Cows.equal)
Cows.click_button1.connect(Button1.setEnabled)
Cows.value_changed_str.connect(Label.setText)
Cows.win.connect(Cows.if_win)
Cows.name_changed_str.connect(Button2.setText)
Cows.value_disappeared.connect(Line.setText)
Cows.value_disappeared.connect(Label.setText)

Label_s = QLabel("Выберите режим игры:", Window)
Button_s1 = QPushButton("Отгадывать", Window)
Button_s2 = QPushButton("Загадывать", Window)
Label_s.setGeometry(10, 10, 400, 30)
Button_s1.setGeometry(10, 50, 100, 30)
Button_s2.setGeometry(120, 50, 100, 30)
Button_s1.clicked.connect(Play_you)
Button_s2.clicked.connect(Play_comp)
Label_2.close()
Label_ss2.close()
Button21.close()
Button22.close()
Line2.close()
Line.close()
Button1.close()
Button2.close()
Button3.close()
Label.close()
Button_end.close()
Button_end.clicked.connect(New_choice)




Window.show()
app.exec_()