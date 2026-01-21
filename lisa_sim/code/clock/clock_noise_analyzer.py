"""
clock_noise_analyzer.py - 时钟噪声分析工具模块

功能：
1. 基于Allan方差测量数据估计噪声参数
2. 噪声类型分析（白相位、白频率、闪烁、随机游走）
3. 结果可视化
4. 功率谱密度(PSD)计算
5，生成噪声时间序列

"""

import numpy as np
from typing import Tuple, Dict
from scipy.optimize import least_squares
from scipy.linalg import lstsq
from scipy.signal import fftconvolve

# 常量定义
NOISE_TYPES = ['white_phase', 'white_frequency', 'flicker_frequency', 'random_walk']
DEFAULT_SCALING = {
    'white_phase': 0.1,
    'random_walk_ref_tau': 1000.0
}


def calculate_allan_deviation(tau: np.ndarray, params: np.ndarray) -> np.ndarray:
    """
    计算Allan方差模型

    参数:
        tau: 积分时间数组(秒)
        params: 噪声参数数组 [A_wp, A_wf, A_ff, A_rw]

    返回:
        Allan标准差数组
    """
    A_wp, A_wf, A_ff, A_rw = params
    tau_arr = np.array(tau)  # 将输入列表转换为numpy数组
    return np.sqrt(
        (A_wp ** 2 / tau_arr ** 2) +  # 白相位噪声
        (A_wf ** 2 / tau_arr) +  # 白频率噪声
        (A_ff ** 2) +  # 闪烁噪声
        (A_rw ** 2 * tau_arr)  # 随机游走噪声
    )


def estimate_initial_parameters(adev_measured: np.ndarray) -> np.ndarray:
    """
    基于测量数据估算初始噪声参数

    参数:
        adev_measured: 测量的Allan标准差数组

    返回:
        初始参数估计数组 [A_wp, A_wf, A_ff, A_rw]
    """
    return np.array([
        adev_measured[0] * DEFAULT_SCALING['white_phase'],  # 相位白
        adev_measured[1],  # 频率白
        adev_measured[2],  # 闪烁
        adev_measured[-1] / np.sqrt(DEFAULT_SCALING['random_walk_ref_tau'])  # 随机游走
    ])


def fit_noise_parameters(tau: np.ndarray,
                         adev: np.ndarray,
                         method: str = 'lm') -> Dict[str, float]:
    """
    拟合噪声参数

    参数:
        tau: 积分时间数组(秒)
        adev: 测量的Allan标准差数组
        method: 拟合方法 ('lm'或'linear')

    返回:
        噪声参数字典 {'white_phase': A_wp, ...}
    """
    if method == 'lm':
        # Levenberg-Marquardt非线性拟合
        initial_guess = estimate_initial_parameters(adev)
        res = least_squares(
            lambda p, x, y: (calculate_allan_deviation(x, p) - y) / y,
            initial_guess,
            args=(tau, adev),
            method='lm'
        )
        params = res.x
    else:
        # 线性最小二乘拟合
        H = np.vstack([
            1 / tau ** 2,
            1 / tau,
            np.ones_like(tau),
            tau
        ]).T
        params, _, _, _ = lstsq(H, adev ** 2)
        params = np.sqrt(np.maximum(params, 0))

    return dict(zip(NOISE_TYPES, params))


def calculate_psd(tau: np.ndarray,
                  params: Dict[str, float]) -> Dict[str, np.ndarray]:
    """
    计算功率谱密度(PSD)

    参数:
        tau: 积分时间数组(秒)
        params: 噪声参数字典

    返回:
        包含各噪声PSD的字典 {
            'frequency': 频率数组,
            'total': 总PSD,
            'components': 各噪声分量PSD
        }
    """
    f = 1 / np.array(tau)  # 将tau转换为numpy数组以支持向量化操作
    A_wp = params['white_phase']
    A_wf = params['white_frequency']
    A_ff = params['flicker_frequency']
    A_rw = params['random_walk']

    components = {
        'white_phase': ((A_wp ** 2 * (2 * np.pi) ** 2) / 3) * f ** 2,
        'white_frequency': A_wf ** 2 * 2,
        'flicker_frequency': (A_ff ** 2 / 2 * np.log(2)) / f,
        'random_walk': (A_rw ** 2 * 6) / (2 * np.pi * f) ** 2
    }

    return {
        'frequency': f,
        'total': sum(components.values()),
        'components': components
    }


def analyze_clock_noise(tau: np.ndarray,
                        adev: np.ndarray,
                        method: str = 'lm') -> Dict:
    """
    完整的时钟噪声分析流程

    参数:
        tau: 积分时间数组(秒)
        adev: 测量的Allan标准差数组
        method: 拟合方法 ('lm'或'linear')

    返回:
        分析结果字典 {
            'params': 噪声参数,
            'psd': PSD分析结果,
            'fitted_adev': 拟合的Allan偏差
        }
    """
    params = fit_noise_parameters(tau, adev, method)
    psd = calculate_psd(tau, params)

    return {
        'params': params,
        'psd': psd,
        'fitted_adev': calculate_allan_deviation(tau, list(params.values()))
    }

