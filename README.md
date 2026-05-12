# CUPB Thesis LaTeX

中国石油大学（北京）本科生毕业设计（论文）LaTeX 排版工具。

**Markdown → LaTeX → PDF 一键转换**，严格遵循《中国石油大学（北京）本科生毕业设计（论文）写作指南》格式要求。

## 特性

- 使用 Markdown 写作，自动生成符合学校规范的 `.tex` 文件
- 一键编译为 PDF（XeLaTeX ×3 pass）
- 自动生成：封面、声明页、中英文摘要、目录、前言、结论、致谢
- 支持章节自动编号（第1章、1.1、1.1.1 四级标题）
- 支持 Markdown 表格、有序/无序列表、代码块
- 页眉页脚自动处理（奇偶页不同，前置罗马/正文阿拉伯页码）
- 参考文献支持 GB/T 7714-2005 顺序编码制（gbt7714 宏包）
- 图表编号按章排序（图1-1、表2-3）

## 格式标准

| 项目 | 要求 |
|------|------|
| 纸张 | A4，页边距上/下/左/右 3.0cm，左侧装订 1.0cm |
| 正文字体 | 宋体小四号（12pt），多倍行距 1.25 |
| 一级标题 | 黑体三号居中（第1章、第2章...） |
| 二级标题 | 黑体四号（1.1、1.2...） |
| 三级标题 | 黑体小四号（1.1.1...） |
| 页眉 | 黑体五号，奇数页固定校名，偶数页随章节标题 |
| 页码 | Arial 五号居中，前置部分罗马数字，正文阿拉伯数字 |
| 参考文献 | GB/T 7714-2005 顺序编码制 |

## 文档结构

```
封面 → 声明 → 中文摘要 → 英文摘要 → 目录 → 前言
→ 正文（第1章...）→ 结论 → 主要符号表 → 参考文献 → 附录 → 致谢
```

## 环境要求

- **Python** 3.8+
- **XeLaTeX**（TeX Live 2024+ / MiKTeX / MacTeX）
- **中文字体**：宋体（SimSun）、黑体（SimHei）— Windows 自带；macOS 自带 Songti SC / Heiti SC
- **可选**：`gbt7714` 宏包（GB/T 7714 参考文献格式）

```bash
# 安装 gbt7714（推荐）
tlmgr install gbt7714
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/<your-username>/cupb-thesis-latex.git
cd cupb-thesis-latex
```

### 2. 编写论文（Markdown）

创建 `my-thesis.md`：

```markdown
# 我的论文题目

## 第1章 绪论

研究背景与意义...

## 1.1 国内外研究现状

### 1.1.1 国内研究

文献综述内容...

## 第2章 实验方法

实验设计与方案...

## 结论

总结与展望...

## 参考文献

[1] 作者. 论文题目[J]. 期刊名, 年份, 卷(期): 页码.

## 致谢

感谢导师的悉心指导...
```

### 3. 转换为 LaTeX 并编译

```bash
# 仅生成 .tex 文件
python sample/skill.py my-thesis.md \
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

# 一键生成 .tex 并编译为 PDF
python sample/skill.py my-thesis.md --compile

# 编译已有 .tex 文件
python sample/skill.py my-thesis.tex --compile-only

# 编译后清理临时文件（build/ 目录）
python sample/skill.py my-thesis.md --compile --clean
```

## 命令参考

```bash
python sample/skill.py <输入文件> [选项]
```

| 选项 | 说明 |
|------|------|
| `--compile`, `-c` | 生成 .tex 后自动编译为 PDF |
| `--compile-only`, `-C` | 仅编译已有 .tex 文件 |
| `--clean` | 编译后删除辅助文件目录（`build/`） |
| `--output`, `-o` | 指定输出 .tex 文件路径 |
| `--title` | 论文题目 |
| `--author` | 学生姓名 |
| `--studentid` | 学号 |
| `--college` | 学院名称 |
| `--major` | 专业名称 |
| `--adviser` | 指导教师 |
| `--finishdate` | 完成时间 |
| `--keywords` | 中文关键词（分号分隔） |
| `--en-keywords` | 英文关键词（分号分隔） |
| `--entitle` | 英文论文题目 |

## Markdown 写作指南

### 标题层级

| Markdown | LaTeX 输出 | 说明 |
|----------|-----------|------|
| `# 标题` | `\chapter{标题}` | 第一个 `#` 为论文题目，后续为章标题 |
| `## 标题` | `\section{标题}` | 二级标题（1.1） |
| `### 标题` | `\subsection{标题}` | 三级标题（1.1.1） |
| `#### 标题` | `\subsubsection{标题}` | 四级标题（1.1.1.1） |

### 列表

```markdown
# 有序列表
1. 第一项
2. 第二项

# 无序列表
- 项目一
- 项目二

# 中文编号
（1）第一步
（2）第二步
```

### 表格

```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据 | 数据 | 数据 |
```

### 代码块

````markdown
```python
def hello():
    print("Hello, World!")
```
````

## 文件结构

```
├── sample/                          # 核心工具和示例
│   ├── cupb-thesis.cls              # LaTeX 文档类（格式核心）
│   ├── md2cupb.py                   # Markdown → LaTeX 转换器
│   ├── skill.py                     # 命令行入口工具
│   ├── 中国石油大学论文写作指南.md   # 论文写作指南（Markdown 源）
│   ├── 中国石油大学论文写作指南.tex  # 写作指南 LaTeX 示例输出
│   ├── 中国石油大学论文写作指南.pdf  # 写作指南 PDF 示例输出
│   └── 中国石油大学论文写作指南.docx # 学校原始写作指南文档
├── marketplace/                     # Claude Code 插件分发
├── CLAUDE.md                        # Claude Code 项目说明
├── .gitignore
└── README.md
```

## LaTeX 编译细节

编译流程为 **xelatex ×3**（含 bibtex 可选）：

```bash
xelatex -interaction=nonstopmode -output-directory=build thesis.tex
bibtex build/thesis               # 仅当存在 references.bib 时
xelatex -interaction=nonstopmode -output-directory=build thesis.tex
xelatex -interaction=nonstopmode -output-directory=build thesis.tex
```

辅助文件（`.aux`, `.log`, `.toc` 等）全部输出到 `build/` 目录，最终 PDF 复制到主目录。

## 常见问题

**Q: 编译报错 "font not found"？**

Windows 系统自带 SimSun（宋体）和 SimHei（黑体），确保未删除系统字体。macOS 请确认已安装 Songti SC 和 Heiti SC。

**Q: 参考文献无法正常显示？**

安装 gbt7714 宏包：
```bash
tlmgr install gbt7714
```

或在 `cupb-thesis.cls` 中将 `\bibliographystyle` 改为 `unsrt`。

**Q: 如何添加公式？**

在 Markdown 中直接书写 LaTeX 公式：
```markdown
行内公式 $E=mc^2$，独立公式：

$$ \frac{\partial u}{\partial t} = \alpha \nabla^2 u $$
```

## 许可

本项目仅供中国石油大学（北京）学生撰写毕业论文使用。

格式依据：[中国石油大学（北京）本科生毕业设计（论文）写作指南](sample/中国石油大学论文写作指南.docx)
