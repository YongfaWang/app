from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction, QPushButton, QVBoxLayout, QWidget

from views.resList import ResList


class H5ViewerWindow(QMainWindow):
    def __init__(self, h5_filepath=None):
        super().__init__()
        self.h5_filepath = h5_filepath
        # 设置窗口标题
        self.setWindowTitle('H5 Viewer')
        # 设置窗口大小
        self.resize(400, 300)
        # 创建状态栏并显示信息
        # self.statusBar().showMessage('这是状态栏提示', 5000)
        # 在 __init__ 方法中添加以下代码
        self.open_action = QAction("打开", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)
        self.addAction(self.open_action)
        self.init_ui()
        # 设置样式
        self.setStyleSheet("""
                    QPushButton {
                        background: #CCCCCC;
                        color: black;
                        padding: 8px 20px;
                        min-width: 80px;
                        border-radius: 4px;
                    }
                    QPushButton:hover { background: #999999; }
                    QPushButton:pressed { background: #666666; }
                """)
        if h5_filepath:
            self.open_file()

    def open_file(self):
        if not self.h5_filepath:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "HDF5文件 (*.h5)", options=options)
            if file_path:
                print(f"打开的文件路径: {file_path}")
                # 这里可以添加处理文件路径的逻辑
                self.resList.load_h5_structure(h5_path=file_path)
        else:
            self.resList.load_h5_structure(h5_path=self.h5_filepath)
    # 正确的QMainWindow布局流程
    def init_ui(self):
        # 创建中央容器
        central_widget = QWidget()
        self.setCentralWidget(central_widget)  # 关键步骤[1](@ref)

        # 创建布局并绑定到中央容器
        main_layout = QVBoxLayout(central_widget)

        # 添加子部件
        self.resList = ResList()
        self.openFileBtn = QPushButton('打开文件')
        main_layout.addWidget(self.resList)
        main_layout.addWidget(self.openFileBtn)

        # 信号连接
        self.openFileBtn.clicked.connect(self.open_file)