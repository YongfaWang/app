import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt
from scipy.linalg import lstsq
from scipy.signal import fftconvolve
from sklearn.preprocessing import StandardScaler

# 设置显示中文字体（适用于Windows系统）
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 设置正常显示负号
matplotlib.rcParams['axes.unicode_minus'] = False


# ====================================================
# 论文章节：CLOCK ERRORS MODELLING & SIMULATION OF CLOCK ERRORS
# 实现时钟噪声生成器核心函数
# ====================================================
class ClockErrorGenerator:
    # 论文中按照tau_s=1.0仿真，实际程序中tau_s为变量
    # def __init__(self, tau_s=1.0, f_h=1.0):
    #     """
    #     初始化时钟误差生成器
    #     :param tau_s: 采样间隔时间（单位：秒）
    #     :param f_h: 高频截止频率（单位：Hz）
    #     """
    #     self.tau_s = tau_s  # 采样间隔（秒）
    #     self.f_h = f_h  # 高频截止频率
    def __init__(self, tau_s, f_h=1.0):
        """
        初始化时钟误差生成器
        :param tau_s: 采样间隔时间（单位：秒）
        :param f_h: 高频截止频率（单位：Hz）
        """
        self.tau_s = tau_s  # 采样间隔（秒）
        self.f_h = f_h  # 高频截止频率

    def white_phase_noise(self, A_wp, N):
        """
        生成白相位噪声（White Phase Noise）
        :param A_wp: 白相位噪声幅度系数
        :param N: 生成噪声序列长度
        :return: 白相位噪声序列（一维数组）
        """
        rand = np.random.uniform(-1, 1, N)
        # 通过差分运算生成高频噪声，符合白相位噪声的功率谱特性
        y = A_wp * np.sqrt(self.f_h / self.tau_s ** 2) * (rand[1:] - rand[:-1])
        z = np.pad(y, (1, 0), 'constant')
        return z  # 对齐时间索引

    def white_frequency_noise(self, A_wf, N):
        """
        生成白频率噪声（White Frequency Noise）
        :param A_wf: 白频率噪声幅度系数
        :param N: 生成噪声序列长度
        :return: 白频率噪声序列（一维数组）
        """
        rand = np.random.uniform(-1, 1, N)
        # 直接使用均匀分布生成，sqrt(3)用于调整均匀分布方差
        y = A_wf * np.sqrt(1 / self.tau_s) * np.sqrt(3) * rand
        return y

    def random_walk_noise(self, A_rw, N):
        """
        生成随机游走噪声（Random Walk Noise）
        :param A_rw: 随机游走噪声幅度系数
        :param N: 生成噪声序列长度
        :return: 随机游走噪声序列（一维数组）
        """
        rand = np.random.uniform(-1, 1, N)
        # 通过累积求和生成低频噪声，符合随机游走特性
        y = np.cumsum(A_rw * np.sqrt(self.tau_s) * 3 * rand)
        return y

    def flicker_frequency_noise(self, A_ff, N):
        """
        生成闪烁频率噪声（Flicker Frequency Noise，1/f噪声）
        使用FFT卷积法生成精确的1/f噪声
        :param A_ff: 闪烁噪声幅度系数
        :param N: 生成噪声序列长度
        :return: 闪烁频率噪声序列（一维数组）
        """
        # 计算最接近的2的幂次长度以提高FFT效率
        n = int(np.log2(N)) + 1
        M = 2 ** n
        # 构建功率谱衰减权重（符合1/f特性）
        weights = np.arange(1, M + 1) ** (-2 / 3)
        weights /= np.sqrt(np.sum(weights ** 2))  # 归一化
        # 生成白噪声并进行频谱卷积
        white_noise = np.random.uniform(-1, 1, M)
        conv = fftconvolve(white_noise, weights, mode='full')[:M]
        # 调整幅度和方差以匹配理论值
        return A_ff * np.sqrt(5) * conv[:N] * np.sqrt(12)  # 调整均匀分布方差

    def generate_clock_errors(self, params, N):
        """
        生成综合时钟误差（时间偏差序列）
        :param params: 噪声参数字典，包含A_wp, A_wf, A_ff, A_rw四个键, A对应不同噪声类型的一秒Allan偏差
        :param N: 生成序列长度
        :return: (总时间偏差序列, 各噪声分量字典)
        """
        # 生成各噪声分量
        components = {
            'wp': self.white_phase_noise(params['A_wp'], N),
            'wf': self.white_frequency_noise(params['A_wf'], N),
            'ff': self.flicker_frequency_noise(params['A_ff'], N),
            'rw': self.random_walk_noise(params['A_rw'], N)
        }
        # 叠加频率噪声分量并进行时间积分得到时间偏差
        y_total = sum(components.values())
        x = np.cumsum(y_total) * self.tau_s  # 积分公式：x(t) = ∫y(t)dt
        return y_total, x, components  # 四种噪声分量叠加是y_total,也是频率偏差的叠加
        # # 只使用闪烁频率噪声分量
        # y_total = components['ff']  # 直接使用闪烁频率噪声分量
        # x = np.cumsum(y_total) * self.tau_s  # 积分公式：x(t) = ∫y(t)dt
        # return y_total, x, components  # 返回频率偏差、时间偏差和所有噪声分量


