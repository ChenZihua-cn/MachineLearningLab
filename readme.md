# [原仓库链接](https://github.com/iphysresearch/UndergradResearchLab)

此处我选择题目1和题目2来练习机器学习，。
> 或许可能写一个kaggle上的泰坦尼克号的练习题

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

### PySR 引力波噪声研究

符号回归（PySR）能否在噪声中还原已知波形物理定律？实验分三步：[详细设计](./PySR_GW_Noise_Research/)

| 步骤 | 目标 |
|------|------|
| Part 1 | 高斯噪声基准：纯净→加噪的SR恢复能力曲线 |
| Part 2 | 真实探测器噪声（LIGO敏感曲线） |
| Part 3 | 瞬态Glitch过拟合测试 |

## 环境说明

本项目采用 Windows + WSL 双环境：**PyCBC/LALSuite 运行在 WSL**，**PySR/PyTorch 运行在 Windows**。两者通过共享目录交换数据：

```bash
# WSL 中：软链接指向 Windows 目录
ln -s /mnt/d/gw_shared ~/gw_data
```

WSL 端波形生成后保存到共享目录，Windows 端直接读取即可。
