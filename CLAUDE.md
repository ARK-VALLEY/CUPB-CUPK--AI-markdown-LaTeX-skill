# CUPB Thesis LaTeX Skill

中国石油大学（北京）本科生毕业设计(论文) LaTeX 排版系统。
严格遵循《中国石油大学（北京）本科生毕业设计（论文）写作指南》格式要求。

## 工作流程

当用户要求使用 LaTeX 排版论文时:
1. 确认用户提供了论文内容的 Markdown 文件 (或直接编写)
2. 运行 `python sample/skill.py <论文.md> [选项]` 生成 `.tex` 文件
3. 可选: `--compile` 自动编译为 PDF

## 格式要点 (已内置在 cupb-thesis.cls 中)

| 项目 | 要求 |
|------|------|
| 纸张 | A4, 页边距上下左右 3.0cm, 左侧装订 1.0cm |
| 正文字体 | 宋体小四号 (12pt), 多倍行距 1.25 |
| 一级标题 | 黑体三号居中 (第1章, 第2章…) |
| 二级标题 | 黑体四号 (1.1, 1.2…) |
| 三级标题 | 黑体小四号 (1.1.1…) |
| 页眉 | 黑体五号, 奇数页固定, 偶数页随章节 |
| 页码 | Arial 五号居中, 前置罗马数字, 正文阿拉伯数字 |
| 参考文献 | GB/T 7714-2005 顺序编码制 |
| 篇幅 | 正文约 1.5 万字, 中英文摘要各 300-500 字 |

## 文档结构

封面 → 声明 → 中文摘要 → 英文摘要 → 目录 → 前言 → 正文(第1章~结论) → 主要符号表 → 参考文献 → 附录 → 致谢

## 命令参考

```bash
# 基本用法: Markdown → .tex
python sample/skill.py thesis.md

# 带论文元信息
python sample/skill.py thesis.md \
  --title "催化裂化工艺优化研究" \
  --author "张三" \
  --studentid "20210001" \
  --college "化学工程学院" \
  --major "化学工程与工艺" \
  --adviser "李四 教授" \
  --finishdate "2026年6月" \
  --keywords "催化裂化；工艺优化；收率" \
  --en-keywords "FCC; process optimization; yield" \
  --entitle "Research on FCC Process Optimization"

# Markdown → .tex → PDF (一键)
python sample/skill.py thesis.md --compile

# 仅编译已有 .tex
python sample/skill.py thesis.tex --compile-only

# 编译并清理辅助文件
python sample/skill.py thesis.md --compile --clean
```

## 编译要求

- XeLaTeX (TeX Live 2024+ 或 MiKTeX)
- 中文字体: 宋体(SimSun), 黑体(SimHei) — Windows 自带
- 可选: gbt7714 宏包 (参考文献 GB/T 7714 格式)
