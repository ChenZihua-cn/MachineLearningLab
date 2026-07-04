# 波形近似模型 (Approximant) 选择

## 当前选择: SEOBNRv4

SEOBNRv4 (Bohé et al., 2017, [arXiv:1611.03703](https://arxiv.org/abs/1611.03703)) 是基于有效单体理论 (Effective-One-Body, EOB) 校准于数值相对论 (NR) 的高精度波形模型，覆盖 inspiral、merger 和 ringdown 全阶段。

选择理由：

- **相位精度高**：inspiral 阶段相位误差 < 0.1 rad，适合作为 PySR 符号回归的 "ground truth"
- **自旋处理完整**：支持双自旋 (spin1z, spin2z)，覆盖实际 BBH 参数空间
- **广泛验证**：LIGO/Virgo 参数估计的标准模型之一，物理可信度高

## 依赖: 无需外部数据文件

**SEOBNRv4（完整 EOB 模型）无需外部数据文件**，已在 `gw` conda 环境中验证可直接使用。

需要注意 LALSuite 中 `SEOBNRv4` 有两个变体:

| 模型 | 实现方式 | 外部 HDF5 |
|------|---------|-----------|
| `SEOBNRv4` | 完整 EOB 解析模型 | **不需要** |
| `SEOBNRv4_ROM` | ROM 加速版 | 需要 `SEOBNRv4ROM_v3.0.hdf5` |

两者物理精度相同 (~0.1 rad)，区别仅在于 ROM 版计算更快。本项目使用 `SEOBNRv4`（完整模型）。

> 注意: `pycbc.waveform.get_fd_waveform("SEOBNRv4")` 内部计算波形长度时会走 ROM 路径（`SimIMRSEOBNRv4ROMTimeOfFrequency`），因此会触发 HDF5 缺失错误。请使用 `pycbc.waveform.get_td_waveform("SEOBNRv4")` 生成时域波形，或使用 `IMRPhenomD` 进行频域计算。

如需使用 `SEOBNRv4_ROM`，需要下载数据文件 (~50 MB) 并设置 `$LAL_DATA_PATH`:

### 安装方式

```bash
# 1. 下载数据文件（约 50 MB）
wget https://zenodo.org/records/14999310/files/lalsuite-waveform-data.tar.gz
# 或从 git.ligo.org 获取：
# git clone https://git.ligo.org/waveforms/software/lalsuite-waveform-data

# 2. 解压并设置环境变量
tar -xzf lalsuite-waveform-data.tar.gz -C /path/to/data
export LAL_DATA_PATH=/path/to/data

# 3. 持久化（写入 ~/.bashrc）
echo 'export LAL_DATA_PATH=/path/to/data' >> ~/.bashrc
```

## 备选方案: IMRPhenomD

如果不想安装额外数据文件，可切换到 IMRPhenomD (Husa et al., 2016, [arXiv:1508.07250](https://arxiv.org/abs/1508.07250))，它是频域唯象模型 (phenomenological model)，内置于 LALSuite，无需外部数据。

只需修改 `generate_wave.py` 中的 params：

```python
"approximant": "IMRPhenomD"
```

权衡：

| | SEOBNRv4 | IMRPhenomD |
|---|---|---|
| 优点 | 相位精度最高 (~0.1 rad) | 零外部依赖，即装即用，计算更快 |
| 缺点 | 需要下载数据文件 | inspiral 相位精度略低 (~0.3 rad) |

对 PySR 符号回归任务而言，IMRPhenomD 的精度通常已足够。

## 其他备选模型

| 模型 | 类型 | 外部数据 | 自旋支持 | 相位精度 | 适用场景 |
|------|------|---------|----------|---------|---------|
| SEOBNRv4 | EOB + NR | 不需要 | 双自旋 (z) | ~0.1 rad | 高精度 ground truth |
| IMRPhenomD | 唯象模型 | 不需要 | 双自旋 (z) | ~0.3 rad | 快速原型，零依赖 |
| TaylorF2 | 后牛顿展开 | 不需要 | 自旋 (z) | PN 截断误差 | inspiral-only 解析公式 |
| IMRPhenomPv2 | 唯象 + 进动 | 不需要 | 双自旋 (x,y,z) | ~0.5 rad | 需要进动效应的场景 |
| SEOBNRv4_ROM | EOB + ROM | 需要 | 双自旋 (z) | ~0.1 rad | ROM 加速版，需 HDF5 |

## 对本项目的影响

本项目目标是验证 PySR 能否从噪声数据中恢复 $f \propto (t_c - t)^{-3/8}$ 的 chirp 关系。这对波形模型的绝对相位精度要求不高——后牛顿展开的主项 (leading order) 在典型 SNR 下已足够。因此：

- **推荐优先使用 IMRPhenomD** 进行快速迭代
- **最终验证切换到 SEOBNRv4** 确认结论不依赖于模型系统误差
