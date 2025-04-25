"""
Author: Big Panda
Created Time: 19.03.2025 15:07
Modified Time: 19.03.2025 15:07
Description:
    bug 修复：
        打包 bug 完全修复，打包方式可参考个人 CSDN 博客
"""
import os
import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QRect, QUrl
from PyQt6.QtGui import QPixmap, QAction, QIcon
from functools import partial
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

RANDOM_MOVE_TIME = 8000

GRATING_MESSAGES = [{'text': "Hi, 我是蒙吉，你最可爱的伙伴!", 'x_offset': -55},
                    {'text': 'Hi, 你的蒙吉来啦！', 'x_offset': -15},
                    {'text': 'Hi, 我是蒙吉，好久不见，有没有想我呀?', 'x_offset': -80}]

REMIND_MESSAGES = {'text': "坐的时间太久了，起来活动一下吧!", 'x_offset': -60}

MENGJI_MODELS = {'default': {'still': r"Pets\MengJi_White.png", "Drag": r"Pets\MengJi_White_Drag.png"},
                 'orange': {'still': r"Pets\MengJi_Orange.png", "Drag": r"Pets\MengJi_Orange_Drag.png"}}


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class PetStartMessage(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setGeometry(0, 0, 0, 80)
        self.setWindowIcon(QIcon(resource_path('Icons/Icon.ico')))

        # 创建提示语控件
        self.label = QLabel(text, self)
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 150);  /* 背景颜色（带透明度） */
                color: black;  /* 文字颜色 */
                padding: 10px;  /* 内边距 */
                border-radius: 10px;  /* 圆角 */
                font-size: 14px;  /* 字体大小 */
            }
        """)
        self.label.adjustSize()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.close)
        self.timer1.start(5000)  # 3 秒后关闭窗口


class LongSitRemind(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setGeometry(0, 0, 0, 80)
        self.setWindowIcon(QIcon(resource_path('Icons/Icon.ico')))

        # 创建提示语控件
        self.label = QLabel(text, self)
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 150);  /* 背景颜色（带透明度） */
                color: black;  /* 文字颜色 */
                padding: 10px;  /* 内边距 */
                border-radius: 10px;  /* 圆角 */
                font-size: 14px;  /* 字体大小 */
            }
        """)
        self.label.adjustSize()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.close)
        self.timer1.start(5000)  # 5 秒后关闭窗口


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setWindowIcon(QIcon(resource_path('Icons/Icon.ico')))

        # 新增： 默认宠物文件名称
        self.file_pet_default = MENGJI_MODELS['default']['still']
        self.path_pet_model_default = resource_path(self.file_pet_default)
        self.path_pet_model_Drag = resource_path(MENGJI_MODELS['default']['Drag'])

        self.label = QLabel(self)
        self.pixmap = QPixmap(self.path_pet_model_default)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.size())

        self.center()

        self.drag_position = QPoint()
        self.is_dragging = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_random_move)
        self.timer.start(RANDOM_MOVE_TIME)

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

        self.color_orange = QAction("橙色", self)
        self.change_color.addAction(self.color_orange)
        self.color_white = QAction("白色", self)
        self.change_color.addAction(self.color_white)

        self.tray_icon.setContextMenu(self.tray_menu)

        self.show_action.triggered.connect(self.show_window)
        self.color_orange.triggered.connect(partial(self.change_pet_color, MENGJI_MODELS['orange']['still']))
        self.color_white.triggered.connect(partial(self.change_pet_color, MENGJI_MODELS['default']['still']))
        self.exit_action.triggered.connect(self.close)

        self.tray_icon.show()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setSource(QUrl.fromLocalFile(resource_path(r"Musics\Superman.mp3")))

        rand_index = random.randint(0, len(GRATING_MESSAGES) - 1)
        self.tooltip = PetStartMessage(text=GRATING_MESSAGES[rand_index]['text'])
        self.tooltip.move(self.frameGeometry().x() + GRATING_MESSAGES[rand_index]['x_offset'], self.frameGeometry().y() - 70)
        self.tooltip.show()

        self.remind_timer = QTimer(self)
        self.remind_timer.timeout.connect(self.show_reminder)

        self.remind_window = None  # 用于存储提醒窗口

    def center(self):
        # 获取主屏幕可用区域
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        window_geo = self.label.frameGeometry()
        window_geo.moveCenter(screen_geometry.center())

        # 移动窗口到计算位置
        self.move(window_geo.topLeft())

    def mousePressEvent(self, event):
        """
        鼠标按下事件：记录鼠标按下的位置
        """
        if event.button() == Qt.MouseButton.LeftButton:
            if self.animation.state() == QPropertyAnimation.State.Paused:
                self.animation.stop()

            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.is_dragging = True
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
            # 新增：将位于 mousePressEvent 下的模型替换代码放置到 mouseMoveEvent 下
            self.path_pet_model_Drag = resource_path(''.join([self.file_pet_default.split('.')[0], '_Drag.', self.file_pet_default.split('.')[1]]))
            self.pixmap = QPixmap(self.path_pet_model_Drag)
            self.label.setPixmap(self.pixmap)
            self.label.setScaledContents(True)

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
            ...

    def enterEvent(self, event):
        """
        鼠标进入事件：停止移动
        """
        if self.timer.isActive():
            self.timer.stop()

        else:
            ...

        if self.animation.state() == QPropertyAnimation.State.Running:
            self.animation.pause()
        else:
            ...

    def leaveEvent(self, event):
        """
        鼠标离开事件：恢复移动
        """
        if self.allow_move:
            self.timer.start()
        else:
            ...

        if self.allow_move and self.animation.state() == QPropertyAnimation.State.Paused:
            self.animation.resume()
        else:
            ...

    def start_random_move(self):
        """
        开始随机移动窗口，每次移动距离不超过 100 像素
        """
        #
        # if self.animation.state() == QPropertyAnimation.State.Running:
        #     return

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
        self.file_pet_default = image_path
        self.path_pet_model_default = resource_path(self.file_pet_default)
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

        second_level_menu_long_sit_remind = QMenu('久坐提醒', First_level_menu)
        First_level_menu.addMenu(second_level_menu_long_sit_remind)

        action_minutes_30 = QAction("30 分钟", self)
        action_minutes_30.triggered.connect(partial(self.remind_timer.start, 5000))
        second_level_menu_long_sit_remind.addAction(action_minutes_30)

        action_minutes_45 = QAction("40 分钟", self)
        action_minutes_45.triggered.connect(partial(self.remind_timer.start, 45 * 000))
        second_level_menu_long_sit_remind.addAction(action_minutes_45)

        action_minutes_50 = QAction("50 分钟", self)
        action_minutes_50.triggered.connect(partial(self.remind_timer.start, 50 * 1000))
        second_level_menu_long_sit_remind.addAction(action_minutes_50)

        action_minutes_60 = QAction("60 分钟", self)
        action_minutes_60.triggered.connect(partial(self.remind_timer.start, 60 * 1000))
        second_level_menu_long_sit_remind.addAction(action_minutes_60)

        action_minimize = QAction("隐藏宠物", First_level_menu)
        action_minimize.triggered.connect(self.minimize_pet)
        First_level_menu.addAction(action_minimize)

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
        if not self.allow_move:
            self.allow_move = True
            self.timer.start(RANDOM_MOVE_TIME)
        else:
            ...

    def stop_move(self):
        """
       停止移动
       """
        if self.allow_move:
            self.allow_move = False
            if self.animation.state() == QPropertyAnimation.State.Running:
                self.animation.stop()
            self.timer.stop()
        else:
            ...

    def minimize_pet(self):
        """
       最小化宠物
       """
        self.hide()

    def hide_tooltip(self):
        """
        隐藏提示语
        """
        self.tooltip.hide()
        self.tooltip_timer.stop()

    # def remind_timer(self, time):
    #     """
    #     开启计时器，定时提示休息信息
    #     """
    #     # 当坐的太久的时候，提示用户起来活动活动
    #
    #     self.timer_remind.start(time)

    def show_reminder(self):
        """
        等待一段时间后，开始计时
        """
        if self.remind_window is None or not self.remind_window.isVisible():
            self.remind_window = LongSitRemind(text=REMIND_MESSAGES['text'])
            self.remind_window.move(self.frameGeometry().x() + REMIND_MESSAGES['x_offset'], self.frameGeometry().y() - 70)
            self.remind_window.show()

        # 可选：停止定时器，避免重复提醒
        self.remind_timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