class ClockErrorGenerator:
    """时钟误差生成器类，用于生成不同类型的时钟噪声序列"""

    def __init__(self, tau_s: float, f_h: float = 1.0):
        """
        初始化时钟误差生成器

        参数:
            tau_s: 采样间隔时间（单位：秒）
            f_h: 高频截止频率（单位：Hz）
        """
        self.tau_s = tau_s
        self.f_h = f_h

    def get_noise_parameters(self, tau: np.ndarray, adev: np.ndarray) -> Dict[str, float]:
        """
        获取噪声参数A值

        参数:
            tau: 积分时间数组(秒)
            adev: 测量的Allan标准差数组

        返回:
            噪声参数字典 {'A_wp': ..., 'A_wf': ..., 'A_ff': ..., 'A_rw': ...}
        """
        params = fit_noise_parameters(tau, adev)
        return {
            'A_wp': params['white_phase'],
            'A_wf': params['white_frequency'],
            'A_ff': params['flicker_frequency'],
            'A_rw': params['random_walk']
        }

    def white_phase_noise(self, A_wp: float, N: int) -> np.ndarray:
        """
        生成白相位噪声序列

        参数:
            A_wp: 白相位噪声幅度系数
            N: 生成噪声序列长度

        返回:
            白相位噪声序列（一维数组）
        """
        rand = np.random.uniform(-1, 1, N)
        y = A_wp * np.sqrt(self.f_h / self.tau_s ** 2) * (rand[1:] - rand[:-1])
        return np.pad(y, (1, 0), 'constant')

    def white_frequency_noise(self, A_wf: float, N: int) -> np.ndarray:
        """
        生成白频率噪声序列

        参数:
            A_wf: 白频率噪声幅度系数
            N: 生成噪声序列长度

        返回:
            白频率噪声序列（一维数组）
        """
        rand = np.random.uniform(-1, 1, N)
        return A_wf * np.sqrt(1 / self.tau_s) * np.sqrt(3) * rand

    def random_walk_noise(self, A_rw: float, N: int) -> np.ndarray:
        """
        生成随机游走噪声序列

        参数:
            A_rw: 随机游走噪声幅度系数
            N: 生成噪声序列长度

        返回:
            随机游走噪声序列（一维数组）
        """
        rand = np.random.uniform(-1, 1, N)
        return np.cumsum(A_rw * np.sqrt(self.tau_s) * 3 * rand)

    def flicker_frequency_noise(self, A_ff: float, N: int) -> np.ndarray:
        """
        生成闪烁频率噪声序列（1/f噪声）

        参数:
            A_ff: 闪烁噪声幅度系数
            N: 生成噪声序列长度

        返回:
            闪烁频率噪声序列（一维数组）
        """
        n = int(np.log2(N)) + 1
        M = 2 ** n
        weights = np.arange(1, M + 1) ** (-2 / 3)
        weights /= np.sqrt(np.sum(weights ** 2))
        white_noise = np.random.uniform(-1, 1, M)
        conv = fftconvolve(white_noise, weights, mode='full')[:M]
        return A_ff * np.sqrt(5) * conv[:N] * np.sqrt(12)

    def generate_clock_errors(self, params: Dict[str, float], N: int) -> Tuple[np.ndarray, np.ndarray, Dict[str, np.ndarray]]:
        """
        生成综合时钟误差（时间偏差序列）

        参数:
            params: 噪声参数字典，包含A_wp, A_wf, A_ff, A_rw四个键
            N: 生成序列长度

        返回:
            (频率偏差总和, 时间偏差序列, 各噪声分量字典)
        """
        components = {
            'wp': self.white_phase_noise(params['A_wp'], N),
            'wf': self.white_frequency_noise(params['A_wf'], N),
            'ff': self.flicker_frequency_noise(params['A_ff'], N),
            'rw': self.random_walk_noise(params['A_rw'], N)
        }
        y_total = sum(components.values())
        x = np.cumsum(y_total) * self.tau_s
        return y_total, x, components

# 示例用法
if __name__ == '__main__':
    tau = [0.1, 1, 10, 100, 1000]
    adev = [1.6E-13, 7E-14, 7.1E-14, 8E-14, 2.6E-13]

    # 分析时钟噪声
    results = analyze_clock_noise(tau, adev)
    print("噪声参数:", results['params'])

    # 生成时钟误差序列
    generator = ClockErrorGenerator(tau_s=1.0)
    params = generator.get_noise_parameters(tau, adev)
    y_total, x_total, components = generator.generate_clock_errors(params, N=1000)


