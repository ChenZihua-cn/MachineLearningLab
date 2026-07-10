"""
Part 1.1 — 波形生成

使用 pycbc 生成双黑洞并合波形（只取 inspiral 部分，持续时间 1-2 秒，采样率 4096 Hz），
计算振幅和相位的时间序列。

管线位置: generate_wave.py → pure_simulated_SR.py → noise_simulated_SR.py
"""

from pycbc.waveform import get_td_waveform
import numpy as np
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

# 对 face-on 朝向（默认 inclination=0），h+ 和 h× 天然构成解析信号：
#   h+ = A(t)·cos(Φ(t)),  h× = A(t)·sin(Φ(t))
#   → analytic = h+ + i·h× = A(t)·exp(i·Φ(t))
# 无需 Hilbert 变换，彻底避开边界伪影。
hp_np: np.ndarray = np.asarray(hp.numpy())
hc_np: np.ndarray = np.asarray(hc.numpy())

analytic_signal: np.ndarray = hp_np + 1j * hc_np
amplitude: np.ndarray = np.abs(analytic_signal)
phases: np.ndarray = np.unwrap(np.angle(analytic_signal))
freqs: np.ndarray = np.gradient(phases) / (2 * np.pi * dt)  # Hz

# Sci-Plot: 2x2 布局
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

ax_wave_hp = axes[0, 0]
ax_wave_hc = axes[0, 1]
ax_freq = axes[1, 0]
ax_phase = axes[1, 1]

ax_wave_hp.plot(times, hp_np, "b-", linewidth=0.6)
ax_wave_hp.set_xlabel("Time [s]")
ax_wave_hp.set_ylabel("Strain")
ax_wave_hp.set_title(r"$h_+$ Waveform")

ax_wave_hc.plot(times, hc_np, "c-", linewidth=0.6)
ax_wave_hc.set_xlabel("Time [s]")
ax_wave_hc.set_ylabel("Strain")
ax_wave_hc.set_title(r"$h_\times$ Waveform")

ax_freq.plot(times, freqs, "b-")
ax_freq.set_xlabel("Time [s]")
ax_freq.set_ylabel("Instantaneous Frequency [Hz]")
ax_freq.set_title("Instantaneous Frequency")

ax_phase.plot(times, phases % (2 * np.pi), "r-")
ax_phase.set_xlabel("Time [s]")
ax_phase.set_ylabel("Instantaneous Phase [rad]")
ax_phase.set_title("Instantaneous Phase (mod $2\pi$)")

plt.tight_layout()
plt.savefig("generated_waveform.png")
plt.show()

print("Saved generated_waveform.png")

np.save("waveform_clean.npy", hp_np)
np.savez("waveform_processed.npz",
         times=times, dt=dt,
         amplitude=amplitude, phases=phases, freqs=freqs)
print("Saved waveform_clean.npy and waveform_processed.npz")
