import scipy.signal as signal

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class TestPlotWindow(QWidget):
    def __init__(self, data, fs, rows, cols, parent=None, dataset_dtype=None):
        super().__init__(parent)
        self.dataset_dtype = dataset_dtype
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        # 使用真实数据并确保为一维数组
        # data1 = data.flatten()
        self.ax.clear()
        colors = plt.cm.viridis(np.linspace(0, 1, len(cols)))
        for idx, col in enumerate(cols):
            data1 = data[:, col]
            nfft = len(data1)
            window = np.hanning(nfft)  # 显式创建窗口
            # 均值校正
            data_mean_corrected = data1 - np.mean(data1)
            # 执行Periodogram分析（明确传递窗口参数）
            f1, Pxx1 = signal.periodogram(
                data_mean_corrected,
                window=window,  # 传递numpy数组
                nfft=nfft,
                fs=fs,
                return_onesided=True
            )
            if self.dataset_dtype is None:
                self.ax.loglog(f1, Pxx1, label=f'{idx + 1}', color=colors[idx])
            else:
                self.ax.loglog(f1, Pxx1, label=f'{self.dataset_dtype.names[col]}', color=colors[idx])
        self.ax.legend(loc='upper right',
                       bbox_to_anchor=(1.15, 1),
                       frameon=False)
        self.ax.set_xlabel('Frequency (Hz)')
        self.ax.set_ylabel('Power Spectral Density')
        self.ax.set_title(f'PSD with {fs}Hz Sampling Rate')
        # self.ax.set_xlim(0, 100)  # 显示0-100Hz范围
        self.ax.grid(True)
        self.canvas.draw()
    # def update_style(self, style_name='seaborn'):
    #     """动态更新样式（网页6样式表示例）"""
    #     plt.style.use(style_name)
    #     self.canvas.draw()
