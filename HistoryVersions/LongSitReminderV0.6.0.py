"""
Author: Big Panda
Created Time: 17.02.2025 9:23
Modified Time: 17.02.2025 9:23
Description:
    当组件没有处于运行状态时，如果此时进行拖拽，组件在拖拽后回到指定位置，一切正常。
    新增：
        当组件位于运行状态时，如果此时进行拖拽，组件在拖拽后还是会回到拖拽前的位置。继续之前的移动过程。这对于我们是不能够接受的。
        我们想要即使组件处于移动状态，当我们进行拖拽后，终止组件当前的移动，并使得组件到达拖拽后的新位置。
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

        self.allow_move = True

    def mousePressEvent(self, event):
        """
        鼠标按下事件：记录鼠标按下的位置
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            # 新增：
            # 这里，我们需要判断当前是否有移动（动画）正在被执行，如果此时有动画正在被执行，停止当前动画。
            # 但是鼠标点击拖拽事件往往发生在鼠标 enterEvent 之后，在 enterEvent 中，如果组件正在移动，我们会将组件的移动状态设置为 paused。
            # 因此，这里，我们需要对组件的状态是否是 paused 进行判断而不是 Running
            event.accept()  # accept 仅仅是将事件标记为已处理，它的位置无关紧要

            # 因为当拖拽时存在两种情况，我们选择这种写法，第一种情况不牵扯 if 部分，第二种情况包含 if 部分。
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
            self.close()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
