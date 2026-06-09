"""
Part 1.2 — 纯净信号符号回归

聚焦相位演化：不让 PySR 直接拟合整个波形，而是让它从纯净的相位数据中
重新发现频率演化公式。

已知牛顿近似下，频率随时间演化为:
    f(t) = 1/(8π) * [(G*Mc/c³)^(-5/8)] * (tc - t)^(-3/8) + ...

只给出 f(t) 的数值数据，让 PySR 猜测 f(t) 与 (tc - t) 的关系。

管线位置: generate_wave.py → pure_simulated_SR.py → noise_simulated_SR.py
"""
