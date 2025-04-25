#!/usr/bin/python

from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPainter, QPixmap, QPainterPath
from PyQt6.QtCore import QPoint, QPropertyAnimation, pyqtProperty
import sys


class Ball(QLabel):

    def __init__(self, parent):
        super().__init__(parent)

        pix = QPixmap("ball.png")
        self.h = pix.height()
        self.w = pix.width()

        self.setPixmap(pix)

    def _set_pos(self, pos):

        self.move(pos.x() - self.w//2, pos.y() - self.h//2)

    pos = pyqtProperty(QPoint, fset=_set_pos)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initView()
        self.initAnimation()

    def initView(self):

        self.path = QPainterPath()
        self.path.moveTo(30, 30)
        self.path.cubicTo(30, 30, 200, 350, 350, 30)

        self.ball = Ball(self)

        self.ball.pos = QPoint(30, 30)

        self.setWindowTitle("Animation along curve")
        self.setGeometry(300, 300, 400, 300)
        self.show()

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        qp.drawPath(self.path)
        qp.end()

    def initAnimation(self):

        self.anim = QPropertyAnimation(self.ball, b'pos')
        self.anim.setDuration(7000)

        self.anim.setStartValue(QPoint(30, 30))

        vals = [p/100 for p in range(0, 101)]

        for i in vals:
            self.anim.setKeyValueAt(i, self.path.pointAtPercent(i))

        self.anim.setEndValue(QPoint(350, 30))
        self.anim.start()


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
