"""
Part 1.1 — 波形生成

使用 pycbc 生成双黑洞并合波形（只取 inspiral 部分，持续时间 1-2 秒，采样率 4096 Hz），
计算振幅和相位的时间序列。

管线位置: generate_wave.py → pure_simulated_SR.py → noise_simulated_SR.py
"""

from pycbc.waveform import get_td_waveform
import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt

# 参数设置
params = {
    "approximant": "SEOBNRv4",
    "mass1": 36.0,          # 主黑洞质量（太阳质量单位）
    "mass2": 29.0,          # 次级黑洞质量
    "spin1z": 0.7,          # 主黑洞自旋（沿对称轴）
    "spin2z": 0.5,          # 次级黑洞自旋
    "f_lower": 20.0,        # 最低频率（Hz），波形从此频率开始
    "delta_t": 1.0 / 4096,  # 采样间隔（4096 Hz 采样率）
}

# 生成 SEOBNRv4 时域波形（完整 EOB 模型，无需外部 HDF5 数据）
hp, hc = get_td_waveform(**params)

# 提取时间序列
times = hp.sample_times.numpy()
dt = hp.delta_t

# 通过 Hilbert 变换计算瞬时频率和相位

"""
Explicit np.ndarray type annotations on all variables tell Pylance what types to expect,
preventing tuple[Dispatchable] from propagating through the chain.
"""

hp_np: np.ndarray = np.asarray(hp.numpy())
analytic_signal: np.ndarray = np.asarray(hilbert(hp_np))
amplitude: np.ndarray = np.abs(analytic_signal)
phases: np.ndarray = np.unwrap(np.angle(analytic_signal))
freqs: np.ndarray = np.gradient(phases) / (2 * np.pi * dt)  # Hz

# Sci-Plot
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(times, freqs, "b-")
plt.xlabel("Time [s]")
plt.ylabel("Instantaneous Frequency [Hz]")
plt.title("Instantaneous Frequency")

plt.subplot(1, 2, 2)
plt.plot(times, phases % (2 * np.pi), "r-")
plt.xlabel("Time [s]")
plt.ylabel("Instantaneous Phase [rad]")
plt.title("Instantaneous Phase (mod 2π)")

plt.tight_layout()
plt.show()

np.save("waveform_clean.npy", hp_np)
np.savez("waveform_processed.npz",
         times=times, dt=dt,
         amplitude=amplitude, phases=phases, freqs=freqs)
print("Saved waveform_clean.npy and waveform_processed.npz")
