# HFSS 项目作品集 — 射频/天线工程

## 背景

- **目标**: 秋招射频/天线/电磁仿真工程师岗位
- **策略**: 以项目作品集 + 动手能力破局，用实际能力补学历短板
- **时间线**: 2026年暑假（7-9月），9月秋招
- **协作模式**: Claude Code AI 辅助 — 教学、设计、脚本、文档

## 环境

| 工具 | 路径 |
|------|------|
| Ansys Electronics Desktop 2021 R1 | `D:\Program Files\AnsysEM\AnsysEM21.1\Win64\ansysedt.exe` |
| IronPython | `D:\Program Files\AnsysEM\AnsysEM21.1\Win64\commonfiles\IronPython\ipy64.exe` |
| CPython 3.7 | `D:\Program Files\AnsysEM\AnsysEM21.1\Win64\commonfiles\CPython\3_7\winx64\Release\python\python.exe` |
| ADS 2020 | `D:\Program Files\Keysight\ADS2020\` |
| ADS 2025 U2 | `D:\Program Files\Keysight\ADS2025\` |

## 项目目录结构

```
C:\Users\deng\Documents\Ansoft\
├── OptimTee.aedt          # T型波导功分器（参数化+优化，已完成）
├── Tee3.aedt              # T型波导（双频+场可视化，已完成）
├── Project3.aedt          # 微带结构 FR4+铜（已完成）
├── Project2.aedt          # 螺旋天线（⚠️ 半成品，文件缺失！需重建）
├── PersonalLib/           # 个人材料库
├── temp/                  # 临时文件
└── CLAUDE.md              # 本文件
```

## 工作规范

### 文件命名
- 项目文件: `ProjectName_v1.aedt`, `ProjectName_v2.aedt` ...
- 配套报告: `ProjectName_v1_Report.md`
- 配套脚本: `ProjectName_Script.py`

### 版本管理
- 每次重大修改前保存新版本（增量版本号）
- Git 提交: 完成一个版本 → commit，附有意义的 message
- `.gitignore`: 排除 `.aedtresults/`、`temp/`、`*.lock`

### 每个完成项目必须产出
1. **.aedt 文件** — 完整可求解
2. **报告** — 设计目标、方法、过程、结果、结论
3. **脚本**（如有自动化价值）— IronPython 或 CPython

## 常用命令

```powershell
# 启动 Electronics Desktop
& "D:\Program Files\AnsysEM\AnsysEM21.1\Win64\ansysedt.exe"

# 用 IronPython 跑脚本
& "D:\Program Files\AnsysEM\AnsysEM21.1\Win64\commonfiles\IronPython\ipy64.exe" script.py

# 命令行批量求解
& "D:\Program Files\AnsysEM\AnsysEM21.1\Win64\ansysedt.exe" -BatchSolve project.aedt

# 带脚本运行
& "D:\Program Files\AnsysEM\AnsysEM21.1\Win64\ansysedt.exe" -RunScript script.py
```

## 学习路线（四阶段）

1. **Phase 1 基础** (1-2周): 跑通现有项目，理解每个操作步骤，建立 Git 管理
2. **Phase 2 深入** (3-6周): HFSS/Maxwell/SIwave 模块逐个攻克
3. **Phase 3 自动化** (7-12周): IronPython 脚本库、参数化模板、批量求解
4. **Phase 4 进阶**: ADS-HFSS 联合仿真、多物理场

## Claude 的角色

- **教师**: 解释概念、引导操作、答疑
- **设计助手**: 辅助初始设计计算、优化建议
- **脚本工程师**: 编写自动化脚本
- **文档助手**: 生成报告框架、整理笔记

## 关键约束

- 不考研，直接就业（既定决策）
- 暑假时间窗口有限（7月初到9月）
- 学历是短板，作品集和动手能力必须突出
- 每个项目都要能放进简历和面试展示
