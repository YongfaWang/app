import sys

from PyQt5.QtWidgets import QApplication

from views.MainWidget import MainWidget

if __name__ == '__main__':
    # 创建Qt应用程序实例
    app = QApplication(sys.argv)
    # # 创建窗口
    # window = MainView()
    # # 显示窗口
    # window.show()
    mainWidget = MainWidget()
    mainWidget.show()
    # 运行Qt应用程序
    sys.exit(app.exec_())