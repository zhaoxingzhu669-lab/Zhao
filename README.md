# Zhao

good

## 小工具：文本清洗 text_cleaner

一个零依赖的 Python 命令行小工具，把杂乱的 `.txt` 文本清洗成整齐的版本。适合处理复制来的笔记、待办清单、标注数据等文本。

### 功能

- 去掉每行首尾空格，全角空格转半角
- 行内连续的空格/制表符合并成一个
- 删除空行（`--keep-blank` 可保留）
- 删除重复行，保留第一次出现的顺序（`--keep-dupe` 可保留）
- 清洗完打印统计：删了多少空行、多少重复行、字符数变化

### 用法

需要 Python 3.8+，不用安装任何第三方库。

```bash
python3 text_cleaner.py 输入.txt              # 输出到 输入_cleaned.txt
python3 text_cleaner.py 输入.txt -o 输出.txt   # 指定输出文件
python3 text_cleaner.py 输入.txt --keep-blank  # 保留空行
```

### 示例

输入 `examples/messy.txt`（带多余空格、空行和重复行）：

```bash
python3 text_cleaner.py examples/messy.txt -o examples/clean.txt
```

输出：

```
已清洗：examples/messy.txt -> examples/clean.txt
  原行数: 11
  删除空行: 4
  删除重复行: 2
  原字符数: 60
  清洗后行数: 5
  清洗后字符数: 34
```

清洗结果见 `examples/clean.txt`。

### 测试

```bash
python3 -m unittest test_text_cleaner -v
```
