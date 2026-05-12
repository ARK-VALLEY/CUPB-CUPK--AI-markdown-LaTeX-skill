#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国石油大学（北京）本科生毕业设计(论文)
Markdown → LaTeX 转换器

用法:
  python md2cupb.py input.md [output.tex]

生成的 .tex 文件用 XeLaTeX 编译:
  xelatex output.tex
  bibtex output
  xelatex output.tex
  xelatex output.tex
"""

import re
import sys
import os
import argparse
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ---------------------------------------------------------------------------
#  中英文标题映射 (用于前置部分)
# ---------------------------------------------------------------------------
CHAPTER_PATTERNS = {
    "abstract":    "摘要",
    "enabstract":  "Abstract",
    "toc":         "目录",
    "preface":     "前言",
    "conclusion":  "结论",
    "reference":   "参考文献",
    "appendix":    "附录",
    "acknowledge": "致谢",
    "symbol":      "主要符号表",
}


# ---------------------------------------------------------------------------
#  转义 LaTeX 特殊字符
# ---------------------------------------------------------------------------
LATEX_ESCAPE = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\^{}",
    "\\": r"\textbackslash{}",
}


def escape_latex(text: str) -> str:
    """转义普通文本中的 LaTeX 特殊字符 — 注意顺序: \ 必须最先处理."""
    # 先处理 \, 用占位符避免后续字符被二次转义
    placeholder = "\x00BACKSLASH\x00"
    text = text.replace("\\", placeholder)
    # 处理其他特殊字符
    for char, replacement in LATEX_ESCAPE.items():
        if char != "\\":
            text = text.replace(char, replacement)
    # 还原 \
    text = text.replace(placeholder, r"\textbackslash{}")
    return text


# ---------------------------------------------------------------------------
#  内联格式转换
# ---------------------------------------------------------------------------
def convert_inline(text: str) -> str:
    """转换 Markdown 内联格式为 LaTeX."""
    if not text:
        return text
    # 粗体+斜体
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', text)
    # 粗体
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    # 斜体
    text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
    return text


# ---------------------------------------------------------------------------
#  段落处理
# ---------------------------------------------------------------------------
def process_paragraph(text: str) -> str:
    """处理段落文本, 转义 + 转换内联格式."""
    text = convert_inline(text)
    # 转义非命令的 LaTeX 特殊字符
    # 保护已有 LaTeX 命令
    parts = re.split(r'(\\[a-zA-Z]+\{.*?\})', text)
    result = []
    for part in parts:
        if part.startswith("\\") and "{" in part:
            result.append(part)
        else:
            result.append(escape_latex(part))
    return "".join(result)


# ---------------------------------------------------------------------------
#  列表检测与转换
# ---------------------------------------------------------------------------
def is_enumerate_line(line: str) -> bool:
    """检测是否为有序列表项."""
    return bool(re.match(r'^(\d+)[\.\．]\s', line))


def is_itemize_line(line: str) -> bool:
    """检测是否为无序列表项."""
    return bool(re.match(r'^[-\*]\s', line))


def is_chinese_enum(line: str) -> bool:
    """检测中文编号列表: (1), （1）, ①, a. 等."""
    return bool(re.match(r'^[（(]\d+[）)]\s?', line))


# ---------------------------------------------------------------------------
#  主转换函数
# ---------------------------------------------------------------------------
def convert_md_to_tex(md_content: str, metadata: dict = None) -> str:
    """将 Markdown 内容转换为完整的 LaTeX 文档."""
    if metadata is None:
        metadata = {}

    lines = md_content.split("\n")

    # 输出缓冲区 (正文部分)
    tex = []
    # 状态追踪
    in_list = 0           # 有序列表嵌套深度
    in_itemize = 0        # 无序列表嵌套深度
    in_cn_enum = 0        # 中文编号列表嵌套深度
    in_table = False
    in_code_block = False
    first_h1 = True       # 第一个 H1 作为文档标题, 不输出

    table_rows = []
    abstract_lines = []
    enabstract_lines = []

    def close_all_lists():
        """关闭所有打开的列表环境."""
        nonlocal in_list, in_itemize, in_cn_enum
        for _ in range(in_list):
            tex.append("\\end{enumerate}")
        for _ in range(in_itemize):
            tex.append("\\end{itemize}")
        for _ in range(in_cn_enum):
            tex.append("\\end{enumerate}")
        in_list = 0
        in_itemize = 0
        in_cn_enum = 0

    def close_lists_except(target):
        """关闭除 target 外的所有列表."""
        nonlocal in_list, in_itemize, in_cn_enum
        if target != "list":
            for _ in range(in_list):
                tex.append("\\end{enumerate}")
            in_list = 0
        if target != "itemize":
            for _ in range(in_itemize):
                tex.append("\\end{itemize}")
            in_itemize = 0
        if target != "cn_enum":
            for _ in range(in_cn_enum):
                tex.append("\\end{enumerate}")
            in_cn_enum = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # --- 代码块 ---
        if stripped.startswith("```"):
            if in_code_block:
                tex.append("\\end{verbatim}")
                tex.append("")
                in_code_block = False
            else:
                close_all_lists()
                tex.append("\\begin{verbatim}")
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            tex.append(line)
            i += 1
            continue

        # --- 空行 ---
        if not stripped:
            # 空行不关闭列表, 允许列表项之间有空白
            tex.append("")
            i += 1
            continue

        # --- 标题检测 (H1 - H6) ---
        heading_match = re.match(r'^(#{1,6})\s+(.+)', stripped)
        if heading_match:
            close_all_lists()

            level = len(heading_match.group(1))
            title_text = process_paragraph(heading_match.group(2))

            if level == 1:
                if first_h1:
                    # 第一个 H1 → 文档标题 (存入 metadata)
                    first_h1 = False
                    tex.append(f"% 文档标题: {title_text}")
                    tex.append("")
                else:
                    # 后续 H1 → chapter*
                    tex.append(f"\\chapter*{{{title_text}}}")
                    tex.append("")
            elif level == 2:
                tex.append(f"\\section{{{title_text}}}")
                tex.append("")
            elif level == 3:
                tex.append(f"\\subsection{{{title_text}}}")
                tex.append("")
            elif level == 4:
                tex.append(f"\\subsubsection{{{title_text}}}")
                tex.append("")
            else:
                tex.append(f"\\paragraph{{{title_text}}}")
                tex.append("")

            i += 1
            continue

        # --- 水平线 ---
        if stripped in ("---", "***", "___"):
            close_all_lists()
            tex.append("\\bigskip\\hrule\\bigskip")
            i += 1
            continue

        # --- 有序列表: "1. ", "1．" (中文全角点号, 后可能无空格) ---
        enum_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        enum_fw_match = re.match(r'^(\d+)\．\s*(.+)', stripped)  # 全角点号
        if enum_match or enum_fw_match:
            m = enum_match or enum_fw_match
            close_lists_except("list")
            if in_list == 0:
                tex.append("\\begin{enumerate}[label=\\arabic*.]")
                in_list = 1
            item_text = process_paragraph(m.group(2))
            tex.append(f"  \\item {item_text}")
            i += 1
            continue

        # --- 中文编号列表: (1), （1） ---
        cn_enum_match = re.match(r'^[（(](\d+)[）)]\s*(.+)', stripped)
        if cn_enum_match:
            close_lists_except("cn_enum")
            if in_cn_enum == 0:
                tex.append("\\begin{enumerate}[label=（\\arabic*）]")
                in_cn_enum = 1
            item_text = process_paragraph(cn_enum_match.group(2))
            tex.append(f"  \\item {item_text}")
            i += 1
            continue

        # --- 圆圈数字: ① ② ③ ---
        circle_match = re.match(r'^([①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳])\s*(.+)', stripped)
        if circle_match:
            close_lists_except("itemize")
            if in_itemize == 0:
                tex.append("\\begin{itemize}")
                in_itemize = 1
            tex.append(f"  \\item[{circle_match.group(1)}] {process_paragraph(circle_match.group(2))}")
            i += 1
            continue

        # --- 无序列表: "- ", "* " ---
        itemize_match = re.match(r'^[-\*]\s+(.+)', stripped)
        if itemize_match:
            close_lists_except("itemize")
            if in_itemize == 0:
                tex.append("\\begin{itemize}")
                in_itemize = 1
            tex.append(f"  \\item {process_paragraph(itemize_match.group(1))}")
            i += 1
            continue

        # --- 表格 ---
        if "|" in stripped and stripped.startswith("|"):
            if not in_table:
                close_all_lists()
                table_rows = []
                in_table = True
            table_rows.append(stripped)
            i += 1
            if i < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i].strip()):
                i += 1
            continue
        elif in_table:
            tex.extend(convert_table(table_rows))
            tex.append("")
            table_rows = []
            in_table = False

        # --- 普通段落 ---
        processed = process_paragraph(stripped)
        tex.append(processed)
        tex.append("")
        i += 1

    # 关闭未结束的列表
    close_all_lists()

    # -------------------------------------------------------------------
    #  组装完整文档
    # -------------------------------------------------------------------
    # 从 tex 中提取被注释掉的文档标题
    doc_title = metadata.get("title", "")
    for line in tex:
        m = re.match(r'^%\s*文档标题:\s*(.+)', line)
        if m and not doc_title:
            doc_title = m.group(1).strip()
            break

    title    = doc_title or metadata.get("title", "论文题目")
    author   = metadata.get("author", "学生姓名")
    studentid = metadata.get("studentid", "")
    college  = metadata.get("college", "学院名称")
    major    = metadata.get("major", "专业名称")
    adviser  = metadata.get("adviser", "指导教师")
    finishdate = metadata.get("finishdate", "年\\quad 月\\quad 日")
    cn_keywords = metadata.get("keywords", "关键词1；关键词2；关键词3")
    en_keywords = metadata.get("en_keywords", "keyword1; keyword2; keyword3")
    entitle  = metadata.get("entitle", "English Title")

    preamble = f"""% !TEX program = xelatex
