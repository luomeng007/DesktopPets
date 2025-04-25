"""
Author: Big Panda
Created Time: 17.02.2025 9:23
Modified Time: 17.02.2025 9:23
Description:
    新增：
        在宠物上右键弹出选项窗口，可以实现音乐播放效果, 实现创建音乐两级菜单。
            一级菜单：
            1. 音乐
                二级菜单：
                1. 播放音乐
                2. 停止音乐

            但是目前播放音乐时会存在 warning 提示，这个问题后期跟进
        新增 resource_path 函数，使得程序打包输出时可以集成用户的所有数据，从该版本后，所有数据文件导入时都可以使用绝对路径，使用绝对路径导入数据是我们推荐的。

"""
import os
import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QRect, QUrl
from PyQt6.QtGui import QPixmap, QAction, QIcon
from functools import partial
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput  # 新增 QMediaPlayer, QAudioOutput 模块


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.pixmap = QPixmap(resource_path(r"C:\Project\PythonProject\LongSitReminderPet\Pets\MengJi_White.png"))
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.size())

        self.move(100, 100)

        self.drag_position = QPoint()
        self.is_dragging = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_random_move)
        self.timer.start(3000)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(2000)
        self.animation.finished.connect(self.on_animation_finished)

        self.allow_move = True

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path(r"C:\Project\PythonProject\LongSitReminderPet\Pets\MengJi_White.png")))
        self.tray_icon.setToolTip("Desktop Pet")

        self.tray_menu = QMenu()

        self.tray_menu.setStyleSheet("""
            QMenu {
                background-color: black;  /* 菜单背景颜色 */
                border: 2px solid #000000;  /* 菜单边框(宽度，样式，颜色) */
                border-radius: 10px;  /* 菜单边框圆角 */
            }
            QMenu::item {
                padding-left: 50px;  /* 左侧留出空间 */
                padding-right: 50px;  /* 右侧留出空间 */
                text-align: center;  /* 文字居中 */
                font-size: 14px;    /* 设置字体大小 */
                color: white;
                background-color: black;
            }
            QMenu::item:hover {
                background-color: #005bb5;  /* 鼠标悬停时的背景颜色 */
                color: white;  /* 鼠标悬停时的文字颜色 */
            }
            QMenu::item:pressed {
                background-color: #5B9BD5;  /* 鼠标按下时的背景颜色 */
                color: white;  /* 鼠标按下时的文字颜色 */
            }
        """)

        self.show_action = QAction("显示", self)
        self.change_color = QMenu("更换颜色", self.tray_menu)
        self.change_pet = QMenu("更换宠物", self.tray_menu)
        self.exit_action = QAction("退出", self)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addMenu(self.change_color)
        self.tray_menu.addMenu(self.change_pet)
        self.tray_menu.addAction(self.exit_action)

        self.color_yellow = QAction("黄色", self)
        self.change_color.addAction(self.color_yellow)
        self.color_white = QAction("白色", self)
        self.change_color.addAction(self.color_white)

        self.tray_icon.setContextMenu(self.tray_menu)

        self.show_action.triggered.connect(self.show_window)
        self.color_yellow.triggered.connect(partial(self.change_pet_color, resource_path(r'C:\Project\PythonProject\LongSitReminderPet\Pets\MengJi_Orange.png')))
        self.color_white.triggered.connect(partial(self.change_pet_color, resource_path(r'C:\Project\PythonProject\LongSitReminderPet\Pets\MengJi_White.png')))
        self.exit_action.triggered.connect(self.close)

        self.tray_icon.show()

        # 新增：允许右键菜单
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # 新增：初始化音乐播放器
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        # self.audio_output.setVolume(2)  # 設定音量
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setSource(QUrl.fromLocalFile(r"C:\Project\PythonProject\LongSitReminderPet\Musics\Superman.mp3"))  # 替换为你的音乐文件路径

    def mousePressEvent(self, event):
        """
        鼠标按下事件：记录鼠标按下的位置
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.is_dragging = True
            event.accept()

            if self.animation.state() == QPropertyAnimation.State.Paused:
                self.animation.stop()

    def mouseMoveEvent(self, event):
        """
        鼠标移动事件：拖动窗口
        """
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            screen_geometry = QApplication.primaryScreen().geometry()

            new_pos.setX(max(screen_geometry.left(), min(new_pos.x(), screen_geometry.right() - self.width())))
            new_pos.setY(max(screen_geometry.top(), min(new_pos.y(), screen_geometry.bottom() - self.height())))

            self.move(new_pos)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        """
        双击事件，关闭窗口
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.hide()

    def enterEvent(self, event):
        """
        鼠标进入事件：停止移动
        """
        self.allow_move = False
        if self.animation.state() == QPropertyAnimation.State.Running:
            self.animation.pause()

    def leaveEvent(self, event):
        """
        鼠标离开事件：恢复移动
        """
        self.allow_move = True
        if self.animation.state() == QPropertyAnimation.State.Paused:
            self.animation.resume()

    def start_random_move(self):
        """
        开始随机移动窗口，每次移动距离不超过
        100
        像素
        """
        #
        if self.animation.state() == QPropertyAnimation.State.Running:
            return

        current_geometry = self.geometry()
        current_x = current_geometry.x()
        current_y = current_geometry.y()

        new_x = current_x + random.randint(-100, 100)
        new_y = current_y + random.randint(-100, 100)

        screen_geometry = QApplication.primaryScreen().geometry()

        new_x = max(screen_geometry.left(), min(new_x, screen_geometry.right() - self.width()))
        new_y = max(screen_geometry.top(), min(new_y, screen_geometry.bottom() - self.height()))

        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(QRect(new_x, new_y, self.width(), self.height()))

        self.animation.start()

    def on_animation_finished(self):
        """
        动画结束时的回调函数
        """
        pass

    def show_window(self):
        """
        显示窗口
        """
        self.show()

    def closeEvent(self, event):
        """
        关闭事件：隐藏窗口而不是关闭
        """
        event.accept()

    def change_pet_color(self, image_path):
        self.pixmap = QPixmap(image_path)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.size())
        self.tray_icon.setIcon(QIcon(image_path))

    # 实现音乐播放功能
    def show_context_menu(self, pos):
        """
        显示右键菜单
        """
        # 创建菜单
        menu = QMenu(self)

        # 新增：音乐二级菜单
        music_menu = QMenu('音乐', menu)
        menu.addMenu(music_menu)

        # 新增：添加“播放音乐”选项
        play_music_action = QAction("播放音乐", self)
        play_music_action.triggered.connect(self.play_music)
        music_menu.addAction(play_music_action)

        # 新增：添加“停止音乐”选项
        stop_music_action = QAction("停止音乐", self)
        stop_music_action.triggered.connect(self.stop_music)
        music_menu.addAction(stop_music_action)

        # 显示菜单
        menu.exec(self.mapToGlobal(pos))

    def play_music(self):
        """
        播放音乐
        """
        # 新增：播放音乐
        if self.media_player.isPlaying():
            ...
        else:
            self.media_player.play()

    def stop_music(self):
        """
        播放音乐
        """
        # 新增：停止音乐
        if self.media_player.isPlaying():
            self.media_player.stop()
        else:
            ...


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
