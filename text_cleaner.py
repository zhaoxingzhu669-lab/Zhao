#!/usr/bin/env python3
"""文本清洗小工具 text_cleaner

把杂乱的 .txt 文本清洗成整齐的版本：
  - 去掉每行首尾的空格，全角空格转半角
  - 行内连续的空格/制表符合并成一个空格
  - 删除空行（可用 --keep-blank 保留）
  - 删除重复行，保留第一次出现的顺序（可用 --keep-dupe 保留）

用法：
    python3 text_cleaner.py 输入.txt              # 输出到 输入_cleaned.txt
    python3 text_cleaner.py 输入.txt -o 输出.txt   # 指定输出文件
    python3 text_cleaner.py 输入.txt --keep-blank  # 保留空行

清洗完成后会打印一份小统计：删了多少空行、多少重复行、字数变化。
不需要安装任何第三方库，Python 3.8+ 即可运行。
"""

import argparse
import re
import sys
from pathlib import Path

FULLWIDTH_SPACE = "　"
MULTI_WS = re.compile(r"[ \t]+")


def clean_text(text: str, keep_blank: bool = False, keep_dupe: bool = False) -> tuple[str, dict]:
    """清洗文本，返回 (清洗后的文本, 统计信息)。"""
    lines = text.splitlines()
    stats = {
        "原行数": len(lines),
        "删除空行": 0,
        "删除重复行": 0,
        "原字符数": len(text),
    }

    seen = set()
    out_lines = []
    for raw in lines:
        line = MULTI_WS.sub(" ", raw.replace(FULLWIDTH_SPACE, " ")).strip()
        if not line:
            if keep_blank:
                out_lines.append("")
            else:
                stats["删除空行"] += 1
            continue
        if not keep_dupe:
            if line in seen:
                stats["删除重复行"] += 1
                continue
            seen.add(line)
        out_lines.append(line)

    cleaned = "\n".join(out_lines)
    if cleaned:
        cleaned += "\n"
    stats["清洗后行数"] = len(out_lines)
    stats["清洗后字符数"] = len(cleaned)
    return cleaned, stats


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="文本清洗小工具：去空行、去重行、合并多余空格")
    parser.add_argument("input", help="输入的 .txt 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径（默认：输入文件名 + _cleaned.txt）")
    parser.add_argument("--keep-blank", action="store_true", help="保留空行")
    parser.add_argument("--keep-dupe", action="store_true", help="保留重复行")
    args = parser.parse_args(argv)

    src = Path(args.input)
    if not src.is_file():
        print(f"找不到输入文件：{src}", file=sys.stderr)
        return 1

    text = src.read_text(encoding="utf-8", errors="replace")
    cleaned, stats = clean_text(text, keep_blank=args.keep_blank, keep_dupe=args.keep_dupe)

    dst = Path(args.output) if args.output else src.with_name(src.stem + "_cleaned" + src.suffix)
    dst.write_text(cleaned, encoding="utf-8")

    print(f"已清洗：{src} -> {dst}")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