% =============================================================================
%  中国石油大学（北京）本科生毕业设计(论文)
%  由 md2cupb.py 自动生成
%  编译: xelatex → bibtex → xelatex → xelatex
% =============================================================================

\\documentclass{{cupb-thesis}}

% ---------------------------------------------------------------------------
%  论文元信息 (请根据实际情况修改)
% ---------------------------------------------------------------------------
\\thesititle{{{title}}}
\\thesiauthor{{{author}}}
\\thesistudentid{{{studentid}}}
\\thesicollege{{{college}}}
\\thesimajor{{{major}}}
\\thesiadviser{{{adviser}}}
\\thesifinishdate{{{finishdate}}}
\\thesientitle{{{entitle}}}
\\cnkeywords{{{cn_keywords}}}
\\enkeywords{{{en_keywords}}}

% ---------------------------------------------------------------------------
%  参考文献文件 (如果有 .bib 文件, 在此指定)
% ---------------------------------------------------------------------------
% \\addbibresource{{references.bib}}

\\begin{{document}}

% ===========================================================================
%  前置部分
% ===========================================================================

%% --- 中文封面 ---
\\makecover

%% --- 声明页 ---
\\makestatement

%% --- 中文摘要 ---
\\begin{{cnabstract}}
{chr(10).join('  ' + l for l in abstract_lines) if abstract_lines else '（请在此处填写中文摘要，300-500字）'}
\\end{{cnabstract}}

