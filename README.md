# RF Portfolio — 射频天线作品集

> 2026 年暑假 · 6 个 HFSS 仿真项目 · 从单元到阵列到系统级

## 项目清单

| # | 项目 | 频段 | 关键指标 | 核心技术 |
|---|------|------|----------|----------|
| 1 | **微带贴片天线** | 2.44GHz | S11=−19dB, BW=50MHz | 传输线模型、内嵌馈电、参数优化 |
| 2 | **Wilkinson 功分器** | 2.44GHz | 等分 −3.67dB, S11=−16.6dB | 70.7Ω λ/4 变换、正交布局、Unite 连接 |
| 3 | **端耦合带通滤波器** | 2.44GHz | 2-pole Chebyshev, S11=−13dB | 间隙耦合、外部 Q、耦合系数 |
| 4 | **2×2 并馈阵列** | 24GHz | Gain=4.0dBi | 并联馈电网络、等路径设计、毫米波 |
| 5 | **4×4 串-并混合阵列** | 5.8GHz | Gain=8.4dBi, 16 单元 | 串馈 (λg 同相)、并馈 (等幅)、混合拓扑 |
| 6 | **ADS-HFSS 联合仿真** | 2.44GHz | 三方验证一致 | Touchstone S3P、SnP 黑盒建模、系统级级联 |

## 工具链

`HFSS` `ADS 2020` `Python` `Git` `IronPython`

## 文件说明

```
Documents/Ansoft/
├── PatchAntenna_v1.aedt    # 项目1: 贴片天线
├── Wilkinson_v1.aedt       # 项目2: 功分器
├── Filter_v1.aedt          # 项目3: 滤波器
├── Array24G_v1.aedt        # 项目4: 2×2 阵列
├── Array58G_v1.aedt        # 项目5: 4×4 阵列
├── Wilkinson.s3p           # 项目6: Touchstone 导出
├── scripts/                # 建模脚本 + 分析工具
│   ├── build_wilkinson.py
│   ├── build_filter.py
│   ├── build_array24g.py
│   ├── build_58g_array.py
│   ├── co_sim.py           # S3P 解析 + 级联分析
│   └── gen_report.py       # HTML 报告生成器
├── templates/              # 项目笔记模板
└── README.md
```

## 关键发现

- **旋转破坏 Lumped Port 耦合** — 端口面必须垂直于走线（6 轮迭代定位）
- **AEDT 2021 Lumped Port 要求 h≥1.6mm** — 0.508mm Rogers 5880 端口不可用
- **2D 重叠 ≠ 电气连接** — Unite 操作保证单导体
- **串馈间距 = λg** — 保证同相激励，是相控阵基础
- **S 参数黑盒建模** — HFSS→S3P→ADS/Python 三方验证

## 关于我

二本电子信息工程大三，不考研。暑假用 6 个项目证明动手能力——从设计公式到建模仿真到参数优化到报告输出全流程独立完成。目标车载/卫星通信方向射频天线岗。

📧 deng@example.com
