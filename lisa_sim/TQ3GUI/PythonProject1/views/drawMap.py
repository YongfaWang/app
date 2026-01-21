import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QLabel,
                             QMessageBox)


class SelectionDialog(QDialog):
    def __init__(self, parent=None, dataset=None):
        super().__init__(parent)
        self.dataset = dataset
        self.setWindowTitle("选择")
        self.setMinimumWidth(300)
        if len(self.dataset.shape) <= 1 and self.dataset.dtype.names is None:
            self.dataset_size = (self.dataset.shape[0], 1)
        elif len(self.dataset.shape) <= 1:
            self.dataset_size = (self.dataset.shape[0], len(self.dataset.dtype.names))
        else:
            self.dataset_size = (self.dataset.shape[0], self.dataset.shape[1])
        self.dataset_size_label = QLabel(f'{self.dataset_size[0]}*{self.dataset_size[1]}')
        self.dataset_size_label.setAlignment(Qt.AlignCenter)
        # 将字体设置为微软雅黑
        self.dataset_size_label.setFont(QFont("Arial", 10, QFont.Bold))
        # 标签
        self.row_label = QLabel("指定行索引")
        self.col_label = QLabel("指定列索引")
        self.row_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.col_label.setFont(QFont("Arial", 10, QFont.Bold))
        # 编辑框
        self.row_input = QLineEdit()
        self.col_input = QLineEdit()
        self.row_input.setPlaceholderText(f"示例: 500-{self.dataset.shape[0]}")
        self.col_input.setPlaceholderText(f"示例: 1-{self.dataset.shape[1]}")
        self.col_input.setClearButtonEnabled(True)
        self.row_input.setClearButtonEnabled(True)
        self.confirm_btn = QPushButton("绘图")

        # 布局设置
        layout = QVBoxLayout()
        layout.addWidget(self.dataset_size_label)
        layout.addWidget(self.row_label)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.row_input)
        input_layout.setContentsMargins(20, 0, 0, 0)  # 左缩进
        layout.addLayout(input_layout)
        layout.addWidget(self.col_label)
        # 输入字段组

        input_layout1 = QVBoxLayout()
        input_layout1.addWidget(self.col_input)
        input_layout1.setContentsMargins(20, 0, 0, 0)  # 左缩进
        layout.addLayout(input_layout1)

        input_layout2 = QVBoxLayout()
        # input_layout2.addWidget(self.custom_input)
        input_layout2.setContentsMargins(20, 0, 0, 0)  # 左缩进
        layout.addLayout(input_layout2)

        # 按钮组
        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.confirm_btn, alignment=Qt.AlignRight)
        layout.addItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addLayout(btn_layout)

        # 信号连接
        # self.col_radio.toggled.connect(self.specify_toggled)
        # self.row_radio.toggled.connect(self.round_toggled)
        # self.diy_radio.toggled.connect(self.diy_toggled)
        self.confirm_btn.clicked.connect(self.applyBtnClicked)

        # 设置样式
        self.setStyleSheet("""
            QDialog { background: #f5f5f5; }
            QRadioButton { 
                spacing: 8px;
                font: 14px 'Microsoft YaHei';
                padding: 5px 0;
            }
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 5px;
            }
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

        self.setLayout(layout)

    def applyBtnClicked(self):
        old_row_index = ''
        old_col_index = ''
        """确认按钮点击事件"""
        old_row_index = self.row_input.text()
        old_col_index = self.col_input.text()
        if self.row_input.text() == '':
            old_row_index = self.row_input.placeholderText().replace('示例: ', '')
        if self.col_input.text() == '':
            old_col_index = f'1-{self.dataset_size[1]}'
        validate_status, msg = self.validate_row_input(old_row_index)
        if not validate_status:
            QMessageBox.warning(self, "警告", f"{msg}")
            return
        validate_status, msg = self.validate_row_input(old_col_index)
        if not validate_status:
            QMessageBox.warning(self, "警告", f"{msg}")
            return
        self.new_row_index = self.parse_index_str(old_row_index, True)
        self.new_col_index = self.parse_index_str(old_col_index)
        for item in self.new_row_index:
            if item > self.dataset_size[0]:
                QMessageBox.warning(self, "警告", f"行索引超出范围, 请重新输入！")
                return
            if item <= 0:
                QMessageBox.warning(self, "警告", f"行索引应从 1 开始, 请重新输入！")
                return
        for item in self.new_col_index:
            if item > self.dataset_size[1]:
                QMessageBox.warning(self, "警告", f"列索引超出范围, 请重新输入！")
                return
            if item <= 0:
                QMessageBox.warning(self, "警告", f"列索引应从 1 开始, 请重新输入！")
                return
        self.accept()

    # Flag表示是否为行
    def round_toggled(self, checked):
        """控制输入框可用状态"""
        self.row_input.setEnabled(checked)

    def parse_index_str(self, s, flag=False):
        index_list = []
        parts = s.split(',')
        for part in parts:
            part = part.strip()
            if re.match(r'^\d+$', part):  # 单个数字
                index_list.append(int(part))
            elif re.match(r'^\d+-\d+$', part):  # 范围
                start, end = map(int, part.split('-'))
                if start > end:
                    raise ValueError(f"范围起始值大于结束值：{part}")
                index_list.extend(range(start, end + 1))
            else:
                raise ValueError(f"非法格式：{part}")
        return index_list

    def specify_toggled(self, checked):
        """控制输入框可用状态"""
        self.col_input.setEnabled(checked)

    # def diy_toggled(self, checked):
    #     """控制输入框可用状态"""
    #     self.custom_input.setEnabled(checked)

    # def set_total_count(self, count):
    #     """设置总数显示（动态更新用）"""
    #     self.all_radio.setText(f"全部 ({count})")
    def validate_unique_numbers(self, text):
        numbers = text.split(',')
        return len(numbers) == len(set(numbers))  # 通过集合去重判断

    def validate_unique_numbers_size(self, text):
        numbers = text.split(',')
        for number in numbers:
            if int(number) >= self.dataset.shape[1]:
                return False
        return True

    def get_selection(self):
        """获取用户选择结果"""
        return self.new_row_index, self.new_col_index


    def validate_row_input(self, input_str):
        # 定义数字有效性正则表达式（不允许前导零）
        number_pattern = re.compile(r'^[1-9]\d*$')

        # 检查是否包含空格
        if ' ' in input_str:
            return False, "输入中不能包含空格"

        # 分割输入字符串
        elements = input_str.split(',')

        # 检查空输入或空元素
        # if not elements:
        #     return False, "输入不能为空"
        if any(not element for element in elements):
            return False, "存在空的元素（多个逗号）"

        for element in elements:
            # 检查范围格式
            if '-' in element:
                parts = element.split('-')
                # 验证范围格式
                if len(parts) != 2:
                    return False, f"无效范围格式: {element}"
                start, end = parts

                # 验证数字有效性
                for num in [start, end]:
                    if not number_pattern.match(num):
                        return False, f"无效数字: {num}"

                # 转换为数字比较范围
                if int(start) > int(end):
                    return False, f"范围错误: {element}（起始值大于结束值）"

            # 检查单个数字
            else:
                if not number_pattern.match(element):
                    return False, f"无效数字: {element}"

        return True, ""