"""원본 HTML을 test.html 수준의 프릳츠 스타일로 변환 (v2)"""
import os
import re

ORIG_DIR = "/tmp/orig_docs"
DEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

FRITZ_CSS = '''@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fafaf7;font-family:'Pretendard',sans-serif;-webkit-font-smoothing:antialiased;color:#222}
a{color:inherit;text-decoration:none}
.wrap{max-width:480px;margin:0 auto;padding:0 28px 120px}
.nav{padding:32px 0 64px;font-size:.7rem;color:#aaa;letter-spacing:.3px}
.hero{padding-bottom:56px}
.hero-cat{font-size:.72rem;font-weight:500;color:#999;margin-bottom:32px}
.hero h1{font-size:1.9rem;font-weight:800;line-height:1.45;letter-spacing:-.8px;color:#111}
.prose{padding:0 0 48px}
.prose p{font-size:.95rem;color:#444;line-height:2.2;margin-bottom:20px;word-break:keep-all}
.prose .muted{color:#999}
.prose .bold{font-weight:700;color:#111}
.quote{padding:40px 0;margin:8px 0}
.quote p{font-size:1.05rem;color:#444;line-height:2;letter-spacing:-.2px}
.quote strong{color:#191919;font-weight:700}
.quote-from{font-size:.78rem;color:#bbb;margin-top:16px}
.num-block{padding:48px 0;text-align:center;border-top:1px solid #eee;border-bottom:1px solid #eee;margin:8px 0 48px}
.num-block .num{font-size:3rem;font-weight:900;color:#111;letter-spacing:-1px}
.num-block .num-sub{font-size:.75rem;color:#aaa;margin-top:8px;font-weight:400}
.emphasis{background:#111;margin:0 -28px;padding:40px 32px}
.emphasis p{font-size:1rem;color:#ddd;line-height:2;font-weight:500}
.emphasis strong{color:#e8530e;font-weight:700}
.section{padding:48px 0;border-top:1px solid #eee}
.section-label{font-size:.6rem;font-weight:700;color:#bbb;letter-spacing:2.5px;margin-bottom:20px}
.section h2{font-size:1.3rem;font-weight:800;line-height:1.4;margin-bottom:20px;word-break:keep-all}
.timeline{display:flex;flex-direction:column;gap:16px;margin-top:8px}
.tl-item{background:#fff;border-radius:14px;padding:22px 20px;box-shadow:0 1px 8px rgba(0,0,0,.03)}
.tl-item.highlight{background:#fff8f5;border:1.5px solid rgba(255,107,53,.2)}
.tl-num{font-size:.6rem;font-weight:700;color:#ccc;letter-spacing:1.5px;margin-bottom:8px}
.tl-item.highlight .tl-num{color:#e8530e}
.tl-title{font-size:.95rem;font-weight:700;margin-bottom:6px}
.tl-item.highlight .tl-title{color:#e8530e}
.tl-desc{font-size:.84rem;color:#888;line-height:1.6}
.compare{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}
.compare-box{background:#fff;border-radius:14px;padding:22px 18px;box-shadow:0 1px 8px rgba(0,0,0,.03)}
.compare-box h4{font-size:.68rem;font-weight:700;color:#bbb;letter-spacing:.5px;margin-bottom:12px}
.compare-box.active h4{color:#e8530e}
.compare-box li{list-style:none;font-size:.84rem;color:#888;padding:3px 0;line-height:1.5}
.compare-box.active li{color:#444}
.compare-box.active strong{color:#111}
.signal{padding:48px 0;border-bottom:1px solid #eee}
.signal-label{font-size:.6rem;font-weight:700;color:#bbb;letter-spacing:2.5px;margin-bottom:20px}
.signal-item{display:flex;align-items:baseline;gap:12px;padding:10px 0}
.signal-dot{width:5px;height:5px;border-radius:50%;background:#e8530e;flex-shrink:0;margin-top:6px}
.signal-text{font-size:.88rem;color:#555;line-height:1.6}
.aud-card{padding:48px 0;text-align:center;border-bottom:1px solid #eee}
.aud-card h3{font-size:.88rem;font-weight:600;color:#666;margin-bottom:12px}
.aud-card .aud-num{font-size:2.6rem;font-weight:900;color:#e8530e;letter-spacing:-1px}
.aud-card .aud-basis{font-size:.72rem;color:#bbb;margin-top:8px}
.usecase{padding:48px 0}
.usecase-label{font-size:.6rem;font-weight:700;color:#bbb;letter-spacing:2.5px;margin-bottom:28px}
.usecase-item{padding:20px 0;border-bottom:1px solid #f0f0f0}
.usecase-item:last-child{border:none}
.usecase-who{font-size:.88rem;font-weight:700;color:#111;margin-bottom:6px}
.usecase-how{font-size:.84rem;color:#888;line-height:1.7}
.cta{text-align:center;padding:48px 0}
.cta a{display:inline-block;background:#111;color:#fff;padding:14px 36px;font-size:.8rem;font-weight:600;letter-spacing:.3px}
.footer{text-align:center;font-size:.68rem;color:#ccc;padding:32px 0;line-height:2}'''


