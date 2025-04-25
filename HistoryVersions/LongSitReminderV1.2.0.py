"""
Author: Big Panda
Created Time: 19.03.2025 14:23
Modified Time: 19.03.2025 14:23
Description:
    Bug 修复，目前，当我们选择停止移动时，一切正常，但是当停止移动后拖拽 pet 到新位置时，pet 又会重新开始进入随机移动状态，这是不合理的，对这个逻辑进行修复
"""
import os
import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QRect, QUrl
from PyQt6.QtGui import QPixmap, QAction, QIcon
from functools import partial
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 新增：设定初始化时 pet 模型路径变量
        self.path_pet_model_default = resource_path(r"C:\Project\PythonProject\LongSitReminderPet/Pets/MengJi_White.png")
        self.path_pet_model_Drag = resource_path(r"C:\Project\PythonProject\LongSitReminderPet/Pets/MengJi_White_Drag.png")

        self.label = QLabel(self)
        self.pixmap = QPixmap(self.path_pet_model_default)
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
        self.tray_icon.setIcon(QIcon(self.path_pet_model_default))
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
        self.color_yellow.triggered.connect(partial(self.change_pet_color, resource_path(r'C:\Project\PythonProject\LongSitReminderPet/Pets/MengJi_Orange.png')))
        self.color_white.triggered.connect(partial(self.change_pet_color, resource_path(r'C:\Project\PythonProject\LongSitReminderPet/Pets/MengJi_White.png')))
        self.exit_action.triggered.connect(self.close)

        self.tray_icon.show()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setSource(QUrl.fromLocalFile(r"C:\Project\PythonProject\LongSitReminderPet\Musics\Superman.mp3"))

    def mousePressEvent(self, event):
        """
        鼠标按下事件：记录鼠标按下的位置
        """
        if event.button() == Qt.MouseButton.LeftButton:
            if self.animation.state() == QPropertyAnimation.State.Paused:
                self.animation.stop()

            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.is_dragging = True
            self.path_pet_model_Drag = ''.join([self.path_pet_model_default.split('.')[0], '_Drag.', self.path_pet_model_default.split('.')[1]])
            self.pixmap = QPixmap(self.path_pet_model_Drag)
            self.label.setPixmap(self.pixmap)
            self.label.setScaledContents(True)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pixmap = QPixmap(self.path_pet_model_default)
            self.label.setPixmap(self.pixmap)
            self.label.setScaledContents(True)
            event.accept()

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
        self.stop_move()
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
        开始随机移动窗口，每次移动距离不超过 100 像素
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
        self.path_pet_model_default = image_path
        self.pixmap = QPixmap(self.path_pet_model_default)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.size())
        self.tray_icon.setIcon(QIcon(self.path_pet_model_default))

    def show_context_menu(self, pos):
        """
        显示右键菜单
        """
        First_level_menu = QMenu(self)

        second_level_menu_music = QMenu('音乐', First_level_menu)
        First_level_menu.addMenu(second_level_menu_music)

        action_play_music = QAction("播放音乐", First_level_menu)
        action_play_music.triggered.connect(self.play_music)
        second_level_menu_music.addAction(action_play_music)

        action_stop_music = QAction("停止音乐", First_level_menu)
        action_stop_music.triggered.connect(self.stop_music)
        second_level_menu_music.addAction(action_stop_music)

        second_level_menu_move = QMenu('随机移动', First_level_menu)
        First_level_menu.addMenu(second_level_menu_move)

        action_start_move = QAction("开始移动", self)
        action_start_move.triggered.connect(self.start_move)
        second_level_menu_move.addAction(action_start_move)

        action_stop_move = QAction("停止移动", self)
        action_stop_move.triggered.connect(self.stop_move)
        second_level_menu_move.addAction(action_stop_move)

        First_level_menu.exec(self.mapToGlobal(pos))

    def play_music(self):
        """
        播放音乐
        """
        if self.media_player.isPlaying():
            ...
        else:
            self.media_player.play()

    def stop_music(self):
        """
        播放音乐
        """
        if self.media_player.isPlaying():
            self.media_player.stop()
        else:
            ...

    def start_move(self):
        """
       开始移动
       """
        self.timer.start(3000)

    def stop_move(self):
        """
       停止移动
       """

        self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
