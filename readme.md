# [原仓库链接](https://github.com/iphysresearch/UndergradResearchLab)

此处我选择题目1和题目2来练习机器学习，或许可能写一个kaggle上的泰坦尼克号的练习题。

## **引力波天文学 + AI for Science 交叉研究**

具体来说：

### 引力波数据分析（观测端）

| 研究内容 | 说明 |
|----------|------|
| **引力波信号搜寻** | 从噪声中提取微弱的引力波信号 |
| **参数估计** | 确定波源质量、距离、位置等参数 |
| **多信使天文学** | 引力波+电磁波+中微子联合观测 |
| **数据挑战** | 模拟真实数据，训练分析算法 |

**对应的题目：**
- (一) [致密双星并合信号搜寻](./Search%20for%20Gravitational%20Wave%20Signals/)
- (二) [快速参数推断](./Rapid%20parameter%20inference/)
- (三) PycWB时频聚类分析
- (五) LISA/Taiji Data Challenge

## 跨平台工作流：Windows + WSL 协同说明

本项目采用**双环境分离**的设计思路，以兼顾易用性与功能性：

- **Windows 宿主环境**：运行 PySR、Julia、PyTorch（GPU），负责符号回归与模型训练。
- **WSL 2 环境**：运行 PyCBC 与 LALSuite，负责引力波波形生成。

两个环境通过**共享文件目录 + 软链接**实现无缝数据交换，无需手动复制文件。

### 1. 环境搭建速览

| 环境  | 主要任务         | 核心技术栈                        |
| ----- | ---------------- | --------------------------------- |
| Windows | 符号回归 / 训练  | `pysr`、`julia`、`torch` (CUDA)   |
| WSL   | 波形生成         | `pycbc`、`lalsuite`（通过 Conda 安装） |

WSL 环境一键配置（在 Ubuntu 22.04 / 24.04 中执行）：

```bash
# 安装 Miniconda（如果尚未安装）
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# 重启终端后执行：
conda create -n gw python=3.10 -y
conda activate gw
conda install -c conda-forge pycbc lalsuite -y
```

验证安装：

```python
from pycbc.waveform import get_td_waveform
hp, hc = get_td_waveform(approximant="SEOBNRv4_opt", mass1=10, mass2=10, delta_t=1/4096, f_lower=30)
print("✅ 波形生成成功")
```

### 2. 目录共享与软链接（核心）

**目标**：让 WSL 和 Windows 能“看到”同一组数据文件。

1. **在 Windows 上创建共享目录**（例如 `D:\gw_shared`）。
2. **在 WSL 中创建软链接**指向该目录：

```bash
ln -s /mnt/d/gw_shared ~/gw_data
```

3. **在 WSL 中生成波形并直接写入共享目录**：

```python
import numpy as np
from pycbc.waveform import get_td_waveform

hp, hc = get_td_waveform(approximant="SEOBNRv4_opt", mass1=10, mass2=10, delta_t=1/4096, f_lower=30)
np.save("~/gw_data/waveform_hp.npy", hp)
np.save("~/gw_data/waveform_hc.npy", hc)
```

4. **在 Windows 中直接读取同一目录**：

```python
import numpy as np
hp = np.load("D:/gw_shared/waveform_hp.npy")
```

> **提示**：Windows 访问 WSL 文件的路径为 `\\wsl$\Ubuntu\home\你的用户名\gw_data`，亦可直接映射为网络驱动器。

### 3. 完整工作流示意图

```text
[WSL]  PyCBC 生成波形
        ↓ 保存至
~/gw_data (软链接)
        ↓ 实际指向
/mnt/d/gw_shared (Windows NTFS)
        ↓ Windows 中直接读取
D:\gw_shared\*.npy
        ↓ 输入至
[Windows] PySR / PyTorch
```

### 4. 注意事项

- **路径中避免空格**：若 Windows 目录名含空格，需用引号或反斜杠转义（例如 `"D:/My Data"` 或 `D:/My\ Data`）。
- **性能说明**：通过 `/mnt/` 访问 Windows 文件系统比原生 WSL 文件系统略慢，但对波形生成等计算密集型任务（IO 非瓶颈）影响很小。若需极高 IO 性能，可先在 WSL 本地生成临时文件，任务结束后再移至共享目录。
- **权限问题**：若 WSL 生成的文件在 Windows 中为只读，可在 WSL 中执行 `chmod 666 <文件名>` 添加写权限。
- **删除软链接**：`unlink ~/gw_data` 仅删除链接，不影响原始目录。

### 5. 为什么会采用这种架构？

| 需求                 | 单纯 Windows            | 单纯 Linux/WSL          | 本工作流（双环境）      |
| -------------------- | ----------------------- | ----------------------- | ----------------------- |
| PyCBC / LALSuite     | ❌ 无法原生安装          | ✅ 完美支持              | ✅ WSL 负责              |
| PySR / Julia / CUDA  | ✅ 原生支持              | ⚠️ 驱动/兼容性较复杂     | ✅ Windows 负责          |
| 数据交换             | ——                      | ——                      | ✅ 共享目录 + 软链接     |

通过这种分离，我们**避开了 Windows 上 LALSuite 的安装困境**，也**无需在 Linux 下折腾 GPU 驱动的复杂配置**，同时保留了两边最擅长的工具链。
