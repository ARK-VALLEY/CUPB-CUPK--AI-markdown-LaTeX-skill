#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国石油大学（北京）本科生毕业设计(论文) LaTeX 排版 Skill
============================================================
用法:
  python skill.py <input.md> [选项]

本 skill 将 Markdown 论文文件转换为严格符合 《中国石油大学（北京）
本科生毕业设计（论文）写作指南》 格式要求的 LaTeX (.tex) 文件,
并可选自动编译生成 PDF。

示例:
  # 只生成 .tex
  python skill.py thesis.md

  # 生成 .tex 并编译
  python skill.py thesis.md --compile

  # 指定论文信息
  python skill.py thesis.md --title "催化裂化工艺优化" --author "张三" --studentid "20210001"

  # 只编译已有的 .tex 文件
  python skill.py thesis.tex --compile-only

格式要求 (自动实现):
  - A4 纸, 上下左右页边距 3.0cm, 左侧 1.0cm 装订线
  - 正文: 宋体小四号 (12pt), 多倍行距 1.25
  - 一级标题: 黑体三号居中 (第1章, 第2章...)
  - 二级标题: 黑体四号 (1.1, 1.2...)
  - 三级标题: 黑体小四号 (1.1.1...)
  - 页眉: 黑体五号, 奇数页固定, 偶数页随章节标题
  - 页码: Arial 五号居中, 前置部分用罗马数字
  - 参考文献: GB/T 7714-2005 顺序编码制
  - 封面、声明页、中英文摘要、目录、前言、结论、致谢
"""

import subprocess
import sys
import os
import shutil
import argparse
from pathlib import Path

# 确保 md2cupb.py 在同一目录
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))

from md2cupb import convert_md_to_tex


def compile_tex(tex_path: Path) -> bool:
    """编译 .tex 文件生成 PDF (xelatex → bibtex → xelatex → xelatex).
    辅助文件 (.aux .log .toc 等) 全部输出到 build/ 子目录, PDF 留在主目录.
    """
    tex_dir = tex_path.parent
    tex_name = tex_path.stem
    build_dir = tex_dir / "build"

    build_dir.mkdir(exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  编译: {tex_name}.tex")
    print(f"  临时文件: {build_dir}/")
    print(f"{'='*60}")

    # 检查 xelatex
    try:
        subprocess.run(["xelatex", "--version"],
                       capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: xelatex not found. 请安装 TeX Live 或 MiKTeX.")
        return False

    xelatex_args = [
        "xelatex",
        "-interaction=nonstopmode",
        "-output-directory=build",
        f"{tex_name}.tex",
    ]

    # 第一遍
    print("\n[1/4] xelatex (第一遍)...")
    result = subprocess.run(
        xelatex_args, cwd=str(tex_dir),
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        print("  (可能有警告, 继续编译)")

    # bibtex (如果有 .bib 文件)
    bib_path = tex_dir / f"{tex_name}.bib"
    aux_in_build = build_dir / f"{tex_name}.aux"
    if bib_path.exists():
        print("[2/4] bibtex...")
        subprocess.run(["bibtex", str(aux_in_build)],
                       capture_output=True, encoding="utf-8", errors="replace")
    else:
        print("[2/4] bibtex (跳过 — 无 .bib 文件)")

    # 第二遍
    print("[3/4] xelatex (第二遍)...")
    subprocess.run(
        xelatex_args, cwd=str(tex_dir),
        capture_output=True, encoding="utf-8", errors="replace"
    )

    # 第三遍
    print("[4/4] xelatex (第三遍)...")
    subprocess.run(
        xelatex_args, cwd=str(tex_dir),
        capture_output=True, encoding="utf-8", errors="replace"
    )

    # PDF 在 build/ 中, 复制到主目录
    pdf_in_build = build_dir / f"{tex_name}.pdf"
    pdf_final = tex_dir / f"{tex_name}.pdf"
    if pdf_in_build.exists():
        shutil.copy2(pdf_in_build, pdf_final)
        print(f"\n  编译成功: {pdf_final}")
        print(f"  (辅助文件在 {build_dir}/)")
        return True
    else:
        print(f"\n  编译可能失败, 请查看 {build_dir / tex_name}.log")
        return False


def clean_aux(tex_path: Path):
    """清理辅助文件 — 直接删除 build/ 目录."""
    tex_dir = tex_path.parent
    build_dir = tex_dir / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print(f"  已清理 {build_dir}/")
    else:
        print(f"  没有需要清理的临时文件")


def main():
    parser = argparse.ArgumentParser(
        description="CUPB Thesis LaTeX Skill — Markdown → PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python skill.py thesis.md                    # Markdown → .tex
  python skill.py thesis.md --compile          # Markdown → .tex → PDF
  python skill.py thesis.tex --compile-only    # .tex → PDF
  python skill.py thesis.md --compile --clean  # 编译后清理辅助文件
  python skill.py thesis.md --title "题目" --author "姓名" --studentid "学号"
        """,
    )
    parser.add_argument("input", help="输入文件 (.md 或 .tex)")
    parser.add_argument("--compile", "-c", action="store_true",
                        help="转换后自动编译为 PDF")
    parser.add_argument("--compile-only", "-C", action="store_true",
                        help="仅编译已有 .tex 文件")
    parser.add_argument("--clean", action="store_true",
                        help="编译后清理辅助文件")
    parser.add_argument("--output", "-o", help="输出 .tex 文件路径")
    parser.add_argument("--title", help="论文题目")
    parser.add_argument("--author", help="学生姓名")
    parser.add_argument("--studentid", help="学号")
    parser.add_argument("--college", help="学院")
    parser.add_argument("--major", help="专业")
    parser.add_argument("--adviser", help="指导教师")
    parser.add_argument("--finishdate", help="完成时间")
    parser.add_argument("--keywords", help="中文关键词 (分号分隔)")
    parser.add_argument("--en-keywords", help="英文关键词")
    parser.add_argument("--entitle", help="英文论文题目")

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"ERROR: 文件不存在 — {args.input}")
        sys.exit(1)

    # --- 仅编译模式 ---
    if args.compile_only:
        if input_path.suffix.lower() != ".tex":
            print("ERROR: --compile-only 需要 .tex 文件")
            sys.exit(1)
        success = compile_tex(input_path)
        if success and args.clean:
            clean_aux(input_path)
        sys.exit(0 if success else 1)

    # --- 转换模式: Markdown → .tex ---
    if input_path.suffix.lower() not in (".md", ".markdown", ".txt"):
        print(f"WARNING: 非 Markdown 文件, 尝试按文本处理: {input_path.name}")

    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 收集元数据
    metadata = {}
    for key in ["title", "author", "studentid", "college", "major",
                "adviser", "finishdate", "keywords", "en_keywords", "entitle"]:
        val = getattr(args, key, None)
        if val:
            metadata[key] = val

    # 转换
    print(f"  输入: {input_path}")
    tex_content = convert_md_to_tex(md_content, metadata)

    if args.output:
        tex_path = Path(args.output)
    else:
        tex_path = input_path.with_suffix(".tex")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    print(f"  输出: {tex_path}")
    print(f"  结构: 封面→声明→中英文摘要→目录→前言→正文→结论→参考文献→附录→致谢")

    # 编译
    if args.compile:
        success = compile_tex(tex_path)
        if success and args.clean:
            clean_aux(tex_path)

    print(f"\n  完成.")


if __name__ == "__main__":
    main()
