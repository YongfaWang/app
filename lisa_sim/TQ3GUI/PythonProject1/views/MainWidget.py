import os
import subprocess
import sys
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget, QDialog
from fontTools.unicodedata import script

from views.TextEditView import TextEditView
from views.generated.Ui_MainWidget import Ui_MainWidget
from views.h5ViewerWindow import H5ViewerWindow


def getCurrentPath():
    return os.path.split(os.path.abspath(__file__))[0]
class MainWidget(QWidget, Ui_MainWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap(getCurrentPath() + "\\..\\resources\\images\\bg.png")))
        # self.setPalette(palette)
        bg_path = os.path.join(getCurrentPath(), "..","resources","images","bg.png")
        bg_pixmap = QPixmap(bg_path)
        self.setAutoFillBackground(True)  # 启用自动填充背景
        # 缩放图片至当前窗口大小，忽略宽高比
        scaled_pixmap = bg_pixmap.scaled(
            self.size(),
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation  # 平滑缩放
        )
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)
        self.btn1.clicked.connect(self.orbitsClicked)
        self.btn2.clicked.connect(self.responseClicked)
        self.btn3.clicked.connect(self.instrumentClicked)
        self.btn4.clicked.connect(self.h5ViewerClicked)
        self.pushButton_7.clicked.connect(self.glitchsClicked)
    def responseClicked(self):
        ini_path = os.path.normpath(os.path.join(getCurrentPath(), "..", "..", "..", "tests-gw-response", "gw_response.ini"))
        script_path = os.path.normpath(os.path.join(getCurrentPath(), "..", "..", "..", "tests-gw-response", "main_response.py"))
        self.showEditor(ini_path, script_path)
    def orbitsClicked(self):
        ini_path = os.path.normpath(os.path.join(getCurrentPath(), "..", "..", "..", "testorbits", "orbits.ini"))
        script_path = os.path.normpath(os.path.join(getCurrentPath(), "..", "..", "..", "testorbits", "main_orbits.py"))
        self.showEditor(ini_path, script_path)
    def glitchsClicked(self):
        ini_path = os.path.normpath(os.path.join(getCurrentPath(), "..", "..", "..", "lisaglitch-1.3", "glitches.ini"))
        script_path = os.path.normpath(os.path.join(getCurrentPath(), "..", "..", "..", "lisaglitch-1.3", "main_glitch.py"))
        self.showEditor(ini_path, script_path)
    def h5ViewerClicked(self):
        self.H5ViewerWindow = H5ViewerWindow()
        self.H5ViewerWindow.show()
    def instrumentClicked(self):
        ini_path = os.path.normpath(os.path.join(getCurrentPath(), "..","..","..","testsInstrument","instrument.ini"))
        script_path = os.path.normpath(os.path.join(getCurrentPath(), "..","..","..","testsInstrument","main_instrument.py"))
        self.showEditor(ini_path, script_path)
    def showEditor(self, ini_path, script_path):
        self.iniEditor = TextEditView(ini_path)
        self.iniEditor.show()
        self.currentScript = script_path
        self.iniEditor.runClicked.connect(self.run_subprocess)
        if self.iniEditor.exec_() == QDialog.Accepted:
            print("文件已成功保存")
    def run_subprocess(self):
        print(f'启动子进程: {self.currentScript}')
        script_cwd = os.path.dirname(os.path.abspath(self.currentScript))
        # 跨平台参数配置
        kwargs = {
            'stdin': subprocess.DEVNULL,
            'stdout': None,
            'stderr': None,
            'cwd': script_cwd,
        }

        if sys.platform == 'win32':
            # Windows平台
            kwargs.update({
                'creationflags': subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                'close_fds': False,  # Windows不支持close_fds
            })
        else:
            # Unix平台（Linux/macOS）
            kwargs.update({
                'start_new_session': True,
                'close_fds': True,
            })

        try:
            # 使用当前Python解释器路径
            child_proc = subprocess.Popen(
                [sys.executable, self.currentScript],
                **kwargs
            )

            # 创建监控线程
            def monitor_thread():
                child_proc.wait()
                # 通过线程安全的方式更新UI
                self.on_process_finished()
            threading.Thread(target=monitor_thread, daemon=True).start()

        except Exception as e:
            print(f"启动子进程失败: {str(e)}")

    def on_process_finished(self):
        self.iniEditor.save_btn.setEnabled(True)
        self.iniEditor.run_btn.setEnabled(True)
        self.iniEditor.run_btn.setText("再次运行")
    # def resizeEvent(self, event):
    #     self.updateBackground()
    #     super().resizeEvent(event)