# ====================================================
# 论文章节：SIMULATION RESULTS
# 实现Allan方差计算和可视化
# ====================================================
def allan_deviation(taus, x, tau_s):
    """
    计算Allan标准差（ADEV）
    :param taus: 积分时间数组（单位：秒）
    :param x: 时间偏差序列（单位：秒）
    :param tau_s: 采样间隔时间（单位：秒）
    :return: Allan标准差数组（与taus同维度）
    """
    n = len(x)
    adev = []
    for tau in taus:
        m = int(tau / tau_s)  # 计算对应采样点数
        sigma = 0
        # 遍历所有可能的差分窗口
        for k in range(1, n - 2 * m):
            # 二阶差分公式计算频率波动
            delta = (x[k + 2 * m] - 2 * x[k + m] + x[k]) / tau
            sigma += delta ** 2
        # 计算统计方差并取平方根
        adev.append(np.sqrt(sigma / (2 * (n - 2 * m - 1))))
    return np.array(adev)


def estimate_noise_parameters(taus, adev_measured):
    """
    基于Allan方差测量值的噪声参数估计
    :param taus: 积分时间数组
    :param adev_measured: 测量的Allan标准差数组
    :return: 估计的噪声参数字典（包含A_wp, A_wf, A_ff, A_rw）
    """
    fh = 1  # 高频截止频率

    # 构建设计矩阵 (根据Allan方差理论模型)
    # H 6x4
    H = np.vstack([
        np.sqrt(fh / np.array(taus) ** 2),  # 白相位噪声项 (1/τ²)
        np.sqrt(1 / np.array(taus)),  # 白频率噪声项 (1/τ)
        np.ones(len(taus)),  # 闪烁频率噪声项 (常数)
        np.sqrt(np.array(taus)) # 随机游走噪声项 (τ)
    ]).T

    # 计算矩阵条件数
    cond = np.linalg.cond(H)
    print(f"设计矩阵条件数: {cond:.2e}")

    # 构建目标向量 (平方后的测量值)
    # y 6x1
    # y = adev_measured ** 2
    y = adev_measured
    # 最小二乘求解：Hθ = y → θ = (H^T H)^-1 H^T y
    # theta 4x1
    theta, _, _, _ = lstsq(H, y)

    estimated_params = {
        'A_wp': theta[0],  # 白相位噪声幅度
        'A_wf': theta[1],  # 白频率噪声幅度
        'A_ff': theta[2],  # 闪烁频率噪声幅度
        'A_rw': theta[3]   # 随机游走噪声幅度
    }

    # # 计算功率谱密度系数(h参数)
    # h_params = {
    #     'h2': (theta[0] * 4 * np.pi**2)/(3 * fh),  # 白相位噪声系数
    #     'h0': theta[1] * 2,                         # 白频率噪声系数
    #     'h_1': theta[2]**2/(2 * np.log(2)),        # 闪烁频率噪声系数
    #     'h_2': (3 * theta[3]**2)/(4 * np.pi**2)    # 随机游走噪声系数
    # }

    return estimated_params


