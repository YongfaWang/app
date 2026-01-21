import csv
import os

import h5py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QAction
from PyQt5.QtCore import Qt, QSize
import pandas as pd
import numpy as np

from views.TestPlot import TestPlotWindow
from views.drawMap import SelectionDialog
from views.lineMap import LineMap


class ResList(QWidget):
    def __init__(self, h5_path=None, parent=None):
        super().__init__(parent)
        self.fs = None
        self.h5_path = h5_path
        self.current_path = []  # 用于记录当前层级路径（栈结构）
        self.list_widget = QListWidget()
        self.init_ui()
        self.setStyleSheet("""
                    QListWidget::Item {
                        background: #EEEEEE;
                        color: black;
                        padding: 5px 0px;
                        /** padding: 8px 20px; **/
                        /** min-width: 80px; **/
                        /** border-radius: 4px; **/
                    }
                    QListWidget::Item:hover { background: #CCCCCC; }
                    QListWidget::Item:pressed { background: #AAAAAA; }
                    QListWidget::Item:selected { background: #AAAAAA; }
                        """)

        self.return_action1 = QAction("返回上一级", self)
        self.return_action1.setShortcut("Alt+UP")
        self.return_action1.triggered.connect(self.return_parent)
        self.addAction(self.return_action1)
        self.return_action2 = QAction("返回上一级", self)
        self.return_action2.setShortcut("Backspace")
        self.return_action2.triggered.connect(self.return_parent)
        self.addAction(self.return_action2)
        if h5_path:
            self.load_h5_structure()

    def init_ui(self):
        # 设置自适应布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.list_widget.setSizeAdjustPolicy(QListWidget.AdjustToContents)
        self.list_widget.itemDoubleClicked.connect(self.on_item_Doubleclicked)
        self.list_widget.itemClicked.connect(self.on_item_clicked)

    def load_h5_structure(self, h5_path=None):
        # 修改代码时要注意h5_path的传递,一个是传入的h5_path，一个是类属性的h5_path
        if h5_path:
            self.h5_path = h5_path
            self.current_path = []  # 每次打开h5文件时，重置当前路径
        # 加载当前路径下的组和数据集
        self.list_widget.clear()
        with h5py.File(self.h5_path, 'r') as h5_file:
            self.fs = h5_file.attrs['fs']
            # 添加返回上一级项（非根目录时显示）
            if len(self.current_path) > 0:
                item = QListWidgetItem("← 返回上一级")
                item.setData(Qt.UserRole, ("back", None))
                self.list_widget.addItem(item)

            # 获取当前层级对象
            current_obj = h5_file
            for key in self.current_path:
                current_obj = current_obj[key]

            # 遍历子项
            for name in current_obj:
                obj = current_obj[name]
                item = QListWidgetItem()
                if isinstance(obj, h5py.Group):
                    item.setText(f"📁 {name} (组)")
                    item.setData(Qt.UserRole, ("group", name))
                else:
                    if obj.ndim > 2:
                        obj = np.array(obj)
                        obj = obj.reshape(obj.shape[0], -1)
                    if len(obj.shape) <= 1 and obj.dtype.names is None:
                        item.setText(f"📄 {name} (数据集) 数据集大小:{obj.shape[0]}*1")
                    elif len(obj.shape) <= 1:
                        item.setText(f"📄 {name} (数据集) 数据集大小:{obj.shape[0]}*{len(obj.dtype.names)}")
                    else:
                        item.setText(f"📄 {name} (数据集) 数据集大小:{obj.shape[0]}*{obj.shape[1]}")
                    item.setData(Qt.UserRole, ("dataset", name))
                self.list_widget.addItem(item)
    def reduce_dim(self, dataset):
        # 假设 dataset 是 NumPy 数组
        if hasattr(dataset, 'ndim'):  # 确保是类似数组的结构
            if dataset.ndim > 2:
                # 保持第一维，后续维度展平到第二维
                dataset = dataset.reshape(dataset.shape[0], -1)
        else:
            # 如果 dataset 不是数组结构，先转换为 NumPy 数组再处理
            dataset = np.array(dataset)
            if dataset.ndim > 2:
                dataset = dataset.reshape(dataset.shape[0], -1)
        return dataset
    def on_item_Doubleclicked(self, item):
        # 处理点击事件
        obj_type, name = item.data(Qt.UserRole)
        dataset = None
        if obj_type == "back":
            if self.current_path:
                self.current_path.pop()
                self.load_h5_structure()
        elif obj_type == "group":
            self.current_path.append(name)
            self.load_h5_structure()
        elif obj_type == "dataset":
            dataset_dtype = None
            obj_type, name = item.data(Qt.UserRole)
            with h5py.File(self.h5_path, 'r') as h5_file:
                current_obj = h5_file
                for key in self.current_path:
                    current_obj = current_obj[key]
                    dataset = current_obj[name][()]  # 获取数据集数值
                if len(self.current_path) == 0:
                    dataset = current_obj[name][()]  # 获取数据集数值 根目录
                if len(dataset.shape) <= 1:
                    # 这个判断临时解决bug使用 不作为最优代码, 用于将shape(40000,)转换为shape(40000,1), else是最优代码, 用于设置[(1,2,3),(4,5,6),(7,8,9)]转换为[[1,2,3],[4,5,6],[7,8,9]]
                    if dataset.dtype.names is None:
                        dataset = dataset.reshape(-1, 1)
                    else:
                        dataset_dtype = dataset.dtype
                        dataset = np.array(dataset.tolist())
                # 创建弹窗

                # if len(dataset.shape) <= 1:
                #     dataset.reshape(len(dataset.dtype), -1)
                dataset = self.reduce_dim(dataset)
                dialog = SelectionDialog(dataset=dataset)
                if dialog.exec_():
                    result = dialog.get_selection()
                    print("用户选择：", result) # 初始化组件
                    self.plotter = LineMap(dataset_dtype=dataset_dtype)
                    self.plotter.resize(800, 600)
                    result[0].pop()
                    for i, fruit in enumerate(result[0]):
                        result[0][i] -= 1
                    for i, fruit in enumerate(result[1]):
                        result[1][i] -= 1
                    self.plotter.plot_data(dataset, result[0], result[1], yLabels=name)
                    self.plotter.show()
                    self.tpw = TestPlotWindow(data=dataset, fs=self.fs, dataset_dtype=dataset_dtype, rows=result[0], cols=result[1])
                    self.tpw.show()


    def on_item_clicked(self, item):
        # 处理点击事件
        obj_type, name = item.data(Qt.UserRole)
        if obj_type == "dataset":
            with h5py.File(self.h5_path, 'r') as h5_file:
                current_obj = h5_file
                for key in self.current_path:
                    current_obj = current_obj[key]
                dataset = current_obj[name]
                # 获取数据集属性
                info = {
                    "Path": dataset.name,
                    "Shape": dataset.shape,
                    "Dtype": dataset.dtype,
                    "Compression": dataset.compression
                }
                # print("Dataset Info:", info)  # 或传递到UI控件
                # print(dataset[...])

            # self.export_dataset_item_csv(item)
        elif obj_type == "group":
            with h5py.File(self.h5_path, 'r') as h5_file:
                current_obj = h5_file
                for key in self.current_path:
                    current_obj = current_obj[key]
                group = current_obj[name]
                # 获取组子项
                subgroups = []
                datasets = []
                for key in group.keys():
                    if isinstance(group[key], h5py.Group):
                        subgroups.append(key)
                    else:
                        datasets.append(key)
                print(f"Group '{name}': Subgroups={subgroups}, Datasets={datasets}")
    def return_parent(self):
        # 返回上一级
        if len(self.current_path) > 0:
            self.current_path.pop()
            self.load_h5_structure()
    def display_dataset_info(self, dataset):
        info = {
            "名称": dataset.name,  # 完整路径（如"/group1/data1"）
            "形状": dataset.shape,  # 数据维度（如(100, 200)）
            "数据类型": dataset.dataset_dtype,  # 数据类型（如float32）
            "压缩方式": dataset.compression  # 压缩算法（如'gzip'）
        }
        # 可选：读取数据（注意大数据可能导致性能问题）
        if dataset.size < 1e4:  # 限制数据量
            data = dataset[()]
        # 将info显示到UI组件（如QTableWidget或QTextEdit）

    def display_group_info(self, group):
        children = {
            "子组": [],
            "数据集": []
        }
        for key in group.keys():
            obj = group[key]
            if isinstance(obj, h5py.Group):
                children["子组"].append(key)
            else:
                children["数据集"].append(key)
        # 将children显示到UI组件

    def sizeHint(self):
        # 自适应宽高（根据内容调整）
        return QSize(400, 300)

    def delete_dataset_item(self, item):
        # 删除数据集项
        obj_type, name = item.data(Qt.UserRole)
        if obj_type == "dataset":
            with h5py.File(self.h5_path, 'r+') as h5_file:
                current_obj = h5_file
                for key in self.current_path:
                    current_obj = current_obj[key]
                    del current_obj[name]
                    self.load_h5_structure()

    def delete_group_item(self, item):
        # 删除组项
        obj_type, name = item.data(Qt.UserRole)
        if obj_type == "group":
            with h5py.File(self.h5_path, 'r+') as h5_file:
                current_obj = h5_file
                for key in self.current_path:
                    current_obj = current_obj[key]
                    del current_obj[name]
                    self.load_h5_structure()

    def copy_dataset_item(self, item):
        # 复制数据集项
        obj_type, name = item.data(Qt.UserRole)
        if obj_type == "dataset":
            with h5py.File(self.h5_path, 'r+') as h5_file:
                current_obj = h5_file
                for key in self.current_path:
                    current_obj = current_obj[key]
                    dataset = current_obj[name]
                    # 复制数据集
                    new_dataset = current_obj.create_dataset(
                        name + "_copy", dataset.shape, dtype=dataset.dataset_dtype)
                    new_dataset[...] = dataset[...]
                    self.load_h5_structure()

    def copy_group_item(self, item):
        # 复制组项
        obj_type, name = item.data(Qt.UserRole)
        if obj_type == "group":
            with h5py.File(self.h5_path, 'r+') as h5_file:
                current_obj = h5_file
                for key in self.current_path:
                    current_obj = current_obj[key]
                    group = current_obj[name]
                    # 复制组
                    new_group = current_obj.create_group(name + "_copy")
                    # 复制子项
                    for key in group.keys():
                        obj = group[key]
                        if isinstance(obj, h5py.Group):
                            new_group.create_group(key)
                        else:
                            new_group.create_dataset(key, obj.shape, dtype=obj.dataset_dtype)
                            new_group[key][...] = obj[...]
                        self.load_h5_structure()

    def exprot_dataset_item_h5(self, item):
        # 导出数据集项
        obj_type, name = item.data(Qt.UserRole)
        if obj_type == "dataset":
            with h5py.File(self.h5_path, 'r+') as h5_file:
                current_obj = h5_file
                for key in self.current_path:
                    current_obj = current_obj[key]
                    dataset = current_obj[name]
                    # 导出数据集
                    dataset.export(name + ".h5", name + "_export")
                    self.load_h5_structure()

    def export_dataset_item_csv(self, item):
        obj_type, name = item.data(Qt.UserRole)
        if obj_type == "dataset":
            with h5py.File(self.h5_path, 'r') as h5_file:
                current_obj = h5_file
                for key in self.current_path:
                    current_obj = current_obj[key]
                    dataset = current_obj[name][()]  # 获取数据集数值

                # 强制转换为文本类型并禁用科学计数法
                df = pd.DataFrame(np.array(dataset)).astype(str)  # 全部转为文本类型[4,7](@ref)

                # 保存为CSV
                try:
                    # 设置float_format防止数值自动转换科学计数法
                    df.to_csv(f"{os.path.dirname(self.h5_path)}\\{name}.csv",
                              index=False,
                              float_format='%.0f',  # 整数格式强制不显示小数
                              quoting=csv.QUOTE_NONNUMERIC,  # 非数值字段加引号[6](@ref)
                              encoding='utf-8-sig')  # 支持中文
                    print(f"成功保存到{name}.csv")
                except PermissionError:
                    print("错误：文件被占用或没有写入权限")
                except Exception as e:
                    print(f"保存失败：{str(e)}")
