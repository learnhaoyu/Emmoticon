import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QMessageBox, QDesktopWidget)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QCoreApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Emmoticon")
        self.setWindowIcon(QIcon(".\\downloadimg\\8bitheart.png"))
        # 这种静态的方法设置一个用于显示工具提示的字体。我们使用10px滑体字体。
        QToolTip.setFont(QFont('SansSerif', 10))

        # 创建一个提示，我们称之为settooltip()方法。我们可以使用丰富的文本格式
        self.setToolTip('This is a <b>QWidget</b> widget')

        # 创建一个PushButton并为他设置一个tooltip
        btn = QPushButton('Quit', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.clicked.connect(QCoreApplication.instance().quit)

        # btn.sizeHint()显示默认尺寸
        btn.resize(btn.sizeHint())

        # 移动窗口的位置
        btn.move(50, 50)

        self.resize(650, 500)
        self.center()

        self.show()

    def closeEvent(self, QCloseEvent):
        reply=QMessageBox.question(self,"Message","Are you sure to quit",QMessageBox.Yes|QMessageBox.No)
        if reply==QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())


app = QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())