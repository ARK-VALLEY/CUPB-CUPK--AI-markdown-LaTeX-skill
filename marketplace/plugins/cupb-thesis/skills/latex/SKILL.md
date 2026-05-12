---
name: latex
description: 将 Markdown 论文文件转换为严格符合中国石油大学（北京）本科生毕业设计(论文)写作指南的 LaTeX 文件并编译为 PDF。当用户提到 "latex排版"、"tex格式"、"编译tex"、"生成pdf"、"论文排版"、"转换tex" 时应使用此 skill。也用于处理 .md 转 .tex、latex 编译、论文格式调整等需求。
argument-hint: <论文.md> [--compile] [--clean] [--title ...] [--author ...]
user-invocable: true
---

# CUPB Thesis LaTeX Skill

中国石油大学（北京）本科生毕业设计(论文) LaTeX 排版系统。
严格遵循《中国石油大学（北京）本科生毕业设计（论文）写作指南》格式要求。

## 工具定位

工具文件打包在插件 `tools/` 目录中。执行时先定位：

- **项目本地** (优先): 检查当前目录下是否有 `sample/skill.py`
- **插件缓存** (通用): `~/.claude/plugins/cache/cupb-tools/cupb-thesis/tools/skill.py`

## 使用方式

用户调用时传入的参数为: `$ARGUMENTS`

```bash
# 定位工具路径 (二选一)
# 优先用项目本地的 sample/skill.py，否则用插件缓存中的 tools/skill.py

# Markdown → .tex + PDF (一键)
python <tools>/skill.py <论文.md> --compile \
  --title "题目" --author "姓名" --studentid "学号" \
  --college "学院" --major "专业" --adviser "指导教师" \
  --finishdate "20xx年x月" \
  --keywords "关键词1；关键词2" \
  --en-keywords "keyword1; keyword2" \
  --entitle "English Title"

# 仅生成 .tex
python <tools>/skill.py <论文.md> --title "题目" --author "姓名" ...

# 仅编译已有 .tex
python <tools>/skill.py <论文.tex> --compile-only

# 编译后清理临时文件
python <tools>/skill.py <论文.md> --compile --clean
```

## 文档结构 (自动生成)

封面 → 声明 → 中文摘要 → 英文摘要 → 目录 → 前言 → 正文(第1章~结论) → 参考文献 → 附录 → 致谢

## 格式要点

| 项目 | 要求 |
|------|------|
| 纸张 | A4, 页边距 3.0cm, 左侧装订 1.0cm |
| 正文 | 宋体小四号 (12pt), 多倍行距 1.25 |
| 一级标题 | 黑体三号居中 (第1章, 第2章…) |
| 二级标题 | 黑体四号 (1.1, 1.2…) |
| 三级标题 | 黑体小四号 (1.1.1…) |
| 页眉 | 黑体五号, 奇/偶页不同 |
| 页码 | 前置罗马数字, 正文阿拉伯数字 |
| 参考文献 | GB/T 7714-2005 顺序编码制 |

## 执行步骤

1. 定位工具目录：先找项目 `sample/skill.py`，没有则用 `~/.claude/plugins/cache/cupb-tools/cupb-thesis/tools/skill.py`
2. 确认 Markdown 文件存在
3. 收集元信息 (题目、姓名、学号等)，未提供的用占位符
4. 运行转换脚本生成 .tex
5. 若 `--compile`，执行 xelatex ×3 编译，辅助文件进 `build/`
6. 报告结果

## 编译要求

- XeLaTeX (TeX Live / MacTeX 2024+)
- 中文字体: Windows 自带 SimSun/SimHei, macOS 自带 Songti SC/Heiti SC
- 可选: `tlmgr install gbt7714` (GB/T 7714 参考文献格式)
