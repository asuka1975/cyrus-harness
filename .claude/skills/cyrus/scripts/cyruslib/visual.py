"""原稿を画像にし、中心視野・周辺視野を模してぼかす（視覚的な拾い読みテストの入力を作る）。

処理の流れ:
  1. Markdown を HTML にする。拾い読みで目が留まりやすい箇所（見出し、段落の最初の文、太字、
     箇条書きの頭、表の見出し行、図表のキャプション）を「注視点」として印を付ける。
  2. ヘッドレス Chrome で、注視点の位置を取り出し（--dump-dom）、ページ全体を画像にする（--screenshot）。
  3. Pillow で画像をぼかす。注視点はくっきり、その周り（傍中心視野）は少しぼかし、
     それ以外（周辺視野）は文字が読めない程度にぼかす。
  4. 読者の画面の高さごとにページを切り分ける。あわせて、文書全体の縮小図（一瞥したときの見え方）を作る。

Chrome と Pillow がない環境では VisualUnavailable を送出する。
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from . import jatext, mdparse


class VisualUnavailable(RuntimeError):
    pass


# 読む媒体ごとの見え方（本文の幅・文字の大きさ・一画面の高さ）
MEDIA = {
    "screen": {"width": 760, "font": 16, "viewport": 900},
    "mobile": {"width": 360, "font": 16, "viewport": 740},
    "print": {"width": 680, "font": 15, "viewport": 1000},
    "slide": {"width": 1000, "font": 22, "viewport": 700},
}
MARGIN = 24

# ぼかしの強さ（文字の大きさに対する比）。周辺視野は字形が崩れて読めない程度、傍中心視野はかろうじて語の形がわかる程度。
PERIPHERAL_BLUR = 0.34
PARAFOVEAL_BLUR = 0.14
FOVEA_PAD = 0.35       # 注視点の矩形を広げる量（文字の大きさに対する比）
PARAFOVEA_PAD = 2.5    # 傍中心視野の横の広さ（文字の大きさに対する比）。縦はその 0.25 倍（行をまたぐとほぼ見えない）

CSS = """
body { font-family: "Noto Sans CJK JP", "Noto Sans JP", "Hiragino Sans", sans-serif; color: #1f2328;
       background: #fff; width: %(width)dpx; margin: %(margin)dpx; font-size: %(font)dpx; line-height: 1.8; }
h1 { font-size: 1.8em; margin: 0.4em 0 0.6em; border-bottom: 1px solid #d0d7de; padding-bottom: 0.2em; }
h2 { font-size: 1.45em; margin: 1.4em 0 0.5em; border-bottom: 1px solid #d0d7de; padding-bottom: 0.15em; }
h3 { font-size: 1.2em; margin: 1.2em 0 0.4em; }
h4, h5, h6 { font-size: 1.05em; margin: 1em 0 0.3em; }
p { margin: 0 0 0.9em; }
ul, ol { margin: 0 0 0.9em; padding-left: 1.6em; }
li { margin: 0.15em 0; }
table { border-collapse: collapse; margin: 0 0 0.9em; font-size: 0.95em; }
th, td { border: 1px solid #d0d7de; padding: 0.3em 0.6em; text-align: left; vertical-align: top; }
th { background: #f6f8fa; }
pre { background: #f6f8fa; padding: 0.8em; font-size: 0.85em; line-height: 1.5; white-space: pre-wrap; margin: 0 0 0.9em; }
code { background: #f0f2f4; padding: 0 0.2em; font-size: 0.9em; }
blockquote { margin: 0 0 0.9em; padding: 0 1em; color: #57606a; border-left: 0.25em solid #d0d7de; }
.mermaid { text-align: center; margin: 0 0 0.9em; }
.figure { border: 1px dashed #8c959f; padding: 1.5em; text-align: center; color: #57606a; margin: 0 0 0.9em; }
#cyrus-layout { display: none; }
"""

LAYOUT_JS = """
<script>
function cyrusMeasure() {
  const out = [];
  document.querySelectorAll('[data-fx]').forEach(function (e) {
    const rects = Array.from(e.getClientRects()).map(function (r) {
      return [r.left + window.scrollX, r.top + window.scrollY, r.width, r.height];
    }).filter(function (r) { return r[2] > 0 && r[3] > 0; });
    out.push({kind: e.getAttribute('data-fx'), text: e.textContent.slice(0, 40), rects: rects});
  });
  const pre = document.createElement('pre');
  pre.id = 'cyrus-layout';
  pre.textContent = JSON.stringify({height: document.documentElement.scrollHeight, fixations: out});
  document.body.appendChild(pre);
}
window.addEventListener('load', function () {
  // Mermaid が読み込めたら図を描いてから測る。読み込めなければ（オフラインなど）ソースのまま測る。
  if (window.mermaid && document.querySelector('.mermaid')) {
    mermaid.initialize({startOnLoad: false, theme: 'neutral'});
    mermaid.run().then(cyrusMeasure, cyrusMeasure);
  } else {
    cyrusMeasure();
  }
});
</script>
"""


# Mermaid の図を描くためのライブラリ（読み込むのはライブラリ本体だけで、原稿は送らない）。
# CYRUS_MERMAID_JS でローカルのファイルや別の URL を指定できる。空文字にすると図はソースのまま表示する。
MERMAID_SRC = os.environ.get("CYRUS_MERMAID_JS", "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js")
MERMAID_JS = f'<script src="{html.escape(MERMAID_SRC)}"></script>' if MERMAID_SRC else ""


# ---------------------------------------------------------------- Markdown → HTML


def _inline(text: str) -> str:
    """インライン記法を HTML にする。太字は目に留まるので注視点にする。"""
    codes: list[str] = []

    def keep_code(m: re.Match) -> str:
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]*)`", keep_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"<u>\1</u>", text)
    text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r'<strong data-fx="bold">\1</strong>', text)
    text = re.sub(r"(?<![A-Za-z0-9_])__(?=\S)(.+?)(?<=\S)__(?![A-Za-z0-9_])", r'<strong data-fx="bold">\1</strong>', text)
    text = re.sub(r"\*(?=\S)(.+?)(?<=\S)\*", r"<em>\1</em>", text)
    return re.sub("\x00(\\d+)\x00", lambda m: f"<code>{html.escape(codes[int(m.group(1))])}</code>", text)


def _first_sentence_split(raw: str) -> tuple[str, str]:
    """段落の最初の文と残りに分ける（インライン記法を壊さないよう、Markdown のまま分ける）。"""
    depth = 0
    for i, ch in enumerate(raw):
        if ch in "「『（(【":
            depth += 1
        elif ch in "」』）)】" and depth:
            depth -= 1
        elif ch in "。！？" and depth == 0:
            j = i + 1
            while j < len(raw) and raw[j] in "」』）)】":
                j += 1
            head, rest = raw[:j], raw[j:]
            # 太字や強調の途中で切れたら、切らずに段落全体を最初の文とみなす
            if head.count("**") % 2 or head.count("`") % 2:
                return raw, ""
            return head, rest
    return raw, ""


def markdown_to_html(text: str, media: str = "screen") -> str:
    m = MEDIA.get(media, MEDIA["screen"])
    body: list[str] = []
    for b in mdparse.parse(text):
        if b.kind == "heading":
            lv = min(b.level, 6)
            body.append(f'<h{lv}><span data-fx="heading">{_inline(b.text)}</span></h{lv}>')
        elif b.kind == "paragraph":
            plain = jatext.strip_inline(b.text)
            if re.match(r"^\s*(図|表)\s*[0-9０-９]+", plain):
                body.append(f'<p><span data-fx="caption">{_inline(b.text)}</span></p>')
                continue
            head, rest = _first_sentence_split(b.text)
            body.append(f'<p><span data-fx="first">{_inline(head)}</span>{_inline(rest)}</p>')
        elif b.kind == "quote":
            head, rest = _first_sentence_split(b.text)
            body.append(f'<blockquote><p><span data-fx="first">{_inline(head)}</span>{_inline(rest)}</p></blockquote>')
        elif b.kind == "list":
            stack = ["ol" if b.items and b.items[0].ordered else "ul"]
            parts = [f"<{stack[0]}>"]
            for it in b.items:
                while it.depth > len(stack):
                    tag = "ol" if it.ordered else "ul"
                    stack.append(tag)
                    parts.append(f"<{tag}>")
                while it.depth < len(stack):
                    parts.append(f"</{stack.pop()}>")
                # 箇条書きは頭の数文字に目が留まる
                raw = it.text
                cut = 12
                if len(raw) > cut and raw[:cut].count("**") % 2 == 0 and raw[:cut].count("`") % 2 == 0:
                    parts.append(f'<li><span data-fx="item">{_inline(raw[:cut])}</span>{_inline(raw[cut:])}</li>')
                else:
                    parts.append(f'<li><span data-fx="item">{_inline(raw)}</span></li>')
            parts.extend(f"</{t}>" for t in reversed(stack))
            body.append("".join(parts))
        elif b.kind == "table" and b.rows:
            rows = ["<table><thead><tr>" + "".join(f'<th><span data-fx="table-head">{_inline(c)}</span></th>' for c in b.rows[0]) + "</tr></thead><tbody>"]
            for r in b.rows[1:]:
                rows.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>")
            rows.append("</tbody></table>")
            body.append("".join(rows))
        elif b.kind == "code":
            if b.lang == "mermaid":
                # 図は目に留まりやすいので、全体を注視点にする
                body.append(f'<div data-fx="figure"><pre class="mermaid">{html.escape(b.text)}</pre></div>')
            else:
                first, _, rest = b.text.partition("\n")
                body.append(f'<pre><code><span data-fx="code-head">{html.escape(first)}</span>'
                            + (f"\n{html.escape(rest)}" if rest else "") + "</code></pre>")
        elif b.kind == "image":
            body.append(f'<div class="figure"><span data-fx="caption">［図］{html.escape(b.text)}</span></div>')
        elif b.kind == "hr":
            body.append("<hr>")
    css = CSS % {"width": m["width"], "margin": MARGIN, "font": m["font"]}
    mermaid = MERMAID_JS if any(b.kind == "code" and b.lang == "mermaid" for b in mdparse.parse(text)) else ""
    return ("<!doctype html><html lang=\"ja\"><head><meta charset=\"utf-8\"><style>" + css + "</style></head><body>"
            + "\n".join(body) + mermaid + LAYOUT_JS + "</body></html>")


# ---------------------------------------------------------------- Chrome


def find_chrome() -> str | None:
    env = os.environ.get("CYRUS_CHROME")
    if env and Path(env).exists():
        return env
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        exe = shutil.which(name)
        if exe:
            return exe
    for cand in sorted((Path.home() / ".cache" / "ms-playwright").glob("chromium-*/chrome-linux*/chrome"), reverse=True):
        return str(cand)
    return None


def _chrome(args: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
    exe = find_chrome()
    if not exe:
        raise VisualUnavailable("Chrome / Chromium が見つかりません（環境変数 CYRUS_CHROME で場所を指定できます）。")
    with tempfile.TemporaryDirectory(prefix="cyrus-chrome-") as profile:
        base = [exe, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--no-first-run",
                "--disable-extensions", f"--user-data-dir={profile}", "--force-device-scale-factor=1"]
        return subprocess.run(base + args, capture_output=True, text=True, timeout=timeout)


def measure(html_path: Path, window_width: int) -> dict:
    proc = _chrome([f"--window-size={window_width},1000", "--virtual-time-budget=10000", "--dump-dom", html_path.as_uri()])
    m = re.search(r'<pre id="cyrus-layout">(.*?)</pre>', proc.stdout, re.DOTALL)
    if not m:
        raise VisualUnavailable(f"Chrome からレイアウトを取得できませんでした: {proc.stderr.strip()[:300]}")
    return json.loads(html.unescape(m.group(1)))


def screenshot(html_path: Path, out: Path, window_width: int, height: int) -> None:
    proc = _chrome([f"--window-size={window_width},{height}", "--virtual-time-budget=10000",
                    f"--screenshot={out}", html_path.as_uri()])
    if not out.exists():
        raise VisualUnavailable(f"Chrome で画像を作れませんでした: {proc.stderr.strip()[:300]}")


# ---------------------------------------------------------------- ぼかし


def _pil():
    try:
        from PIL import Image, ImageDraw, ImageFilter  # noqa: F401
    except ImportError as e:  # pragma: no cover
        raise VisualUnavailable("Pillow（PIL）が必要です: pip install pillow") from e
    return Image, ImageDraw, ImageFilter


def foveate(img, rects: list[list[float]], font_px: int):
    """注視点（rects）はくっきり、周りは少し、それ以外は強くぼかした画像を返す。"""
    Image, ImageDraw, ImageFilter = _pil()
    peripheral = img.filter(ImageFilter.GaussianBlur(font_px * PERIPHERAL_BLUR))
    parafoveal = img.filter(ImageFilter.GaussianBlur(font_px * PARAFOVEAL_BLUR))
    fovea_mask = Image.new("L", img.size, 0)
    para_mask = Image.new("L", img.size, 0)
    df, dp = ImageDraw.Draw(fovea_mask), ImageDraw.Draw(para_mask)
    fp, pp = font_px * FOVEA_PAD, font_px * PARAFOVEA_PAD
    for x, y, w, h in rects:
        df.rectangle([x - fp, y - fp, x + w + fp, y + h + fp], fill=255)
        dp.rounded_rectangle([x - pp, y - pp * 0.25, x + w + pp, y + h + pp * 0.25], radius=int(pp * 0.4), fill=255)
    # 境目を柔らかくして、視野の中心から外へ連続的にぼやけるようにする
    fovea_mask = fovea_mask.filter(ImageFilter.GaussianBlur(font_px * 0.25))
    para_mask = para_mask.filter(ImageFilter.GaussianBlur(font_px * 0.7))
    out = Image.composite(parafoveal, peripheral, para_mask)
    return Image.composite(img, out, fovea_mask)


@dataclass
class VisualResult:
    pages: list[Path]
    overview: Path
    layout: Path
    fixations: int


def render(text: str, out_dir: Path, media: str = "screen", keep_sharp: bool = False) -> VisualResult:
    """原稿を画像化してぼかし、out_dir に page-XX.png と overview.png を書き出す。"""
    Image, _, _ = _pil()
    m = MEDIA.get(media, MEDIA["screen"])
    window = m["width"] + MARGIN * 2
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("page-*.png"):
        old.unlink()
    with tempfile.TemporaryDirectory(prefix="cyrus-visual-") as td:
        page = Path(td) / "doc.html"
        page.write_text(markdown_to_html(text, media), encoding="utf-8")
        layout = measure(page, window)
        height = max(int(layout["height"]) + MARGIN, 200)
        full_png = Path(td) / "full.png"
        screenshot(page, full_png, window, height)
        img = Image.open(full_png).convert("RGB")
    (out_dir / "layout.json").write_text(json.dumps(layout, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if keep_sharp:
        img.save(out_dir / "sharp.png")

    rects = [r for f in layout["fixations"] for r in f["rects"]]
    blurred = foveate(img, rects, m["font"])

    # 一画面ずつに切り分ける（読者がスクロールしながら見る単位）
    vp = m["viewport"]
    pages: list[Path] = []
    top, n = 0, 0
    while top < img.height:
        n += 1
        p = out_dir / f"page-{n:02d}.png"
        blurred.crop((0, top, img.width, min(top + vp, img.height))).save(p)
        pages.append(p)
        top += vp - m["font"] * 3  # 少し重ねて、境目の行が切れて読めなくなるのを防ぐ

    # 一瞥したときの見え方: 全体を縮小（細かい字は読めず、見出しや図表の配置だけがわかる）
    scale = min(0.4, 2400 / max(img.height, 1))
    overview = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.LANCZOS)
    ov = out_dir / "overview.png"
    overview.save(ov)
    return VisualResult(pages, ov, out_dir / "layout.json", len(layout["fixations"]))
