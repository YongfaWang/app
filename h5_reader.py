import h5py
import numpy as np
import json
import sys
import os
from typing import Dict, Any, List, Optional

class H5Reader:
    def __init__(self):
        self.file_handles = {}
    
    def check_file_exists(self, file_path: str) -> bool:
        """检查文件是否存在"""
        return os.path.exists(file_path)
    
    def get_file_structure(self, file_path: str) -> Dict[str, Any]:
        """递归读取 HDF5 文件结构"""
        if not self.check_file_exists(file_path):
            return {"error": f"文件不存在: {file_path}"}
        
        try:
            with h5py.File(file_path, 'r') as f:
                return self._traverse_group(f, '/')
        except Exception as e:
            return {"error": f"读取文件失败: {str(e)}"}
    
    def _traverse_group(self, group: h5py.Group, path: str) -> Dict[str, Any]:
        """递归遍历 HDF5 组"""
        result = {
            "name": path.split('/')[-1] or '/',
            "path": path,
            "type": "group",
            "children": []
        }
        
        for key in group.keys():
            item = group[key]
            item_path = f"{path}/{key}" if path != '/' else f"/{key}"
            
            if isinstance(item, h5py.Group):
                # 递归处理子组
                child_result = self._traverse_group(item, item_path)
                result["children"].append(child_result)
            elif isinstance(item, h5py.Dataset):
                # 处理数据集
                dataset_info = {
                    "name": key,
                    "path": item_path,
                    "type": "dataset",
                    "shape": item.shape,
                    "dtype": str(item.dtype),
                    "attributes": self._get_attributes(item)
                }
                result["children"].append(dataset_info)
        
        result["attributes"] = self._get_attributes(group)
        return result
    
    def _get_attributes(self, obj) -> Dict[str, Any]:
        """获取对象的属性"""
        attrs = {}
        for attr_name in obj.attrs:
            try:
                attr_value = obj.attrs[attr_name]
                # 将 numpy 类型转换为 Python 原生类型
                if hasattr(attr_value, 'tolist'):
                    attr_value = attr_value.tolist()
                elif isinstance(attr_value, (np.number, np.bool_)):
                    attr_value = attr_value.item()
                attrs[attr_name] = attr_value
            except Exception:
                attrs[attr_name] = f"无法读取属性: {attr_name}"
        return attrs
    
    def read_dataset(self, file_path: str, dataset_path: str, 
                    max_size: int = 1000000) -> Dict[str, Any]:
        """读取指定数据集的数据"""
        if not self.check_file_exists(file_path):
            return {"error": f"文件不存在: {file_path}"}
        
        try:
            with h5py.File(file_path, 'r') as f:
                if dataset_path not in f:
                    return {"error": f"数据集不存在: {dataset_path}"}
                
                dataset = f[dataset_path]
                if not isinstance(dataset, h5py.Dataset):
                    return {"error": f"路径不是数据集: {dataset_path}"}
                
                # 检查数据集大小，避免读取过大文件
                dataset_size = np.prod(dataset.shape) * dataset.dtype.itemsize
                if dataset_size > max_size:
                    return {
                        "error": f"数据集过大 ({dataset_size} bytes)，最大支持 {max_size} bytes",
                        "shape": dataset.shape,
                        "dtype": str(dataset.dtype)
                    }
                
                # 读取数据
                data = dataset[()]
                
                # 转换数据为可序列化的格式
                if hasattr(data, 'tolist'):
                    data = data.tolist()
                elif isinstance(data, np.ndarray):
                    data = data.tolist()
                elif isinstance(data, (np.number, np.bool_)):
                    data = data.item()
                
                return {
                    "path": dataset_path,
                    "shape": dataset.shape,
                    "dtype": str(dataset.dtype),
                    "data": data,
                    "attributes": self._get_attributes(dataset)
                }
                
        except Exception as e:
            return {"error": f"读取数据集失败: {str(e)}"}

def main():
    """命令行接口，用于测试"""
    if len(sys.argv) < 3:
        print("用法: python h5_reader.py <command> <file_path> [dataset_path]")
        print("命令: structure, dataset")
        return
    
    command = sys.argv[1]
    file_path = sys.argv[2]
    dataset_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    reader = H5Reader()
    
    if command == "structure":
        result = reader.get_file_structure(file_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif command == "dataset" and dataset_path:
        result = reader.read_dataset(file_path, dataset_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("无效的命令或参数")

if __name__ == "__main__":
    main()