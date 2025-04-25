"""
Author: Big Panda
Created Time: 17.02.2025 9:23
Modified Time: 17.02.2025 9:23
Description:
    新增：
        目前的随机移动是瞬移过程，加入 QPropertyAnimation 动画效果使移动过程变得平滑
"""
import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QRect  # 新增 QRect，在设置动画效果终止位置时使用
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

        # 新增：动画对象
        # 我们的随机移动时间为 3 秒，为了确保下次随机移动开始前，本次随机移动过程已经结束，因此，我们需要设置动画持续时间小于随机移动计时时间。
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(2000)  # 动画持续时间（2秒）
        self.animation.finished.connect(self.on_animation_finished)

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

    def start_random_move(self):
        """
        开始随机移动窗口，每次移动距离不超过 100 像素
        """
        # 如果动画正在运行，则跳过, 本质上，因为我们前面的时间设定，这里我们无需进行判断操作，但是为了逻辑上的闭环，仍旧进行判断
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

        # 设置动画的起始和结束位置
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(QRect(new_x, new_y, self.width(), self.height()))

        # 启动动画
        self.animation.start()
        # 本质上，这里我们只是使用了动画移动的效果来替代了原始 self.move(new_x, new_y) 的瞬间移动效果。

    def on_animation_finished(self):
        """
        新增：动画结束时的回调函数
        """
        pass  # 可以在这里添加动画结束后的逻辑，目前我们在动画结束后无需进行任何操作，因此，这里我们使用 pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
