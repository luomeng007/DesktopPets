"""
Author: Big Panda
Created Time: 17.02.2025 9:23
Modified Time: 17.02.2025 9:23
Description:
    不是宠物版本的，自制仅 GUI 版本
"""
import sys
import time
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtMultimedia import QSoundEffect


class SitReminderApp(QWidget):
    def __init__(self):
        super().__init__()
        # initialize Gui
        self.setWindowTitle('HGXS Long Sit Reminder')  # Set window title
        self.setGeometry(100, 100, 420, 280)  # Set main Gui window size
        self.setWindowIcon(QIcon(r"./Icons/HGXS.ico"))  # Set window icon

        # initialize sound in MP3 format
        # self.click_sound_player = QMediaPlayer(self)
        # self.audio_output = QAudioOutput(self)
        # self.click_sound_player.setAudioOutput(self.audio_output)
        # self.click_sound_player.setSource(QUrl.fromLocalFile("./Musics/ClickButton.mp3"))  # Load MP3 sound file
        # self.audio_output.setVolume(1.0)  # set volume in interval (0.0, 1.0)

        # initialize sound in WAV format
        self.click_sound_player = QSoundEffect(self)
        self.click_sound_player.setSource(QUrl.fromLocalFile(r"./Musics/ClickButton.wav"))  # 加载音效文件
        self.click_sound_player.setVolume(1.0)  # 设置音量（0.0 到 1.0）

        layout = QVBoxLayout()

        self.label = QLabel("Click 'Start' button to start timing", self)
        layout.addWidget(self.label)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_timer)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_timer)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.remind)

        self.interval = 60 * 50  # 50 分钟
        self.is_running = False

    def play_sound(self):
        if self.click_sound_player.isLoaded():
            self.click_sound_player.play()

    def start_timer(self):
        self.play_sound()
        self.timer.start(self.interval * 1000)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.label.setText('Timing start')
        self.is_running = True

    def stop_timer(self):
        self.play_sound()
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.label.setText('Timing stop')
        self.is_running = False

    def remind(self):
        QMessageBox.information(self, 'HGXS assistant', 'You have sit for 50 minutes, please stand up to have a rest.')
        if self.is_running:
            self.timer.start(self.interval * 1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SitReminderApp()
    ex.show()
    sys.exit(app.exec())