def generate_power_spectrum(taus, adev_measured, num_points=100):
    """
    生成功率谱密度
    :param taus: 积分时间数组 (s)
    :param adev_measured: 测量的Allan标准差数组
    :param num_points: 频率点数
    :return: (功率谱密度数组, 频率数组)
    """
    # 通过Allan方差估计噪声参数h2,h0,h_1,h_2
    _, h_params = estimate_noise_parameters(taus, adev_measured)

    # 生成对数均匀分布的频率点,使用特征频率范围
    f_min = max(1e-10, 1 / (2 * np.pi * taus.max()))  # 最小频率,设置一个较小的正值下限
    f_max = max(1e-9, 1 / (2 * np.pi * taus.min()))   # 最大频率,确保大于f_min
    f = np.logspace(np.log10(f_min), np.log10(f_max), num_points)

    # 计算各噪声分量的功率谱密度
    Sy_components = {
        'wp': h_params['h2'] * f ** 2,  # 白相位噪声:h2*f^2
        'wf': np.full_like(f, h_params['h0']),  # 白频率噪声:h0
        'ff': h_params['h_1'] / f,  # 闪烁频率噪声:h_1/f
        'rw': h_params['h_2'] / f ** 2  # 随机游走噪声:h_2/f^2
    }

    # 叠加各噪声分量得到总功率谱密度
    Sy = np.zeros_like(f)
    for component in Sy_components.values():
        Sy += component

    # 计算时间误差功率谱密度
    Sx = 1 / (4 * np.pi ** 2 * f ** 2) * Sy  # Sx(f) = Sy(f)/(2πf)^2

    return Sy, f, Sx


def plot_allan_comparison(taus, sim_adev, theory_adev, title):
    """
    绘制Allan标准差对比图
    :param taus: 积分时间数组
    :param sim_adev: 仿真得到的Allan标准差
    :param theory_adev: 理论计算的Allan标准差
    :param title: 图表标题
    """
    plt.figure(figsize=(10, 6))
    plt.loglog(taus, sim_adev, 'bo-', label='Simulated')
    plt.loglog(taus, theory_adev, 'r--', label='Theoretical')
    plt.xlabel('tau (s)')
    plt.ylabel('Allan Standard Deviation')
    plt.title(title)
    plt.grid(True, which='both')
    plt.legend()
    plt.show()