%% --- 英文摘要 ---
\\begin{{enabstract}}
{chr(10).join('  ' + l for l in enabstract_lines) if enabstract_lines else '(Please write the English abstract here, 300-500 words.)'}
\\end{{enabstract}}

%% --- 目录 ---
\\tableofcontents

%% --- 前言 ---
\\begin{{preface}}
（请在此处填写前言内容）
\\end{{preface}}

% ===========================================================================
%  正文 (从第一章开始, 页码用阿拉伯数字)
% ===========================================================================
\\mainmatterstart
"""

    # 正文内容 — 包含 \mainmatterstart 之后所有内容
    body = "\n".join(tex) if tex else "% 正文内容"

    postamble = f"""
% ===========================================================================
%  后置部分
% ===========================================================================

%% --- 结论 ---
\\begin{{conclusion}}
（请在此处填写论文结论）
\\end{{conclusion}}

%% --- 主要符号表 (如需要) ---
% \\begin{{symbollist}}
%   $\\alpha$ & 角度 \\\\
%   $\\beta$  & 系数 \\\\
% \\end{{symbollist}}

%% --- 参考文献 ---
% \\makereference{{references}}

%% --- 附录 ---
% \\begin{{theappendix}}
%   \\chapter{{附录标题}}
%   附录内容...
% \\end{{theappendix}}

