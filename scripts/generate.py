#!/usr/bin/env python3
"""
Vocab Quiz Generator
从词库 JSON 生成单文件 HTML 单词测试应用。

用法:
  python3 generate.py <wordlist.json> <output.html> [--title "自定义标题"]

词库 JSON 格式见 references/wordlist-schema.md
"""
import json
import sys
import os
import subprocess
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
TEMPLATE_PATH = os.path.join(SKILL_DIR, "assets", "quiz-template.html")
GLOBAL_WORDS_PATH = os.path.join(SKILL_DIR, "assets", "global-words.json")
INFLECTIONS_PATH = os.path.join(SKILL_DIR, "assets", "inflections-cache.json")


def load_global_words():
    """加载 DeepSeek 12655 词库，返回 {word_lower: {translations, phrases}}"""
    if not os.path.exists(GLOBAL_WORDS_PATH):
        return {}
    with open(GLOBAL_WORDS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    lookup = {}
    for w in data.get("words", []):
        key = w["word"].lower()
        lookup[key] = {
            "translations": w.get("translations", []),
            "phrases": w.get("phrases", [])
        }
    return lookup


def load_inflections():
    """加载单词变形缓存，返回 {word_lower: [{type, word, cn}]}"""
    if not os.path.exists(INFLECTIONS_PATH):
        return {}
    with open(INFLECTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def collect_all_words(word_data):
    """从词库中收集所有单词（不含短语），返回小写列表"""
    words = []
    for theme in word_data.get("themes", []):
        for lesson in theme.get("lessons", []):
            for w in lesson.get("words", []):
                words.append(w["en"].lower())
    return words


def build_deepseek_data(word_data, ds_lookup, infl_lookup):
    """构建本次测试用到的 DeepSeek 数据查找表（释义+搭配+变形）"""
    all_words = collect_all_words(word_data)
    ds_data = {}
    for key in all_words:
        entry = {}
        if key in ds_lookup:
            entry["translations"] = ds_lookup[key]["translations"]
            entry["phrases"] = ds_lookup[key]["phrases"]
        if key in infl_lookup:
            entry["inflections"] = infl_lookup[key]
        if entry:
            ds_data[key] = entry
    return ds_data


def validate_js(html_content):
    """提取 <script> 内容用 node --check 验证语法"""
    s = html_content.find("<script>")
    if s == -1:
        return True, "no <script> found"
    s += 8
    e = html_content.find("</script>", s)
    if e == -1:
        return True, "no </script> found"
    js = html_content[s:e]
    tmp = "/tmp/vocab_quiz_check.js"
    with open(tmp, "w") as f:
        f.write(js)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    if r.returncode == 0:
        return True, "OK"
    return False, r.stderr[:500]


def main():
    parser = argparse.ArgumentParser(description="Generate vocab quiz HTML from wordlist JSON")
    parser.add_argument("wordlist", help="Path to wordlist JSON file")
    parser.add_argument("output", help="Output HTML file path")
    parser.add_argument("--title", help="Override app title (optional)")
    args = parser.parse_args()

    # 1. 读取词库
    if not os.path.exists(args.wordlist):
        print(f"ERROR: wordlist file not found: {args.wordlist}", file=sys.stderr)
        sys.exit(1)
    with open(args.wordlist, "r", encoding="utf-8") as f:
        word_data = json.load(f)

    # 2. 加载 DeepSeek 词库和变形缓存
    ds_lookup = load_global_words()
    infl_lookup = load_inflections()
    print(f"DeepSeek 词库: {len(ds_lookup)} 词")
    print(f"变形缓存: {len(infl_lookup)} 词")

    # 3. 构建本次测试的 DeepSeek 数据
    ds_data = build_deepseek_data(word_data, ds_lookup, infl_lookup)
    all_words = collect_all_words(word_data)
    matched = sum(1 for w in all_words if w in ds_lookup)
    with_infl = sum(1 for w in all_words if w in infl_lookup)
    print(f"本次词库: {len(all_words)} 词")
    print(f"  - 匹配 DeepSeek 释义: {matched}/{len(all_words)}")
    print(f"  - 有变形数据: {with_infl}/{len(all_words)}")

    # 4. 读取模板并注入
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    word_js = "const WORD_DATA = " + json.dumps(word_data, ensure_ascii=False, indent=2) + ";"
    ds_js = "const DEEPSEEK_DATA = " + json.dumps(ds_data, ensure_ascii=False, indent=2) + ";"

    output = template.replace("/*WORD_DATA_PLACEHOLDER*/", word_js)
    output = output.replace("/*DEEPSEEK_DATA_PLACEHOLDER*/", ds_js)

    # 5. 可选：覆盖标题（模板中首页标题为 <h1 ...>Vocab Quiz</h1>）
    if args.title:
        import re as _re
        output = _re.sub(r'(<h1[^>]*>)Vocab Quiz(</h1>)',
                         lambda m: m.group(1) + args.title + m.group(2),
                         output, count=1)

    # 6. 语法验证
    ok, msg = validate_js(output)
    if not ok:
        print(f"ERROR: JS syntax check failed:\n{msg}", file=sys.stderr)
        sys.exit(1)
    print(f"JS 语法验证: {msg}")

    # 7. 写入输出
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output)

    size_kb = len(output) / 1024
    print(f"\n✅ 生成成功: {args.output} ({size_kb:.1f} KB)")
    print(f"   双击在浏览器中打开即可使用")


if __name__ == "__main__":
    main()
