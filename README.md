# RF Portfolio — 射频天线作品集

> 2026 年暑假 · 6 个 HFSS 仿真项目 · 从单元到阵列到系统级

## 项目清单

| # | 项目 | 频段 | S11 | 关键指标 | 核心技术 |
|---|------|------|-----|----------|----------|
| 1 | **微带贴片天线** | 2.44GHz | −19dB | BW=50MHz, Gain=2dBi | 传输线模型、内嵌馈电、参数优化 |
| 2 | **Wilkinson 功分器** | 2.44GHz | −16.6dB | 等分 −3.67dB | 70.7Ω λ/4 变换、正交布局、Unite 连接 |
| 3 | **端耦合带通滤波器** | 2.44GHz | −13dB | 2-pole Chebyshev, FBW=5% | 间隙耦合、外部 Q、耦合系数 |
| 4 | **2×2 并馈阵列** | 24GHz | −13dB | Gain=4.0dBi | 并联馈电网络、等路径设计、毫米波 |
| 5 | **4×4 串-并混合阵列** | 5.8GHz | −18dB | Gain=8.4dBi, 16 单元 | 串馈 (λg 同相)、并馈 (等幅)、混合拓扑 |
| 6 | **ADS-HFSS 联合仿真** | 2.44GHz | −17.25dB | HFSS=ADS=Python 三方一致 | Touchstone S3P、SnP 黑盒建模、系统级级联 |

## 环境要求

- **Ansys Electronics Desktop 2021 R1** (HFSS)
- **Keysight ADS 2020** (项目 6 联合仿真验证)
- **Python 3.7** (Ansys 自带，路径: `commonfiles/CPython/3_7/winx64/Release/python/python.exe`)
- **IronPython** (AEDT 内嵌脚本引擎，Tools → Run Script)

## 快速开始

### 查看仿真结果

```bash
# 1. 打开 Ansys Electronics Desktop
# 2. File → Open → 选择任一 .aedt 文件
# 3. 在 Project Manager 中展开 Results → 右键已有报告 → View
# 4. 或者: Results → Create Modal Solution Data Report → 新建 S 参数图
```

每个 `.aedt` 文件包含完整模型 + 仿真结果，直接打开即可查看：
- **S 参数曲线** (S11/S21/S31)
- **3D 辐射方向图** (阵列项目: Array24G_v1, Array58G_v1)
- **优化迭代记录** (项目 Properties 中的设计变量)

### 重新求解

```bash
# 在 AEDT 中:
# 1. 打开 .aedt 文件
# 2. HFSS → Validation Check (确认模型有效)
# 3. 右键 Setup1 → Analyze (开始求解)
```

### 运行建模脚本

```bash
# 在 AEDT 中:
# 1. Tools → Run Script → 选择 scripts/ 下的 .py 文件
# 2. 脚本自动创建新项目 + 建模 + 设置边界和端口
# 3. 手动添加分析设置 (Script 会打印提示)  → Analyze

# 或命令行 (以 Wilkinson 为例):
& "D:\Program Files\AnsysEM\AnsysEM21.1\Win64\ansysedt.exe" -RunScript "C:\Users\deng\Documents\Ansoft\scripts\build_wilkinson.py"
```

### 联合仿真分析

```bash
# 1. 在 HFSS 中打开 Wilkinson_v1.aedt → 求解
# 2. Results → Export → Touchstone → Wilkinson.s3p
# 3. 运行 Python 分析:
python scripts/co_sim.py
# 输出: 三方结果对照 + 4路功分器级联预测 + 可视化报告
```

### 生成项目报告

```bash
python scripts/gen_report.py PatchAntenna    # 贴片天线报告
python scripts/gen_report.py Wilkinson        # 功分器报告
python scripts/gen_report.py Filter           # 滤波器报告
python scripts/gen_report.py Array24G         # 2×2 阵列报告
# 报告输出到桌面 (HTML 格式)
```

## 文件结构

```
Documents/Ansoft/
├── README.md                    # 本文件
├── .gitignore                   # 排除结果文件/临时文件
│
├── PatchAntenna_v1.aedt         # 项目1: 微带贴片天线 (47×39mm)
├── Wilkinson_v1.aedt            # 项目2: Wilkinson 功分器 (50×60mm)
├── Filter_v1.aedt               # 项目3: 端耦合滤波器 (50×90mm)
├── Array24G_v1.aedt             # 项目4: 2×2 并馈阵列 (30×30mm)
├── Array58G_v1.aedt             # 项目5: 4×4 串-并阵列 (~114×120mm)
├── Wilkinson.s3p                # 项目6: Touchstone S 参数导出
│
├── reports/                     # 项目报告 (HTML)
│   ├── PatchAntenna_v1_Report.html
│   ├── Wilkinson_v1_Report.html
│   ├── Filter_v1_Report.html
│   ├── Array24G_v1_Report.html
│   ├── Array58G_v1_Report.html
│   └── CoSim_v1_Report.html
│
├── scripts/                     # 建模脚本 + 分析工具
│   ├── build_wilkinson.py       # Wilkinson 功分器建模
│   ├── build_filter.py          # 端耦合滤波器建模
│   ├── build_array24g.py        # 2×2 阵列建模
│   ├── build_58g_array.py       # 4×4 阵列建模
│   ├── co_sim.py                # S3P 解析 + 级联分析
│   ├── gen_report.py            # HTML 报告生成器
│   ├── test_thru.py             # 2端口直通线诊断模板
│   └── test_3port.py            # 3端口诊断模板
│
└── templates/                   # 项目笔记模板
    └── project_note_template.md
```

## 工程方法论

每个项目的迭代过程遵循统一的工程方法：

1. **单单元诊断** → 验证基础设计在目标频率正常谐振
2. **逐步扩展** → 单贴片 → 1×N 线阵 → M×N 面阵
3. **参数优化** → 每次只改一个变量，清晰因果关系
4. **bug 日志驱动** → 25+ 条已知问题，新项目开始前逐条过

## 关键发现

- **旋转破坏 Lumped Port 耦合** — 端口面必须垂直于走线（6 轮迭代定位根因）
- **AEDT 2021 Lumped Port 要求 h ≥ 1.6mm** — 0.508mm Rogers 5880 端口完全失效
- **2D 重叠 ≠ 电气连接** — Unite 操作保证单导体连通性
- **串馈间距 = λg** — 保证同相激励，是相控阵雷达基础拓扑
- **S 参数黑盒建模** — HFSS → Touchstone → ADS/Python 三方验证一致

## 工具链

`HFSS` `ADS 2020` `Python` `IronPython` `Git` `Touchstone`

## 关于我

二本电子信息工程大三，不考研。暑假用 6 个项目证明动手能力——从设计公式到 HFSS 建模到参数优化到报告输出全流程独立完成。目标车载/卫星通信方向射频天线岗。

📧 deng@example.com
🔗 [github.com/dfg-ai/rf-portfolio](https://github.com/dfg-ai/rf-portfolio)