%% --- 致谢 ---
\\begin{{acknowledgement}}
（请在此处填写致谢内容，限300字）
\\end{{acknowledgement}}

\\end{{document}}
"""

    return preamble + body + postamble


# ---------------------------------------------------------------------------
#  辅助函数
# ---------------------------------------------------------------------------
def is_marker(text: str, marker: str) -> bool:
    """检查文本是否匹配某个标记."""
    pattern = CHAPTER_PATTERNS.get(marker, marker)
    return pattern.lower() in text.lower()


def convert_table(rows: list) -> list:
    """将 Markdown 表格行转换为 LaTeX tabular."""
    if not rows:
        return []

    # 解析行
    parsed = []
    ncols = 0
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        ncols = max(ncols, len(cells))
        parsed.append(cells)

    # 补全列数
    for row in parsed:
        while len(row) < ncols:
            row.append("")

    # 生成 LaTeX 表格
    col_spec = "c" * ncols
    result = [
        "\\begin{table}[htbp]",
        "  \\centering",
        f"  \\begin{{tabular}}{{{col_spec}}}",
        "    \\toprule",
    ]

    for idx, row in enumerate(parsed):
        latex_row = " & ".join(process_paragraph(c) for c in row)
        result.append(f"    {latex_row} \\\\")
        if idx == 0:
            result.append("    \\midrule")

    result.extend([
        "    \\bottomrule",
        "  \\end{tabular}",
        "\\end{table}",
    ])
    return result


# ---------------------------------------------------------------------------
#  主入口
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="中国石油大学（北京）本科生毕业设计(论文) Markdown → LaTeX 转换器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python md2cupb.py thesis.md
  python md2cupb.py thesis.md output.tex
  python md2cupb.py thesis.md --title "我的论文题目" --author "张三"
        """,
    )
    parser.add_argument("input", help="输入的 Markdown 文件")
    parser.add_argument("output", nargs="?", help="输出的 .tex 文件 (默认与输入同名)")
    parser.add_argument("--title", help="论文题目")
    parser.add_argument("--author", help="学生姓名")
    parser.add_argument("--studentid", help="学号")
    parser.add_argument("--college", help="学院")
    parser.add_argument("--major", help="专业")
    parser.add_argument("--adviser", help="指导教师")
    parser.add_argument("--finishdate", help="完成时间")
    parser.add_argument("--keywords", help="中文关键词 (分号分隔)")
    parser.add_argument("--en-keywords", help="英文关键词 (分号分隔)")
    parser.add_argument("--entitle", help="英文论文题目")

    args = parser.parse_args()

    # 读取 Markdown 文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found - {args.input}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 收集元数据
    metadata = {}
    for key in ["title", "author", "studentid", "college", "major",
                "adviser", "finishdate", "keywords", "en_keywords", "entitle"]:
        val = getattr(args, key, None)
        if val:
            if key == "en_keywords":
                metadata["en_keywords"] = val
            else:
                metadata[key] = val

    # 转换
    tex_content = convert_md_to_tex(md_content, metadata)

    # 输出
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".tex")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    print(f"Done: {output_path}")
    print(f"  Compile: xelatex {output_path.name}")
    print(f"  Full: xelatex -> bibtex -> xelatex -> xelatex")


if __name__ == "__main__":
    main()
