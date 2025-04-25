"""
Author: Big Panda
Created Time: 17.02.2025 9:23
Modified Time: 17.02.2025 9:23
Description:
    新增：
        当鼠标悬停于组件上时，如果组件在自动移动，则暂停移动，鼠标离开时，恢复移动
"""
import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QRect
from PyQt6.QtGui import QPixmap


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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_random_move)
        self.timer.start(3000)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(2000)
        self.animation.finished.connect(self.on_animation_finished)

        # 新增：是否允许移动的标志
        self.allow_move = True

    def mousePressEvent(self, event):
        """
        鼠标按下事件：记录鼠标按下的位置
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
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
            self.close()

    def enterEvent(self, event):
        """
        新增：鼠标进入事件：停止移动
        """
        # 当鼠标进入到组件区域范围内时，此时触发 enterEvent，此时停止组件的移动，优先将可移动标识设置为 False
        # 然后判断动画运行的状态，如果动画的运行处于运行状态，那么暂停动画
        self.allow_move = False
        if self.animation.state() == QPropertyAnimation.State.Running:
            self.animation.pause()  # 暂停动画

    def leaveEvent(self, event):
        """
        新增：鼠标离开事件：恢复移动
        """
        # 当鼠标离开组件区域范围内时，此时触发 leaveEvent，此时停止组件的移动，优先将可移动标识设置为 True
        # 然后判断动画运行的状态，如果动画的运行处于暂停状态，那么恢复动画运行
        # 如果动画没有在运行，什么也不做
        self.allow_move = True
        if self.animation.state() == QPropertyAnimation.State.Paused:
            self.animation.resume()  # 恢复动画

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
