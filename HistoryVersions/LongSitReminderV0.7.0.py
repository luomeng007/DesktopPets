"""
Author: Big Panda
Created Time: 17.02.2025 9:23
Modified Time: 17.02.2025 9:23
Description:
    当组件位于运行状态时，如果此时进行拖拽，当前的运行会被终止，组件会到达拖拽后的位置，尝试有没有可能当被拖拽后，组件继续刚才的运动，不停止呢？
    考虑需要更新坐标。但是感觉这个功能没有任何必要，舍弃开发。
    新增：
        Windows 右下角任务栏中出现一个它的图标，且实现双击组件隐藏它的功能。同时在任务栏窗口上，我们右键点击它可以打开菜单栏，有两个菜单选项，
        其中一个是重新显示它，另一个是退出。

"""
import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu  # 新增：导入 QSystemTrayIcon, QMenu 模块
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QRect
from PyQt6.QtGui import QPixmap, QAction, QIcon  # 新增：导入 QAction, QIcon 模块


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.pixmap = QPixmap(r"C:\Project\PythonProject\LongSitReminderPet/Pets/MengJi_White.png")
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.size())

        self.move(100, 100)

        self.drag_position = QPoint()
        self.is_dragging = False  # 新增：是否正在被移动标识

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_random_move)
        self.timer.start(3000)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(2000)
        self.animation.finished.connect(self.on_animation_finished)

        self.allow_move = True

        # 新增：创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(r"C:\Project\PythonProject\LongSitReminderPet/Pets/MengJi_White.png"))  # 设置托盘图标
        self.tray_icon.setToolTip("Desktop Pet")  # 设置托盘图标的提示文本

        # 新增：创建托盘图标的右键菜单
        self.tray_menu = QMenu()
        self.show_action = QAction("显示", self)
        self.exit_action = QAction("退出", self)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.exit_action)
        self.tray_icon.setContextMenu(self.tray_menu)

        # 新增：连接菜单项的信号
        self.show_action.triggered.connect(self.show_window)
        self.exit_action.triggered.connect(self.close)

        # 显示托盘图标
        self.tray_icon.show()

    def mousePressEvent(self, event):
        """
        鼠标按下事件：记录鼠标按下的位置
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            # 新增：
            # 无论何时，只要鼠标点击事件被在组件上触发，意味着此时组件处于拖拽状态，第一时间应将 self.is_dragging 标识设置为 True
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
            self.hide()  # 新增： 双击时不再关闭窗口，而是隐藏窗口

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
        新增：显示窗口
        """
        self.show()

    def closeEvent(self, event):
        """
        新增：关闭事件：隐藏窗口而不是关闭
        """
        # 在 mouseDoubleClickEvent 句柄中，我们实现了双击关闭组件，即退出的功能。这里我们将关闭事件进行忽略，即实现了当双击组件关闭时，只最小化隐藏窗口。
        event.accept()  # 执行关闭操作


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
