# HFSS 项目作品集 — 射频/天线工程

## 背景

- **目标**: 秋招射频/天线/电磁仿真工程师岗位（2026年9月）
- **策略**: 以项目作品集 + 动手能力破局，用实际能力补学历短板
- **时间线**: 2026年暑假（7-9月）
- **协作模式**: Claude Code AI 辅助 — 教学、设计、脚本、文档
- **记忆系统**: `C:\Users\deng\.claude\projects\D--Program-Files-AnsysEM\memory\`

## 环境

| 工具 | 路径 |
|------|------|
| Ansys Electronics Desktop 2021 R1 | `D:\Program Files\AnsysEM\AnsysEM21.1\Win64\ansysedt.exe` |
| IronPython | `D:\Program Files\AnsysEM\AnsysEM21.1\Win64\commonfiles\IronPython\ipy64.exe` |
| CPython 3.7 | `D:\Program Files\AnsysEM\AnsysEM21.1\Win64\commonfiles\CPython\3_7\winx64\Release\python\python.exe` |
| ADS 2020 | `D:\Program Files\Keysight\ADS2020\` |
| ADS 2025 U2 | `D:\Program Files\Keysight\ADS2025\` |

## 目录结构

```
C:\Users\deng\Documents\Ansoft\
├── OptimTee.aedt          # ⚠️ 练手项目，不投入时间
├── Tee3.aedt              # ⚠️ 练手项目
├── Project3.aedt          # ⚠️ 练手项目
├── Project2.aedtresults/  # ⚠️ 练手残留（.aedt 已丢失）
├── PersonalLib/           # 个人材料库
├── temp/                  # 临时文件
├── templates/             # 项目笔记模板
├── CLAUDE.md              # 本文件
└── .gitignore
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
2. **报告** — 使用 `templates/project_note_template.md`，涵盖设计目标→方法→结果→结论
3. **脚本**（如有自动化价值）— IronPython 或 CPython

## 当前状态

- **Phase**: 基础搭建完成，待开始第一个正式作品
- **下一个决策**: 选第一个项目方向（微带贴片天线 / Wilkinson功分器 / Vivaldi天线 / 带通滤波器）
- **记忆文件**: 7个 memory 文件已建立，MEMORY.md 索引已更新

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

## Claude 的角色

- **教师**: 解释概念、引导操作、答疑（做中学优先）
- **设计助手**: 辅助初始设计计算、优化建议
- **脚本工程师**: 编写自动化脚本
- **文档助手**: 生成报告框架、整理笔记

## 关键约束

- 不考研，直接就业（既定决策）
- 暑假时间窗口有限（7月初到9月）
- 学历是短板，作品集和动手能力必须突出
- 每个项目都要能放进简历和面试展示
- 练手项目不占用时间 — 直接做正式作品
