"""
Author: Big Panda
Created Time: 17.02.2025 9:23
Modified Time: 17.02.2025 9:23
Description:
    新增：
        1. 宠物静态图片加载
        2. 宠物鼠标拖动
"""
# Load modules
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        # setWindowFlags(Qt.WindowType.FramelessWindowHint) 用于设置窗口无边框
        # setWindowFlags(Qt.WindowType.WindowStaysOnTopHint) 用于设置窗口永远位于最上层
        # setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 用于设置透明背景
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 加载图片
        self.label = QLabel(self)  # 在 QWidget 上创建一个 QLabel 对象
        self.pixmap = QPixmap("C:\Project\PythonProject\LongSitReminderPet/Pets/MengJi_White.png")  # 加载图片
        self.label.setPixmap(self.pixmap)  # 将图片放到创建的 QLabel 对象上
        self.label.resize(self.pixmap.size())  # 根据图片大小调整窗口大小

        # 设置窗口初始位置
        self.move(100, 100)

        # 用于拖动窗口的变量
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        """
        鼠标按下事件：记录鼠标按下的位置

        事件只有鼠标与组件相互作用时才会起作用。意味着，如果在屏幕上非组件占据的其他位置点击鼠标，事件将不会被记录。
        """
        if event.button() == Qt.MouseButton.LeftButton:
            # event.globalPosition().toPoint() 表示鼠标当前点击位置位于整个屏幕的位置，屏幕左上角为坐标原点，初始为 QPointF 对象，使用 .toPoint() 后可以将坐标点转换为 QPoint 可四则运算的对象。
            # self.frameGeometry().topLeft() 表示鼠标点击位置相对于当前窗口的位置，窗口的左上角为坐标原点。其中，self.frameGeometry() 会给出组件左上角点的坐标以及组件的宽度和高度。
            # .topLeft() 则会从中提取出组件左上角的坐标点，使其变为 QPoint 对象，QPoint 对象类似 Coordinates，可以参与四则运算。
            # self.drag_position 中存放的是当使用窗口左上角为坐标原点时，鼠标点击的位置
            # 这里要计算 self.drag_position 位置的原因是我们希望鼠标点击拖动的时候是根据当前在组件上点击的位置进行拖动的，而不是左上角的位置。
            # 如果这里不计算 self.drag_position 的位置，那么后面在 mouseMoveEvent 中，我们拖动时鼠标首先会被自动定位到组件左上角的位置，会比较违和
            # print(self.frameGeometry())  # PyQt6.QtCore.QRect(100, 100, 140, 100)
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """
        鼠标移动事件：拖动窗口
        """
        # 判断当前鼠标左键是否被按下，拖动时，通常，鼠标左键处于持续按下状态
        if event.buttons() == Qt.MouseButton.LeftButton:
            # 计算新位置
            new_pos = event.globalPosition().toPoint() - self.drag_position

            # 获取屏幕的几何信息
            screen_geometry = QApplication.primaryScreen().geometry()

            # 限制窗口在屏幕内
            new_pos.setX(max(screen_geometry.left(), min(new_pos.x(), screen_geometry.right() - self.width())))
            new_pos.setY(max(screen_geometry.top(), min(new_pos.y(), screen_geometry.bottom() - self.height())))

            # 移动窗口
            self.move(new_pos)
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
