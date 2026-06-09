"""
Part 1.3 — 加噪测试

向纯净信号中加入不同功率的高斯白噪声（从 LIGO 设计灵敏度曲线反推典型
噪声水平），生成不同 SNR 的相位数据（SNR: ∞ → 10, 8, 5, 3）。

对每个 SNR 数据集，固定搜索算符集 (+, -, *, /, pow, sqrt)，
让 PySR 寻找 f ~ (tc - t)^α 形式的公式。

目标: 找出 PySR 无法恢复幂律形式的临界 SNR。

管线位置: generate_wave.py → pure_simulated_SR.py → noise_simulated_SR.py
"""
