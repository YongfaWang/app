import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import ScalarFormatter


class LineMap(QWidget):
    def __init__(self, parent=None, dataset_dtype=None):
        super().__init__(parent)
        self.dataset_dtype = dataset_dtype
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.dataset = None

        # 设置保存和打印功能
        self.save_action = QAction("Save image", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_canvas)
        self.addAction(self.save_action)
        # 设置默认样式（网页4、网页6）
        plt.style.use('seaborn')
        # 鼠标左键拖拽事件
        self.lastx = 0  # 获取鼠标按下时的坐标X
        self.lasty = 0  # 获取鼠标按下时的坐标Y
        self.press = False
        # Alt键按下松开调用on_press on_release
        self.figure.canvas.mpl_connect("button_press_event", self.on_press)
        self.figure.canvas.mpl_connect("button_release_event", self.on_release)
        self.figure.canvas.mpl_connect("motion_notify_event", self.on_move)
        # 鼠标滚轮事件
        self.figure.canvas.mpl_connect('scroll_event', self.call_back)

    # ================ 鼠标滚轮放大缩小坐标 ================ #
    def call_back(self, event):
        axtemp = event.inaxes
        x_min, x_max = axtemp.get_xlim()
        y_min, y_max = axtemp.get_ylim()
        xfanwei = (x_max - x_min) / 10
        yfanwei = (y_max - y_min) / 10
        if event.button == 'up':
            axtemp.set(xlim=(x_min + xfanwei, x_max - xfanwei))
            axtemp.set(ylim=(y_min + yfanwei, y_max - yfanwei))
        elif event.button == 'down':
            axtemp.set(xlim=(x_min - xfanwei, x_max + xfanwei))
            axtemp.set(ylim=(y_min - yfanwei, y_max + yfanwei))
        self.figure.canvas.draw_idle()  # 绘图动作实时反映在图像上

    # ================ 鼠标左键拖拽坐标 ================ #
    def on_press(self, event):
        if event.inaxes:  # 判断鼠标是否在axes内
            if event.button == 1:  # 判断按下的是否为鼠标左键1（右键是3）
                self.press = True
                self.lastx = event.xdata  # 获取鼠标按下时的坐标X
                self.lasty = event.ydata  # 获取鼠标按下时的坐标Y

    def on_move(self, event):
        axtemp = event.inaxes
        if axtemp:
            if self.press:  # 按下状态
                # 计算新的坐标原点并移动
                # 获取当前最新鼠标坐标与按下时坐标的差值
                x = event.xdata - self.lastx
                y = event.ydata - self.lasty
                # 获取当前原点和最大点的4个位置
                x_min, x_max = axtemp.get_xlim()
                y_min, y_max = axtemp.get_ylim()

                x_min = x_min - x
                x_max = x_max - x
                y_min = y_min - y
                y_max = y_max - y

                axtemp.set_xlim(x_min, x_max)
                axtemp.set_ylim(y_min, y_max)
                self.figure.canvas.draw()  # 绘图动作实时反映在图像上

    def on_release(self, event):
        if self.press:
            self.press = False  # 鼠标松开，结束移动

    def save_canvas(self):
        # 弹出保存对话框[3,5](@ref)
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存画布",
            "",
            "PNG 文件, 支持透明 (*.png);;JPG 文件 (*.jpg);;PDF 文件 (*.pdf)",
            options=options
        )

        if file_path:
            try:
                # 使用 matplotlib 保存画布[1,6](@ref)
                self.ax.figure.savefig(
                    file_path,
                    dpi=72,
                    bbox_inches='tight',
                    transparent=True
                )
                print(f"成功保存至：{file_path}", 5000)
            except Exception as e:
                print(f"保存失败：{str(e)}", 5000)

    def plot_data(self, dataset, rows, cols, yLabels):
        """核心绘图方法（参考网页4、网页5、网页6）"""
        self.dataset = dataset
        self.ax.clear()
        # 绘制各列数据
        colors = plt.cm.viridis(np.linspace(0, 1, len(cols)))
        for idx, col in enumerate(cols):
            if self.dataset_dtype is None:
                # self.ax.plot(dataset[rows, col],
                #              color=colors[idx],
                #              linestyle='-',
                #              linewidth=1.5,
                #              alpha=0.8,
                #              label=f'{col}')
                self.ax.plot(rows, dataset[rows, col],
                             color=colors[idx],
                             linestyle='-',
                             linewidth=1.5,
                             alpha=0.8,
                             label=f'{col + 1}')
            else:
                self.ax.plot(dataset[rows, col],
                             color=colors[idx],
                             linestyle='-',
                             linewidth=1.5,
                             alpha=0.8,
                             label=f'{self.dataset_dtype.names[col]}')
        # 设置图表元素
        self.ax.set_title(f"Data Visuali")
        self.ax.set_xlabel("Size")
        self.ax.set_ylabel(yLabels)
        # 添加鼠标滚轮缩放功能
        self.ax.legend(loc='upper right',
                       bbox_to_anchor=(1.15, 1),
                       frameon=False)

        self.canvas.draw()

    def _get_columns(self, mode, config):
        """获取目标列索引（处理三种模式逻辑）"""
        if mode == 'all':
            return range(self.dataset.shape[1])
        elif mode == 'specify':
            quantity = int(config.get('quantity', 0))
            return range(min(quantity, self.dataset.shape[1]))

        elif mode == 'custom':
            custom_str = config.get('custom', '')
            return [int(x.strip()) - 1 for x in custom_str.split(',') if x.strip().isdigit()]
        elif mode == 'round':
            round_str = config.get('custom', '')
            if int(round_str.split(',')[0]) < int(round_str.split(',')[1]) + 1:
                return range(int(round_str.split(',')[0]), int(round_str.split(',')[1]) + 1)
            return range(int(round_str.split(',')[1]), int(round_str.split(',')[0]) + 1)

        raise ValueError(f"未知模式: {mode}")

    def update_style(self, style_name='seaborn'):
        """动态更新样式（网页6样式表示例）"""
        plt.style.use(style_name)
        self.canvas.draw()
