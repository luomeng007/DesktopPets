"""
Author: Big Panda
Created Time: 19.03.2025 17:07
Modified Time: 19.03.2025 17:07
Description:
    
"""
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt


class TooltipWindow(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        # 设置窗口无边框和透明背景
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 因为后面，我们让自动调节 label 大小适应内容，因此，这里，我们无需设置宽度，仅设置高度来类似设置字体大小
        self.setGeometry(0, 0, 0, 80)

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
        self.label.adjustSize()  # 调整大小以适应内容

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 使用定时器关闭窗口
        # 位于主 QWidget 中的定时器，我们也可以移动到这里使用
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.close)
        self.timer1.start(5000)  # 3 秒后关闭窗口


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建提示语窗口
    tooltip = TooltipWindow("这是一个外部提示语！")
    tooltip.show_at(500, 300)  # 在屏幕坐标 (500, 300) 处显示

    sys.exit(app.exec())
