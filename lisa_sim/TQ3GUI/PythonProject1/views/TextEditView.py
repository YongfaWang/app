from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTextEdit, QShortcut, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt, QFile, QTextStream, QIODevice, pyqtSignal


class TextEditView(QDialog):
    runClicked = pyqtSignal()
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path

        # 设置模态属性（关键参数）
        self.setWindowModality(Qt.ApplicationModal)  # 完全模态[3](@ref)
        self.setWindowTitle(f"文本编辑器 - {file_path}")
        self.resize(800, 600)

        self.init_ui()
        self.load_file()

        # 快捷键绑定（保留原功能）
        QShortcut(Qt.CTRL + Qt.Key_S, self).activated.connect(self.save_file)

    def init_ui(self):
        btnLayout = QHBoxLayout()

        # 保存按钮（保持原样式）
        self.save_btn = QPushButton("保存", self)
        self.save_btn.clicked.connect(self.save_file)
        btnLayout.addWidget(self.save_btn)
        # 运行按钮（保持原样式）
        self.run_btn = QPushButton("运行", self)
        self.run_btn.clicked.connect(self.run_script)
        btnLayout.addWidget(self.run_btn)
        editLayout = QHBoxLayout()
        # 文本编辑区（继承原功能）
        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.text_changed)
        editLayout.addWidget(self.text_edit)
        parentDiv = QVBoxLayout()
        parentDiv.addLayout(btnLayout)
        parentDiv.addLayout(editLayout)
        self.setLayout(parentDiv)
    def text_changed(self):
        self.save_btn.setEnabled(True)
    def load_file(self):
        file = QFile(self.file_path)
        if file.open(QFile.ReadOnly | QFile.Text):
            self.text_edit.setPlainText(QTextStream(file).readAll())
        else:
            self.text_edit.setPlainText("")
        file.close()
    def run_script(self):
        self.save_file()
        self.run_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.run_btn.setText("运行中...")
        self.runClicked.emit()
    def save_file(self):
        self.save_btn.setEnabled(False)
        # 保存逻辑（综合网页6和网页7的实现）
        try:
            file = QFile(self.file_path)
            if not file.open(QIODevice.WriteOnly | QIODevice.Text):
                raise IOError(file.errorString())

            stream = QTextStream(file)
            stream << self.text_edit.toPlainText()
            file.close()
            #
            # QMessageBox.information(self, "保存成功",
            #                         f"文件已保存至：{self.file_path}")
            # self.accept()
        except Exception as e:
            QMessageBox.critical(self, "保存失败",
                                 f"保存过程中发生错误：\n{str(e)}")
