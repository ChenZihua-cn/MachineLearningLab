# PySR in Gravity Wave

> *PySR3 is an open-source library for practical symbolic regression, a type of machine learning which aims to discover human-interpretable symbol.*
> — Cranmer et al., [arXiv:2305.01582](https://arxiv.org/abs/2305.01582)
>
> *At its core, symbolic regression endeavors to identify a functional form, f, such that y = f(x1, x2, ..., xn) optimally describes the relationship between a set of input variables {xi} and an output variable y, based on a given dataset. Unlike traditional regression methods where the structure of f is assumed a priori, SR algorithms explore a diverse range of mathematical operators and their combinations to construct an accurate model.*
> — [arXiv:2512.15920](https://arxiv.org/abs/2512.15920)

## 核心问题

符号回归（PySR）在引力波瞬态噪声（glitches）和探测器高斯噪声背景下，能否可靠地从数据中还原已知的波形物理定律？其在什么信噪比（SNR）水平下会彻底失效？

双黑洞并合产生的引力波波形由广义相对论精确预言的，其主导的inspiral阶段遵循“啁啾”关系，相位演化有严格的解析近似（后牛顿展开），这为我们提供了“真实答案”。

$$f(t) = \frac{1}{8\pi} \left[ \left( \frac{GM_c}{c^3} \right)^{-5/8} (t_c - t)^{-3/8} + \dots \right]$$  

引力波数据既有宽带的高斯噪声（探测器热噪声、量子噪声），也有非高斯、非稳态的瞬态噪声（glitches）。

> PySR是学术玩具?发现不了新物理? 
> - 过拟合、无法处理噪声、工业落地差; 
> - 90年代遗传编程的Julia换皮; 
> - 只能在小数据场景下作为探索工具.

## 实验设计

实验分三步递进，代码组织在对应目录中：

| 步骤 | 目录 | 目标 |
|------|------|------|
| 1 | `part_1/` | 高斯噪声基准：建立纯净→加噪的SR恢复能力曲线 |
| 2 | `part_2/` | 真实探测器噪声（LIGO敏感曲线） |
| 3 | `part_3/` | 瞬态Glitch过拟合测试 |

### Part 1: 噪声鲁棒性基准测试

**管线:** `generate_wave.py` → `pure_simulated_SR.py` → `noise_simulated_SR.py`

- [ ] 生成双黑洞并合inspiral波形，提取瞬时相位/频率
- [ ] 纯净数据上验证PySR能恢复 $f \propto (t_c-t)^{-3/8}$
- [ ] 高斯白噪声扫参 (SNR: ∞, 10, 8, 5, 3)，找出SR崩溃的临界SNR

### Part 2: 真实探测器噪声
- [ ] 引入LIGO设计灵敏度曲线形状的非白噪声
- [ ] 验证PySR是否过拟合到特定频率噪声线

### Part 3: Glitch过拟合
- [ ] 注入瞬态大噪声（glitch），验证PySR过拟合到无物理意义的复杂函数

## 参考文献

1. Cranmer, M. et al. (2023). *Interpretable Machine Learning for Science with PySR and SymbolicRegression.jl.* [arXiv:2305.01582](https://arxiv.org/abs/2305.01582)
2. [arXiv:2512.15920](https://arxiv.org/abs/2512.15920)