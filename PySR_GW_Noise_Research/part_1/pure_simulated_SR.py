"""
Part 1.2 — 纯净信号符号回归

聚焦相位演化：不让 PySR 直接拟合整个波形，而是让它从纯净的相位数据中
重新发现频率演化公式。

已知牛顿近似下，频率随时间演化为:
    f(t) = 1/(8π) * [(G*Mc/c³)^(-5/8)] * (tc - t)^(-3/8) + ...

只给出 f(t) 的数值数据，让 PySR 猜测 f(t) 与 (tc - t) 的关系。

管线位置: generate_wave.py → pure_simulated_SR.py → noise_simulated_SR.py
"""

import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt


# 1. 加载波形，计算瞬时频率

# 优先使用 generate_wave.py 预处理好的数据，否则从原始波形计算

data = np.load("waveform_processed.npz")
times: np.ndarray = data["times"]
dt: float = float(data["dt"])
amp: np.ndarray = data["amplitude"]
phase: np.ndarray = data["phases"]
freq: np.ndarray = data["freqs"]
print("Loaded precomputed waveform_processed.npz")



# 2. 确定并合时间 tc，提取 inspiral 区间

# tc 取频率最大值处（对应 merger）
tc_idx = int(np.argmax(freq))
tc = float(times[tc_idx])
print(f"Coalescence time tc = {tc:.4f} s (index {tc_idx} / {len(times)})")

# 只取 inspiral 部分: t < tc 且频率有效（f > f_lower）
f_lower = 20.0
inspiral_mask = (times < tc) & (freq > f_lower)
t_insp = times[inspiral_mask]
f_insp = freq[inspiral_mask]
tc_minus_t = tc - t_insp

print(f"Inspiral points: {len(t_insp)} (f_lower = {f_lower} Hz)")


# 3. 预检查：对数空间线性拟合验证幂律关系

log_x = np.log(tc_minus_t)
log_f = np.log(f_insp)
slope, intercept = np.polyfit(log_x, log_f, 1)
expected_slope = -3.0 / 8.0  # -0.375

print(f"\nPower-law fit:  log(f) = {slope:.4f} * log(tc - t) + {intercept:.4f}")
print(f"Expected slope:  -3/8 = {expected_slope:.4f}")
print(f"Fitted exponent: α = {slope:.4f}")

# Sci-Plot
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].plot(times, freq, lw=0.5)
axes[0, 0].axvline(tc, color="gray", ls="--", label=f"$t_c$ = {tc:.3f} s")
axes[0, 0].set_xlabel("Time [s]")
axes[0, 0].set_ylabel("$f$ [Hz]")
axes[0, 0].set_title("Instantaneous Frequency (full)")
axes[0, 0].legend()

axes[0, 1].loglog(tc_minus_t, f_insp, lw=0.5)
axes[0, 1].set_xlabel("$t_c - t$ [s]")
axes[0, 1].set_ylabel("$f(t)$ [Hz]")
axes[0, 1].set_title(r"$\log$-$\log$: $f$ vs $t_c - t$ (inspiral)")

fit_f = np.exp(intercept) * tc_minus_t**slope
axes[1, 0].loglog(tc_minus_t, f_insp, lw=0.5, label="data")
axes[1, 0].loglog(
    tc_minus_t,
    fit_f,
    "--",
    lw=1.5,
    label=rf"fit: $\alpha = {slope:.4f}$" + "\n"
    rf"(expected $\alpha = -3/8 = {expected_slope:.4f}$)",
)
axes[1, 0].set_xlabel("$t_c - t$ [s]")
axes[1, 0].set_ylabel("$f(t)$ [Hz]")
axes[1, 0].set_title("Power-law Check")
axes[1, 0].legend()

# 4th panel + plt.tight_layout/show deferred to Section 8 (after PySR)


# 4. 降采样（PySR 在过大样本上运行缓慢）

N_MAX = 2000
if len(tc_minus_t) > N_MAX:
    idx = np.linspace(0, len(tc_minus_t) - 1, N_MAX, dtype=int)
    X = tc_minus_t[idx].reshape(-1, 1)
    y = f_insp[idx]
    print(f"\nSubsampled: {len(tc_minus_t)} → {N_MAX} points for PySR")
else:
    X = tc_minus_t.reshape(-1, 1)
    y = f_insp

# 变量命名提示 PySR: x1 = (tc - t)
print(f"X.shape = {X.shape}, y.shape = {y.shape}")


# 5. PySR 符号回归

from pysr import PySRRegressor

# 算符集: 四则运算 + 幂 + 基本函数
# PySR 内置常数优化，不需要显式添加常数算符
model = PySRRegressor(
    niterations=40,  # 演化代数，可根据精度调整
    binary_operators=["+", "-", "*", "/", "pow"],
    unary_operators=["sqrt", "log", "exp"],
    constraints={"^": (-1, 1)},  # 指数只能是常数或变量（如 x^2）加法无限制
    model_selection="best",  # 选 loss 最低的公式
    maxsize=20,  # 表达式树最大复杂度
    parsimony=1e-4,  # 正则化系数，防止过复杂公式
    warm_start=False,
    verbosity=1,
    progress=True,
)

print("\nRunning PySR...")
model.fit(X, y)


# 6. 输出结果

print("\n" + "=" * 60)
print("Best equation found by PySR:")
print(model.sympy())
print("=" * 60)

# 打印候选公式列表
if hasattr(model, "equations_"):
    eqs = model.equations_
    if eqs is not None and len(eqs) > 0:
        print("\nCandidate equations (top 5):")
        for i in range(min(5, len(eqs))):
            row = eqs.iloc[i] if hasattr(eqs, "iloc") else eqs[i]
            print(f"  [{i}] {row.get('equation', row)}")


# 8. 2x2 汇总图：前3个面板 + PySR 候选公式

# 收集 PySR 候选公式文本
eq_text = f"Best: {model.sympy()}\n\nTop candidates:\n"
if hasattr(model, "equations_"):
    eqs = model.equations_
    if eqs is not None and len(eqs) > 0:
        for i in range(min(5, len(eqs))):
            row = eqs.iloc[i] if hasattr(eqs, "iloc") else eqs[i]
            eq_str = str(row.get("equation", row))
            loss = row.get("loss", float("nan"))
            eq_text += f"\n[{i}] loss={loss:.4f}\n    {eq_str}"

# 第4个面板：PySR 候选公式
axes[1, 1].axis("off")
axes[1, 1].text(
    0.05, 0.95, eq_text,
    transform=axes[1, 1].transAxes,
    fontsize=12, fontfamily="monospace",
    verticalalignment="top",
    horizontalalignment="left",
)
axes[1, 1].set_title("PySR Candidate Equations", fontsize=10)

plt.tight_layout()
plt.savefig("pure_SR_precheck.png", dpi=150)
print("Saved pure_SR_precheck.png (2×2 with PySR equations)")
plt.show()


# 7. 保存数据供 noise_simulated_SR.py 使用

np.savez(
    "pure_SR_data.npz",
    tc=tc,
    times=times,
    freq=freq,
    phase=phase,
    amp=amp,
    tc_minus_t=tc_minus_t,
    f_inspiral=f_insp,
    expected_slope_neg_3_8=expected_slope,
    fitted_slope=slope,
)
print("\nSaved pure_SR_data.npz for noise_simulated_SR.py")
