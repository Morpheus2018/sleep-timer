import os
import threading
import time
from datetime import datetime, timedelta
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout


class SleepTimer(QWidget):
    def __init__(self):
        super().__init__()

        # Timer starten
        self.timer = None

        # Set window title
        self.setWindowTitle("Sleep Timer")

        # GUI-Elemente erstellen
        self.label = QLabel("Sleep Timer")
        self.time_label = QLabel()
        self.cancel_button = QPushButton("Abbrechen")
        self.two_hours_button = QPushButton("2 Stunden")
        self.one_hour_button = QPushButton("1 Stunde")
        self.thirty_min_button = QPushButton("30 Minuten")

        # Layout erstellen
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.cancel_button)
        self.layout.addWidget(self.two_hours_button)
        self.layout.addWidget(self.one_hour_button)
        self.layout.addWidget(self.thirty_min_button)
        self.setLayout(self.layout)

        # Signale und Slots verbinden
        self.cancel_button.clicked.connect(self.cancel_timer)
        self.two_hours_button.clicked.connect(lambda: self.start_timer(2 * 60 * 60))
        self.one_hour_button.clicked.connect(lambda: self.start_timer(1 * 60 * 60))
        self.thirty_min_button.clicked.connect(lambda: self.start_timer(30 * 60))

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
            self.time_label.setText("Timer Abgebrochen")

    def set_time_label(self, time_str):
        self.time_label.setText("Heruntergefahren in {} um {} Uhr".format(time_str, (datetime.now() + timedelta(seconds=self.timer.duration)).strftime("%H:%M:%S")))


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sleep_timer = SleepTimer()
    sleep_timer.show()
    sleep_timer.resize(310, 0)
    sys.exit(app.exec_())
