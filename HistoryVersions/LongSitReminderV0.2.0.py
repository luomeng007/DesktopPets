"""
Author: Big Panda
Created Time: 17.02.2025 9:23
Modified Time: 17.02.2025 9:23
Description:
    新增：
        1. 宠物随机移动
"""
import sys
import random  # 新增 random 模块用于控制随机移动
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint, QTimer  # 新增 QTimer 模块用于计时，一定时间后进行随机移动操作
from PyQt6.QtGui import QPixmap


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.pixmap = QPixmap("C:\Project\PythonProject\LongSitReminderPet/Pets/MengJi_White.png")
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.size())

        self.move(100, 100)

        self.drag_position = QPoint()

        # 新增：定时器：用于触发随机移动
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

    def start_random_move(self):
        """
        新增： 开始随机移动窗口，每次移动距离不超过 100 像素
        """
        # 获取当前窗口位置
        # self.geometry() 获取当前窗口的坐标，返回的是一个 QRect 对象，窗口左上角坐标以及窗口的宽度和高度值，
        # 注意我们自定义的函数这里用的是 self.geometry()，而 mousePressEvent 内置句柄中用的却是 self.frameGeometry()
        # self.geometry().x() 用于获取组件（宠物）所对应的 x 坐标值，self.geometry().y() 用于获取组件（宠物）所对应的 y 坐标值
        current_geometry = self.geometry()
        current_x = current_geometry.x()
        current_y = current_geometry.y()

        # 生成随机目标位置，限制移动距离不超过 100 像素
        new_x = current_x + random.randint(-100, 100)
        new_y = current_y + random.randint(-100, 100)

        # 获取屏幕的几何信息
        screen_geometry = QApplication.primaryScreen().geometry()

        # 限制目标位置在屏幕内
        new_x = max(screen_geometry.left(), min(new_x, screen_geometry.right() - self.width()))
        new_y = max(screen_geometry.top(), min(new_y, screen_geometry.bottom() - self.height()))

        # 移动到新的坐标点
        self.move(new_x, new_y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