def build_fritz_html(title, category, headline, sections):
    content = '\n\n'.join(s for s in sections if s)
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} — 오늘의 오디언스</title>
<style>
{FRITZ_CSS}
</style>
</head>
<body>
<div class="wrap">
<div class="nav">오늘의 오디언스</div>
<div class="hero">
  <div class="hero-cat">{category}</div>
  <h1>{headline}</h1>
</div>

{content}

<div class="cta"><a href="mailto:audiencelab@igaworks.com">이 오디언스 활용 문의 →</a></div>
<div class="footer">
  본 리포트는 IGAWorks DMP 행동 데이터 기반 오디언스 분석입니다.<br>
  데이터 기준: 모바일인덱스 실측 · © 2026 IGAWorks<br>
  made by soddy
</div>
</div>
</body>
</html>'''


def convert_body_style(html):
    """Convert files with .body/.num/.highlight/.signal/.audience/.usecase structure."""
    # Category + headline
    tag_m = re.search(r'<div class="tag">(.*?)</div>', html)
    h1_m = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    category = tag_m.group(1).strip() if tag_m else ''
    headline = h1_m.group(1).strip() if h1_m else ''
    title = re.sub(r'<[^>]+>', ' ', headline).strip()

    sections = []

    # 1. Prose
    body_m = re.search(r'<div class="body">(.*?)<div class="num">', html, re.DOTALL)
    if body_m:
        raw = body_m.group(1)
        lines = []
        for m in re.finditer(r'<p(\s+class="([^"]*)")?\s*>(.*?)</p>', raw, re.DOTALL):
            cls = m.group(2) or ''
            content = m.group(3).strip()
            if 'gray' in cls:
                lines.append(f'  <p class="muted">{content}</p>')
            else:
                lines.append(f'  <p>{content}</p>')
        if lines:
            sections.append('<div class="prose">\n' + '\n'.join(lines) + '\n</div>')

    # 2. Number
    num_m = re.search(r'<div class="num">(.*?)</div>\s*<div class="num-sub">(.*?)</div>', html, re.DOTALL)
    if num_m:
        sections.append(f'<div class="num-block">\n  <div class="num">{num_m.group(1).strip()}</div>\n  <div class="num-sub">{num_m.group(2).strip()}</div>\n</div>')

    # 3. Emphasis/highlight
    hl_m = re.search(r'<div class="highlight">\s*<p>(.*?)</p>\s*</div>', html, re.DOTALL)
    if hl_m:
        sections.append(f'<div class="emphasis">\n  <p>{hl_m.group(1).strip()}</p>\n</div>')

    # 4. Signal
    signal_items = re.findall(r'<div class="s-text">(.*?)</div>', html)
    if signal_items:
        items = '\n'.join(f'  <div class="signal-item"><div class="signal-dot"></div><div class="signal-text">{s.strip()}</div></div>' for s in signal_items)
        sections.append(f'<div class="signal">\n  <div class="signal-label">DMP SIGNAL</div>\n{items}\n</div>')

    # 5. Audience
    aud_m = re.search(r'<h3>(.*?)</h3>\s*<div class="a-num">(.*?)</div>\s*<div class="a-basis">(.*?)</div>', html, re.DOTALL)
    if aud_m:
        sections.append(f'<div class="aud-card">\n  <h3>{aud_m.group(1).strip()}</h3>\n  <div class="aud-num">{aud_m.group(2).strip()}</div>\n  <div class="aud-basis">{aud_m.group(3).strip()}</div>\n</div>')

    # 6. Usecase
    uc_items = re.findall(r'<div class="u-who">(.*?)</div>\s*<div class="u-how">(.*?)</div>', html, re.DOTALL)
    if uc_items:
        items = '\n'.join(f'  <div class="usecase-item">\n    <div class="usecase-who">{w.strip()}</div>\n    <div class="usecase-how">{h.strip()}</div>\n  </div>' for w, h in uc_items)
        sections.append(f'<div class="usecase">\n  <div class="usecase-label">이 오디언스를 쓸 수 있는 광고주</div>\n{items}\n</div>')

    return title, category, headline, sections


def convert_toss_style(html):
    """Convert files with .punchline/.quote/.step/.compare/.audience-box/.biz structure."""
    # Category + headline
    tag_m = re.search(r'<div class="tag">(.*?)</div>', html)
    h1_m = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    category = tag_m.group(1).strip() if tag_m else ''
    headline = h1_m.group(1).strip() if h1_m else ''
    title = re.sub(r'<[^>]+>', ' ', headline).strip()

    sections = []

    # 1. Quote
    quote_m = re.search(r'<div class="quote">\s*<p>(.*?)</p>\s*<div class="from">(.*?)</div>', html, re.DOTALL)
    if quote_m:
        sections.append(f'<div class="quote">\n  <p>{quote_m.group(1).strip()}</p>\n  <p class="quote-from">{quote_m.group(2).strip()}</p>\n</div>')

    # 2. Punchline as emphasis
    punch_m = re.search(r'<div class="punchline">\s*<p>(.*?)</p>\s*</div>', html, re.DOTALL)
    if punch_m:
        sections.append(f'<div class="emphasis">\n  <p>{punch_m.group(1).strip()}</p>\n</div>')

    # 3. Audience number
    aud_m = re.search(r'<h3>(.*?)</h3>\s*<div class="a-num">(.*?)</div>\s*<div class="a-basis">(.*?)</div>', html, re.DOTALL)
    if aud_m:
        sections.append(f'<div class="num-block">\n  <div class="num">{aud_m.group(2).strip()}</div>\n  <div class="num-sub">{aud_m.group(3).strip()}</div>\n</div>')

    # 4. Steps/Timeline
    steps = re.findall(r'<div class="step(\s+active)?">\s*<div class="step-num">(.*?)</div>\s*<div class="step-title">(.*?)</div>\s*<div class="step-desc">(.*?)</div>', html, re.DOTALL)
    if steps:
        items = []
        for active, num, step_title, desc in steps:
            cls = ' highlight' if active.strip() else ''
            items.append(f'    <div class="tl-item{cls}">\n      <div class="tl-num">{num.strip()}</div>\n      <div class="tl-title">{step_title.strip()}</div>\n      <div class="tl-desc">{desc.strip()}</div>\n    </div>')
        tl = '\n'.join(items)
        sections.append(f'<div class="section">\n  <div class="section-label">이 사람의 행동 시그널</div>\n  <div class="timeline">\n{tl}\n  </div>\n</div>')

    # 5. Compare
    comp_m = re.search(r'<div class="compare">\s*<div class="compare-col">\s*<h4>(.*?)</h4>(.*?)</div>\s*<div class="compare-col">\s*<h4>(.*?)</h4>(.*?)</div>', html, re.DOTALL)
    if comp_m:
        def extract_items(raw):
            items = re.findall(r'<li>(.*?)</li>', raw, re.DOTALL)
            return '\n'.join(f'        <li>{i.strip()}</li>' for i in items)
        left_title = comp_m.group(1).strip()
        left_items = extract_items(comp_m.group(2))
        right_title = comp_m.group(3).strip()
        right_items = extract_items(comp_m.group(4))
        sections.append(f'''<div class="section">
  <div class="section-label">뭐가 다른가</div>
  <div class="compare">
    <div class="compare-box">
      <h4>{left_title}</h4>
      <ul>
{left_items}
      </ul>
    </div>
    <div class="compare-box active">
      <h4>{right_title}</h4>
      <ul>
{right_items}
      </ul>
    </div>
  </div>