# ====================================================
# 论文表格4的典型时钟配置示例
# ====================================================
if __name__ == "__main__":
    # 模拟参数
    # USO配置文件
    tau_s = 1/16  # 采样间隔（秒）
    N = 40000  # 样本数量
    # taus_list = [1, 10, 100, 1000, 10000, 86400]  # 积分时间数组，表示分析时钟稳定性的不同时间尺度


    # 时钟偏差初始值(秒)
    clock_offsets = 1.0388E-11  # (USO)
    # 时钟频率偏差(无量纲)
    clock_freqoffsets = 4.999E-8 # (USO)
    # 时钟频率线性漂移率(每秒)
    clock_freqlindrifts = 1.9450E-15
    # 时钟频率二次漂移率(每秒平方)
    clock_freqquaddrifts = -1.3725E-19

    # USO Allan方差序列——积分时间数组
    # taus_list = [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240, 20480]
    taus_list = [0.0625, 0.1250, 0.2500, 0.5000, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    # taus_list = [0.1, 1, 10, 100, 1000]
    taus = np.array(taus_list)  # 转换为NumPy数组
    # measured_adev = np.array([2e-13, 3e-14, 6e-15, 3e-15, 2.5e-15, 2e-15])

    # USO Allan方差序列——测量值
    # measured_adev = np.array(
    #     [0.0893e-11, 0.0545e-11, 0.0305e-11, 0.0226e-11, 0.0321e-11, 0.0595e-11, 0.1114e-11, 0.1870e-11, 0.2132e-11,
    #      0.1101e-11, 0.1518e-11, 0.1364e-11])
    measured_adev = np.array(
        [0.0512e-12, 0.0695e-12, 0.0763e-12, 0.0785e-12, 0.0781e-12, 0.0784e-12, 0.0795e-12, 0.0799e-12, 0.0784e-12, 0.0867e-12, 0.1059e-12, 0.1618e-12, 0.2897e-12, 0.5868e-12]
    )
    # measured_adev = np.array(
    #     [1.6e-13, 7e-14, 7.1e-14, 8e-14, 2.6e-13]
    # )

    measured_adev_dict = dict(zip(taus_list, measured_adev))

    # 参数估计（从仿真数据反推噪声参数）
    estimated_params= estimate_noise_parameters(taus, measured_adev)
    estimated_params_new = sqrt(
        ((estimated_params['A_wp']) * (1 / taus)) ** 2 + ((estimated_params['A_wf']) * (1 / sqrt(taus))) ** 2 + (
            estimated_params['A_ff']) ** 2 + ((estimated_params['A_rw']) * sqrt(taus)) ** 2)
    estimated_params_new_dict = dict(zip(taus_list, estimated_params_new))

    plot_allan_comparison(taus, estimated_params_new, measured_adev, 'plot_allan_comparison')

    # 生成时钟误差和生成各噪声分量
    generator = ClockErrorGenerator(tau_s=tau_s)
    y_total, x, components = generator.generate_clock_errors(estimated_params, N)
    # 生成时间序列
    t = np.arange(N) * tau_s
    clock_offset = (clock_offsets + clock_freqoffsets * t + clock_freqlindrifts * t ** 2 / 2
                    + clock_freqquaddrifts * t ** 3 / 3) + x

    # 绘制四种噪声的频率偏差图
    # plt.figure(figsize=(10, 10))
    # plt.subplot(211)
    # plt.plot(t, components['wp'], 'r-', label='白相位噪声', alpha=0.7)
    # plt.plot(t, components['wf'], 'g-', label='白频率噪声', alpha=0.7)
    # plt.plot(t, components['ff'], 'b-', label='闪烁频率噪声', alpha=0.7)
    # plt.plot(t, components['rw'], 'y-', label='随机游走噪声', alpha=0.7)
    # plt.xlabel('时间 (s)')
    # plt.ylabel('频率偏差 (s/s)')
    # plt.title('四种噪声的频率偏差')
    # plt.grid(True)
    # plt.legend()

    # 计算各噪声分量的钟差
    # clock_wp = np.cumsum(components['wp']) * tau_s
    # clock_wf = np.cumsum(components['wf']) * tau_s
    # clock_ff = np.cumsum(components['ff']) * tau_s
    # clock_rw = np.cumsum(components['rw']) * tau_s

    # 绘制四种噪声的钟差图
    # plt.subplot(212)
    # plt.plot(t, clock_wp, 'r-', label='白相位噪声', alpha=0.7)
    # plt.plot(t, clock_wf, 'g-', label='白频率噪声', alpha=0.7)
    # plt.plot(t, clock_ff, 'b-', label='闪烁频率噪声', alpha=0.7)
    # plt.plot(t, clock_rw, 'y-', label='随机游走噪声', alpha=0.7)
    # plt.xlabel('时间 (s)')
    # plt.ylabel('钟差 (s)')
    # plt.title('四种噪声的钟差')
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()


    # # 模型一：频率白噪声 + 频率闪烁噪声
    # model1_params = {
    #     'A_wp': 0,  # 无白相位噪声
    #     'A_wf': estimated_params['A_wf'],  # 保留频率白噪声
    #     'A_ff': estimated_params['A_ff'],  # 保留频率闪烁噪声
    #     'A_rw': 0  # 无随机游走频率噪声
    # }
    #
    # # 模型二：完整噪声模型
    # model2_params = {
    #     'A_wp': estimated_params['A_wp'],  # 白相位噪声
    #     'A_wf': estimated_params['A_wf'],  # 频率白噪声
    #     'A_ff': estimated_params['A_ff'],  # 频率闪烁噪声
    #     'A_rw': estimated_params['A_rw']   # 随机游走频率噪声
    # }

    # 生成两种模型的时钟误差
    # y_model1, x_model1, _ = generator.generate_clock_errors(model1_params, N)
    # y_model2, x_model2, _ = generator.generate_clock_errors(model2_params, N)

    # 计算两种模型的完整时钟偏差
    # clock_offset_model1 = clock_offsets + clock_freqoffsets * t + clock_freqlindrifts * t**2/2 + clock_freqquaddrifts * t**3/3 + x_model1
    # clock_offset_model2 = clock_offsets + clock_freqoffsets * t + clock_freqlindrifts * t**2/2 + clock_freqquaddrifts * t**3/3 + x_model2
    # # # 绘制三种钟差对比图
    # plt.figure(figsize=(12, 6))
    # plt.plot(t, clock_offset, 'b-', label='测量值钟差', linewidth=1.5, alpha=0.7)
    # plt.plot(t, clock_offset_model1, 'r--', label='模型一钟差(WF+FF)', linewidth=1.5, alpha=0.7)
    # plt.plot(t, clock_offset_model2, 'g:', label='模型二钟差(完整模型)', linewidth=1.5, alpha=0.7)
    # plt.xlabel('时间 (s)', fontsize=12)
    # plt.ylabel('钟差 (s)', fontsize=12)
    # plt.title('不同噪声模型的钟差对比', fontsize=14)
    # plt.grid(True, linestyle='--', alpha=0.7)
    # plt.legend(fontsize=10)
    # plt.tight_layout()
    # plt.show()
    # 计算Allan偏差
    adev = allan_deviation(taus, clock_offset, tau_s)

    plot_allan_comparison(taus, adev, measured_adev, 'plot_allan_comparison')
    # 创建三个子图
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))

    # Allan偏差图
    ax1.loglog(taus, adev, 'go-', linewidth=1.5, markersize=8)
    ax1.set_xlabel('Time τ(s)', fontsize=12)
    ax1.set_ylabel('Allan σ(τ) (s/s)', fontsize=12)
    # ax1.set_title('Allan偏差随积分时间的变化', fontsize=14)
    ax1.grid(True, which='both', linestyle='--', alpha=0.7)
    ax1.set_xlim(0.1, 1000)
    # 时钟误差图
    ax2.plot(t, clock_offset, 'b-', linewidth=1.5)
    ax2.set_xlabel('Time (s)', fontsize=12)
    ax2.set_ylabel('clock offset (s)', fontsize=12)
    #ax2.set_title('时钟误差序列', fontsize=14)
    ax2.grid(True, linestyle='--', alpha=0.7)

    # 频率偏差图
    ax3.plot(t, y_total, 'r-', linewidth=1.5)
    ax3.set_xlabel('Time (s)', fontsize=12)
    ax3.set_ylabel('Frequency Offset (s/s)', fontsize=12)
    # ax3.set_title('Clock Frequency Offset', fontsize=14)
    ax3.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    # # 计算测量值与模拟值之间的差异
    # error_model1 = clock_offset - clock_offset_model1
    # error_model2 = clock_offset - clock_offset_model2
    #
    # rmse_model1_cumulative = np.sqrt(np.cumsum(error_model1**2) / np.arange(1, len(error_model1) + 1))
    # rmse_model2_cumulative = np.sqrt(np.cumsum(error_model2**2) / np.arange(1, len(error_model2) + 1))
    # #
    # # 绘制RMSE对比图
    # plt.figure(figsize=(12, 6))
    # plt.plot(t, rmse_model1_cumulative, 'b-', label='模型一(WF+FF)', linewidth=1.5, alpha=0.7)
    # plt.plot(t, rmse_model2_cumulative, 'r--', label='模型二(完整模型)', linewidth=1.5, alpha=0.7)
    # plt.xlabel('时间 (s)', fontsize=12)
    # plt.ylabel('累积RMSE (s)', fontsize=12)
    # plt.title('不同噪声模型的累积RMSE对比', fontsize=14)
    # plt.grid(True, linestyle='--', alpha=0.7)
    # plt.legend(fontsize=10)
    # plt.tight_layout()
    # plt.show()
    #


    # # 创建第一个图形 - 钟差序列
    # plt.figure(figsize=(12, 6))
    # plt.plot(t, clock_offset, 'b-', label='仿真钟差序列', linewidth=1.5)
    # plt.xlabel('时间 (s)', fontsize=12)
    # plt.ylabel('钟差 (s)', fontsize=12)
    # plt.title('时钟误差序列', fontsize=14)
    # plt.grid(True, linestyle='--', alpha=0.7)
    # plt.legend(fontsize=10)
    # plt.tight_layout()
    # plt.show()
    #
    # # 创建三个独立的图形
    # plt.figure(figsize=(10, 6))
    # plt.plot(t, clock_offset, 'b-', linewidth=1.5)
    # plt.xlabel('时间 (s)', fontsize=12)
    # plt.ylabel('钟差 (s)', fontsize=12)
    # plt.title('时钟误差累积', fontsize=14)
    # plt.grid(True, linestyle='--', alpha=0.7)
    # plt.tight_layout()
    # plt.show()
    #
    # plt.figure(figsize=(10, 6))
    # plt.plot(t[1:], np.diff(clock_offset), 'r-', linewidth=1.5)
    # plt.xlabel('时间 (s)', fontsize=12)
    # plt.ylabel('钟差差分 (s/s)', fontsize=12)
    # plt.title('时钟误差变化率', fontsize=14)
    # plt.grid(True, linestyle='--', alpha=0.7)
    # plt.tight_layout()
    # plt.show()

    # # 绘制频率偏差图
    # plt.figure(figsize=(10, 6))
    # plt.plot(t, y_total, 'k-', linewidth=1.5)
    # plt.xlabel('时间 (s)', fontsize=12)
    # plt.ylabel('频率偏差 (s/s)', fontsize=12)
    # plt.title('时钟频率偏差', fontsize=14)
    # plt.grid(True, linestyle='--', alpha=0.7)
    # plt.tight_layout()
    # plt.show()

    # # 计算Allan偏差
    # adev = allan_deviation(taus, clock_offset, tau_s)
    #
    # plt.figure(figsize=(10, 6))
    # plt.loglog(taus, adev, 'go-', linewidth=1.5, markersize=8)
    # plt.xlabel('积分时间 τ (s)', fontsize=12)
    # plt.ylabel('Allan偏差 σ(τ) (s/s)', fontsize=12)
    # plt.title('Allan偏差随积分时间的变化', fontsize=14)
    # plt.grid(True, which='both', linestyle='--', alpha=0.7)
    # plt.tight_layout()
    # plt.show()

    #
    # # 生成时钟误差
    # generator = ClockErrorGenerator(tau_s=tau_s)
    # y_total, x, _ = generator.generate_clock_errors(Hydrogen_Maser_params, N)

    # 计算Allan方差
    # sim_adev = allan_deviation(taus, x, tau_s)


    # # 功率谱密度计算
    # Sy, f, Sx = generate_power_spectrum(taus, measured_adev, num_points=100)
    # plt.figure(figsize=(10, 6))
    # # 确保数据为正值
    # Sx_positive = np.abs(Sx)  # 取绝对值
    # Sx_positive[Sx_positive < 1e-30] = 1e-30  # 设置最小值下限
    #
    # rad=(Sx_positive * 299792458 /(1064*1E-9))*2 * np.pi
    # asd = np.sqrt(Sx_positive)

    # # 绘制rad图
    # plt.figure(figsize=(10, 6))
    # plt.loglog(f, rad, 'bo-', label='仿真结果', linewidth=1.5, markersize=4)
    # plt.xlabel('频率 (Hz)', fontsize=12)
    # plt.ylabel('相位噪声 (rad/√Hz)', fontsize=12)
    # plt.title('USO相位噪声谱密度', fontsize=14)
    # plt.grid(True, which='both', linestyle='--', alpha=0.7)
    # plt.legend(fontsize=10)
    # plt.xlim(1e-4, 1e0)
    # plt.tight_layout()
    # plt.show()
    #
    # # 绘制asd图
    # plt.figure(figsize=(10, 6))
    # plt.loglog(f, asd, 'ro-', label='仿真结果', linewidth=1.5, markersize=4)
    # plt.xlabel('频率 (Hz)', fontsize=12)
    # plt.ylabel('幅度谱密度 (s/√Hz)', fontsize=12)
    # plt.title('USO时间误差幅度谱密度', fontsize=14)
    # plt.grid(True, which='both', linestyle='--', alpha=0.7)
    # plt.legend(fontsize=10)
    # plt.xlim(1e-4, 1e0)
    # plt.tight_layout()
    # plt.show()

    # plt.loglog(f, Sx_positive, 'bo-', label='仿真结果', linewidth=1.5, markersize=4)
    # plt.xlabel('频率 (Hz)', fontsize=12)
    # plt.ylabel('功率谱密度 (s²/Hz)', fontsize=12)
    # plt.title('USO时间误差功率谱密度', fontsize=14)
    # plt.grid(True, which='both', linestyle='--', alpha=0.7)
    # plt.legend(fontsize=10)
    # plt.xlim(1e-4, 1e0)  # 设置X轴范围
    # plt.tight_layout()
    # plt.show()

    # # 控制台输出详细误差分析
    # print("\n参数估计误差分析:")
    # print("{:<8} | {:<12} | {:<12} | {:<10}".format(
    #     "τ/s", "实测值", "最小二乘法", "相对误差(%)"))
    # print("-" * 50)
    # for key in taus_list:
    #     true_val = measured_adev_dict[key]
    #     est_val = estimated_params_new_dict[key]
    #     if true_val == 0:
    #         error = 0 if est_val == 0 else np.inf
    #     else:
    #         error = 100 * abs(est_val - true_val) / true_val
    #     print("{:<8} | {:<12.2e} | {:<12.2e} | {:<10.2f}".format(
    #         key, true_val, est_val, error))
