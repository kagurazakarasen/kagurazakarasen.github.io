# -*- coding: utf-8 -*-
"""Build a Japanese PDF combining the ja.md translation with original PDF figures."""
import re
import markdown

SRC = r"D:\work\NASA_DOC\Descanso4--Voyager_ed_ja.md"
OUT_HTML = r"D:\work\NASA_DOC\Descanso4--Voyager_ed_ja.html"

with open(SRC, "r", encoding="utf-8") as f:
    text = f.read()

# ---- Insert figure images at appropriate anchors ----
replacements = [
    (
        "**図1-1. ボイジャーの飛行経路。**",
        '<div class="figure">\n<img src="images/fig1-1.jpeg" alt="Fig1-1">\n</div>\n\n'
        "**図1-1. ボイジャーの飛行経路。**",
    ),
    (
        "探査機および観測装置は概ね健全な状態にある。",
        '<div class="figure">\n<img src="images/fig1-2.png" alt="Fig1-2">\n</div>\n\n'
        "**図1-2. ボイジャー探査機と科学観測装置。**\n\n"
        "探査機および観測装置は概ね健全な状態にある。",
    ),
    (
        "**図1-3. 2001年5月時点でのボイジャー恒星間ミッションが探査するプラズマおよび中性粒子\n環境のシミュレーション。**",
        '<div class="figure">\n<img src="images/fig1-3.jpeg" alt="Fig1-3">\n</div>\n\n'
        "**図1-3. 2001年5月時点でのボイジャー恒星間ミッションが探査するプラズマおよび中性粒子\n環境のシミュレーション。**",
    ),
    (
        "### 2.1 アップリンク",
        '<div class="figure">\n<img src="images/fig2-1.png" alt="Fig2-1">\n</div>\n\n'
        "**図2-1. ボイジャーの探査機・地上テレコム機能の概要。**\n\n"
        "### 2.1 アップリンク",
    ),
    (
        "**図3-1. ボイジャー探査機テレコム機能ブロック図。**",
        '<div class="figure">\n<img src="images/fig3-1.png" alt="Fig3-1">\n</div>\n\n'
        "**図3-1. ボイジャー探査機テレコム機能ブロック図。**",
    ),
    (
        "**図3-2. ボイジャーSXAのパターンとビーム幅。**",
        '<div class="figure">\n<img src="images/fig3-2.png" alt="Fig3-2">\n</div>\n\n'
        "**図3-2. ボイジャーSXAのパターンとビーム幅。**",
    ),
    (
        "### 4.2 コマンド処理",
        '<div class="figure">\n<img src="images/fig4-1.jpeg" alt="Fig4-1">\n</div>\n\n'
        "**図4-1. DSS-14局・DSS-43局のマイクロ波・送信機ブロック図。**\n\n"
        "### 4.2 コマンド処理",
    ),
    (
        "**図5-1. ボイジャー2号テレコム性能の25年間予測。**\n**図5-2. ボイジャー1号テレコム性能の25年間予測。**",
        '<div class="figure">\n<img src="images/fig5-1.png" alt="Fig5-1">\n</div>\n\n'
        "**図5-1. ボイジャー2号テレコム性能の25年間予測。**\n\n"
        '<div class="figure">\n<img src="images/fig5-2.png" alt="Fig5-2">\n</div>\n\n'
        "**図5-2. ボイジャー1号テレコム性能の25年間予測。**",
    ),
]

for old, new in replacements:
    count = text.count(old)
    assert count == 1, f"Anchor not found exactly once ({count}): {old[:40]!r}"
    text = text.replace(old, new)

# ---- Convert markdown body to HTML ----
body_html = markdown.markdown(text, extensions=["tables", "extra", "sane_lists"])

# Only force a page break before major chapter-level headings (and ToC/References),
# not every front-matter h2 (preface/foreword/acknowledgements), to avoid near-empty pages.
def _mark_chapter(m):
    inner = m.group(1)
    plain = re.sub(r"<[^>]+>", "", inner)
    if plain.startswith("第") or plain in ("目次", "参考文献"):
        return f'<h2 class="chapter-break">{inner}</h2>'
    return f"<h2>{inner}</h2>"

body_html = re.sub(r"<h2>(.*?)</h2>", _mark_chapter, body_html, flags=re.S)

# ---- Cover page ----
cover_html = """
<div class="cover-page">
  <img src="images/cover.jpeg" alt="cover">
</div>
"""

page_css = """
@page {
  size: A4;
  margin: 20mm 18mm;
}
body {
  font-family: "Yu Mincho", "YuMincho", "Hiragino Mincho ProN", "Meiryo", serif;
  font-size: 10.5pt;
  line-height: 1.85;
  color: #111;
}
h1, h2, h3, h4 {
  font-family: "Yu Gothic", "Meiryo", sans-serif;
  color: #0b2e59;
  page-break-after: avoid;
}
h1 { font-size: 20pt; border-bottom: 3px solid #0b2e59; padding-bottom: 6px; }
h2 {
  font-size: 15pt;
  margin-top: 2.2em;
  border-left: 6px solid #0b2e59;
  padding-left: 8px;
}
h2.chapter-break {
  page-break-before: always;
}
h3 { font-size: 12.5pt; margin-top: 1.6em; }
h4 { font-size: 11pt; margin-top: 1.3em; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.6em 0; }
blockquote {
  border-left: 4px solid #aaa;
  margin: 1em 0;
  padding: 0.2em 1em;
  color: #444;
  font-size: 9.5pt;
  background: #f7f7f7;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
  font-size: 9pt;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #888;
  padding: 4px 7px;
  text-align: left;
  vertical-align: top;
}
th { background: #e8edf5; }
.figure {
  text-align: center;
  margin: 1.2em 0 0.3em 0;
  page-break-inside: avoid;
}
.figure img {
  max-width: 92%;
  max-height: 210mm;
}
p { margin: 0.6em 0; }
p strong:first-child {
  display: block;
  text-align: center;
  margin-top: 0.2em;
}
.cover-page {
  page-break-after: always;
  text-align: center;
}
.cover-page img {
  width: 100%;
  max-height: 277mm;
  object-fit: contain;
}
ul, ol { margin: 0.5em 0; padding-left: 1.6em; }
li { margin: 0.25em 0; }
"""

html_doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>ボイジャー テレコミュニケーション(日本語版)</title>
<style>
{page_css}
</style>
</head>
<body>
{cover_html}
{body_html}
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_doc)

print("Wrote", OUT_HTML, "len=", len(html_doc))
