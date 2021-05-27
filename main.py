# -*- coding: utf-8 -*-
import sys
import random
import pandas as pd
from functools import partial
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtUiTools import QUiLoader


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load('form.ui')

        self.db = pd.read_csv('DB.txt', sep=',')
        self.ui.btn_tr.clicked.connect(self.translate)
        self.ui.btn_clr.clicked.connect(self.reset)
        self.ui.btn_a.clicked.connect(self.arrange)

        self.ui.btn_pass.clicked.connect(self.password)
        self.weak_pass_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.good_pass_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&|?><:;~'
        self.pass_word = ''

        self.ui.btn_start.clicked.connect(self.guess_game)
        self.ui.btn_reset.clicked.connect(self.reset_guess)
        self.ui.btn_check.clicked.connect(self.check_guess)

        self.ui.show()

    def guess_game(self):
        self.guess_count = 0
        self.ui.lbl_guess.setText('my number is in range [1, 20]')
        self.random_num = random.randint(1, 20)
        self.ui.hads.setText('')


    def check_guess(self):
        if self.ui.hads.text() != '':
            self.guessed = int(self.ui.hads.text())
            if self.random_num > self.guessed:
                self.ui.lbl_guess.setText('Lower!')
                self.guess_count += 1
            elif self.random_num < self.guessed:
                self.ui.lbl_guess.setText('Higher!')
                self.guess_count += 1
            elif self.random_num == self.guessed:
                self.ui.lbl_guess.setText('Correct!')
                self.guess_count += 1
                msg_box = QMessageBox()
                msg_box.setText(f'you tried {self.guess_count} times!')
                msg_box.exec()

    def reset_guess(self):
        self.ui.lbl_guess.setText('Try to guess my number AGAIN!')
        self.ui.hads.setText('')

    def arrange(self):
        self.text_in = self.ui.te_in.toPlainText()
        print(self.text_in)
        self.ui.te_out.setText(self.text_in.replace('\n', ''))

    def password(self):
        #self.ui.tb_pass.setText('')
        if self.ui.rb_w.isChecked():
            self.pass_word = ''
            for i in range(7):
                self.pass_word = self.pass_word + random.choice(self.weak_pass_list)
            #self.ui.tb_pass.setText(self.pass_word)
        elif self.ui.rb_n.isChecked():
            self.pass_word = ''
            for i in range(10):
                self.pass_word = self.pass_word + random.choice(self.good_pass_list)
            #self.ui.tb_pass.setText(self.pass_word)
        elif self.ui.rb_s.isChecked():
            self.pass_word = ''
            for i in range(18):
                self.pass_word = self.pass_word + random.choice(self.good_pass_list)
            #self.ui.tb_pass.setText(self.pass_word)
        if any(c.isdigit() for c in self.pass_word):
            self.ui.tb_pass.setText(self.pass_word)
        else:
            self.ui.tb_pass.setText((self.pass_word) + str(random.randint(0,9)))



    def translate(self):
        if self.ui.rb_en_fa.isChecked():
            if self.ui.tb_in.text() != '':
                self.word = self.ui.tb_in.text()
                if len(self.db[self.db['word'].str.contains(self.word)]['word'])>0:
                    self.ui.tb_out.setText('')
                    self.mean = self.db[self.db['word'].str.contains(self.word)]['meaning'].item()
                    self.ui.tb_out.setText(self.mean)
                else:
                    msg_box = QMessageBox()
                    msg_box.setText("Unknown Word, please input from one to ten")
                    msg_box.exec()

        elif self.ui.rb_fa_en.isChecked():
            if self.ui.tb_out.text() != '':
                self.word = self.ui.tb_out.text()
                if len(self.db[self.db['meaning'].str.contains(self.word)]['meaning'])>0:
                    self.ui.tb_in.setText('')
                    self.mean = self.db[self.db['meaning'].str.contains(self.word)]['word'].item()
                    self.ui.tb_in.setText(self.mean)
                else:
                    msg_box = QMessageBox()
                    msg_box.setText("لطفا از کلمات یک تا ده انتخاب کنید")
                    msg_box.exec()

    def reset(self):
        self.ui.tb_out.setText('')
        self.ui.tb_in.setText('')

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