</div>''')

    # 6. Signal
    signal_items = re.findall(r'<div class="s-text">(.*?)</div>', html)
    if signal_items:
        items = '\n'.join(f'  <div class="signal-item"><div class="signal-dot"></div><div class="signal-text">{s.strip()}</div></div>' for s in signal_items)
        sections.append(f'<div class="signal">\n  <div class="signal-label">DMP SIGNAL</div>\n{items}\n</div>')

    # 7. Audience card
    if aud_m:
        sections.append(f'<div class="aud-card">\n  <h3>{aud_m.group(1).strip()}</h3>\n  <div class="aud-num">{aud_m.group(2).strip()}</div>\n  <div class="aud-basis">{aud_m.group(3).strip()}</div>\n</div>')

    # 8. Biz items as usecase
    biz_items = re.findall(r'<span class="biz-name">(.*?)</span>.*?<div class="biz-body-inner">\s*<p>(.*?)</p>\s*<div class="biz-action">(.*?)</div>', html, re.DOTALL)
    if biz_items:
        items = '\n'.join(f'  <div class="usecase-item">\n    <div class="usecase-who">{name.strip()}</div>\n    <div class="usecase-how">{desc.strip()} {action.strip()}</div>\n  </div>' for name, desc, action in biz_items)
        sections.append(f'<div class="usecase">\n  <div class="usecase-label">이 오디언스를 쓸 수 있는 광고주</div>\n{items}\n</div>')

    return title, category, headline, sections


# Process all files
count = 0
for fname in sorted(os.listdir(ORIG_DIR)):
    if not fname.endswith('.html') or fname in ('index.html', 'test.html'):
        continue

    with open(os.path.join(ORIG_DIR, fname), 'r', encoding='utf-8') as f:
        html = f.read()

    # Determine type
    if '<div class="body">' in html:
        title, category, headline, sections = convert_body_style(html)
    elif 'background:#f7f7fa' in html:
        title, category, headline, sections = convert_toss_style(html)
    else:
        print(f"  SKIP (unknown): {fname}")
        continue

    if not headline or len(sections) < 2:
        print(f"  SKIP (insufficient): {fname} — {len(sections)} sections")
        continue

    result = build_fritz_html(title, category, headline, sections)
    dest = os.path.join(DEST_DIR, fname)
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"✓ {fname} ({len(sections)} sections)")
    count += 1

print(f"\n완료 — {count}개 파일 변환됨")
