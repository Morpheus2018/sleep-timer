import os
import threading
import time
from datetime import datetime, timedelta
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMenu, QMenuBar
from PyQt5 import QtCore, QtGui, QtWidgets

from ui import main

class MyQtApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(MyQtApp, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Sleep Timer")

        # Timer starten
        self.timer = None

        # Signale und Slots verbinden
        self.cancel_button.clicked.connect(self.cancel_timer)
        self.exit_button.clicked.connect(self.cancel_timer)
        self.two_hours_button.clicked.connect(lambda: self.start_timer(2 * 60 * 60))
        self.one_hour_button.clicked.connect(lambda: self.start_timer(1 * 60 * 60))
        self.thirty_min_button.clicked.connect(lambda: self.start_timer(30 * 60))

        # Dark mode & StyleSheet
        self.dark_mode = True
        self.stylesheet()
        self.action_Dark_Mode.triggered.connect(self.toggle_dark_mode)

    def start_timer(self, duration):
        # Wenn bereits ein Timer läuft, diesen zuerst abbrechen
        if self.timer:
            self.timer.cancel()

        # Timer starten
        self.timer = CountdownTimer(duration, self)
        self.timer.start()

    def cancel_timer(self):
        # Timer abbrechen
        if self.timer:
            self.timer.cancel()
            self.timer = None
            self.time_label.setText("Timer Abgebrochen, neue Zeit wählen.")

    def set_time_label(self, time_str):
        self.time_label.setText("Heruntergefahren in: {} um {} Uhr.".format(time_str, (datetime.now() + timedelta(seconds=self.timer.duration)).strftime("%H:%M:%S")))

    def stylesheet(self):
        # StyleSheet
        self.setStyleSheet("background-color: #222222; color: #ffffff;")
        for button in self.findChildren(QPushButton):
            button.setStyleSheet("QPushButton:hover { background-color: rgba(135, 167, 82, 100%); border: 1px solid #00FF00; }")
        for qmenu in self.findChildren(QMenu):
            qmenu.setStyleSheet("QMenu::item:selected { background-color: rgba(135, 167, 82, 100%); border: 1px solid #00FF00; color: #fff; }")
        for qmenubar in self.findChildren(QMenuBar):
            qmenubar.setStyleSheet("QMenuBar::item:selected { background-color: rgba(135, 167, 82, 100%); border: 1px solid #00FF00; color: #fff; }")

    def set_dark_mode(self):
        # Dark mode aktivieren
        self.dark_mode = True
        self.setStyleSheet("background-color: #222222; color: #ffffff;")

    def set_light_mode(self):
        # Light mode aktivieren
        self.dark_mode = False
        self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def toggle_dark_mode(self):
        # Dark mode umschalten
        if self.dark_mode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def closeEvent(self, event):
        self.cancel_timer()
        event.accept()

class CountdownTimer:
    def __init__(self, duration, ui):
        self.duration = duration
        self.ui = ui
        self.end_time = datetime.now() + timedelta(seconds=duration)
        self.timer = None
        self.cancelled = False

    def start(self):
        self.timer = threading.Thread(target=self.run)
        self.timer.start()

    def run(self):
        try:
            while self.duration and not self.cancelled:
                hours, remainder = divmod(self.duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
                self.ui.set_time_label(time_str)
                time.sleep(1)
                self.duration -= 1
            if not self.cancelled:
                os.system("shutdown -h now")
        except KeyboardInterrupt:
            print("\nTimer Abgebrochen")

    def cancel(self):
        self.cancelled = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qt_app = MyQtApp()
    qt_app.show()
    sys.exit(app.exec_())