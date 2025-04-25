"""
Author: Big Panda
Created Time: 17.02.2025 9:23
Modified Time: 17.02.2025 9:23
Description:
    新增：
        1. 在宠物组件上双击鼠标左键关闭窗口
"""
import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint, QTimer
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
        新增：双击事件，关闭窗口

        当我们在窗口上双击鼠标左键时，关闭窗口
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.close()

    def start_random_move(self):
        """
        开始随机移动窗口，每次移动距离不超过 100 像素
        """
        current_geometry = self.geometry()
        current_x = current_geometry.x()
        current_y = current_geometry.y()

        new_x = current_x + random.randint(-100, 100)
        new_y = current_y + random.randint(-100, 100)

        screen_geometry = QApplication.primaryScreen().geometry()

        new_x = max(screen_geometry.left(), min(new_x, screen_geometry.right() - self.width()))
        new_y = max(screen_geometry.top(), min(new_y, screen_geometry.bottom() - self.height()))

        self.move(new_x, new_y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
