"""docs/ 내 에세이 HTML을 프릳츠 스타일로 일괄 변환"""
import os
import re

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

FRITZ_TEMPLATE = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} — 오늘의 오디언스</title>
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#fafaf7;font-family:'Pretendard',sans-serif;-webkit-font-smoothing:antialiased;color:#222}}
a{{color:inherit;text-decoration:none}}
.wrap{{max-width:480px;margin:0 auto;padding:0 28px 120px}}
.nav{{padding:32px 0 64px;font-size:.7rem;color:#aaa;letter-spacing:.3px}}
.hero{{padding-bottom:56px}}
.hero-cat{{font-size:.72rem;font-weight:500;color:#999;margin-bottom:32px}}
.hero h1{{font-size:1.9rem;font-weight:800;line-height:1.45;letter-spacing:-.8px;color:#111}}
.prose{{padding:0 0 48px}}
.prose p{{font-size:.95rem;color:#444;line-height:2.2;margin-bottom:20px;word-break:keep-all}}
.prose .muted{{color:#999}}
.prose .bold{{font-weight:700;color:#111}}
.num-block{{padding:48px 0;text-align:center;border-top:1px solid #eee;border-bottom:1px solid #eee;margin:8px 0 48px}}
.num-block .num{{font-size:3rem;font-weight:900;color:#111;letter-spacing:-1px}}
.num-block .num-sub{{font-size:.75rem;color:#aaa;margin-top:8px;font-weight:400}}
.emphasis{{background:#111;margin:0 -28px;padding:40px 32px}}
.emphasis p{{font-size:1rem;color:#ddd;line-height:2;font-weight:500}}
.emphasis strong{{color:#e8530e;font-weight:700}}
.signal{{padding:48px 0;border-bottom:1px solid #eee}}
.signal-label{{font-size:.6rem;font-weight:700;color:#bbb;letter-spacing:2.5px;margin-bottom:20px}}
.signal-item{{display:flex;align-items:baseline;gap:12px;padding:10px 0}}
.signal-dot{{width:5px;height:5px;border-radius:50%;background:#e8530e;flex-shrink:0;margin-top:6px}}
.signal-text{{font-size:.88rem;color:#555;line-height:1.6}}
.aud-card{{padding:48px 0;text-align:center;border-bottom:1px solid #eee}}
.aud-card h3{{font-size:.88rem;font-weight:600;color:#666;margin-bottom:12px}}
.aud-card .aud-num{{font-size:2.6rem;font-weight:900;color:#e8530e;letter-spacing:-1px}}
.aud-card .aud-basis{{font-size:.72rem;color:#bbb;margin-top:8px}}
.usecase{{padding:48px 0}}
.usecase-label{{font-size:.6rem;font-weight:700;color:#bbb;letter-spacing:2.5px;margin-bottom:28px}}
.usecase-item{{padding:20px 0;border-bottom:1px solid #f0f0f0}}
.usecase-item:last-child{{border:none}}
.usecase-who{{font-size:.88rem;font-weight:700;color:#111;margin-bottom:6px}}
.usecase-how{{font-size:.84rem;color:#888;line-height:1.7}}
.cta{{text-align:center;padding:48px 0}}
.cta a{{display:inline-block;background:#111;color:#fff;padding:14px 36px;font-size:.8rem;font-weight:600;letter-spacing:.3px}}
.footer{{text-align:center;font-size:.68rem;color:#ccc;padding:32px 0;line-height:2}}
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


def extract_content(html):
    """Extract structured content from existing essay HTML."""
    # Find the second <style> block content (the actual page content starts after it)
    # Get category/tag
    tag_match = re.search(r'<div class="(?:tag|hero-cat)">(.*?)</div>', html)
    category = tag_match.group(1).strip() if tag_match else ''

    # Get title from <h1>
    h1_match = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    headline = h1_match.group(1).strip() if h1_match else ''
    title = re.sub(r'<[^>]+>', ' ', headline).strip()

    # Extract prose paragraphs (between hero and num)
    prose_parts = []
    # Find paragraphs in .body section
    body_ps = re.findall(r'<p(?:\s+class="([^"]*)")?>(.*?)</p>', html, re.DOTALL)
    
    prose_html = ''
    num_html = ''
    emphasis_html = ''
    signal_html = ''
    audience_html = ''
    usecase_html = ''

    # Extract prose (paragraphs before the number)
    prose_section = re.search(r'<div class="body">(.*?)<div class="num">', html, re.DOTALL)
    if prose_section:
        raw = prose_section.group(1)
        ps = re.findall(r'<p[^>]*>(.*?)</p>', raw, re.DOTALL)
        prose_lines = []
        for p in ps:
            # Convert span.bold to .bold class
            p_clean = p.replace('<span class="bold">', '<span class="bold">').strip()
            if 'class="gray"' in raw and p == ps[1] if len(ps) > 1 else False:
                prose_lines.append(f'  <p class="muted">{p_clean}</p>')
            else:
                # Check if this paragraph had gray class
                prose_lines.append(f'  <p>{p_clean}</p>')
        prose_html = '<div class="prose">\n' + '\n'.join(prose_lines) + '\n</div>'
    
    # Better prose extraction - handle gray class
    prose_section2 = re.search(r'<div class="body">(.*?)<div class="num">', html, re.DOTALL)
    if prose_section2:
        raw = prose_section2.group(1)
        prose_lines = []
        for m in re.finditer(r'<p(\s+class="([^"]*)")?\s*>(.*?)</p>', raw, re.DOTALL):
            cls = m.group(2) or ''
            content = m.group(3).strip()
            if 'gray' in cls:
                prose_lines.append(f'  <p class="muted">{content}</p>')
            else:
                prose_lines.append(f'  <p>{content}</p>')
        if prose_lines:
            prose_html = '<div class="prose">\n' + '\n'.join(prose_lines) + '\n</div>'

    # Extract number
    num_match = re.search(r'<div class="num">(.*?)</div>\s*<div class="num-sub">(.*?)</div>', html, re.DOTALL)
    if num_match:
        num_html = f'''<div class="num-block">
  <div class="num">{num_match.group(1).strip()}</div>
  <div class="num-sub">{num_match.group(2).strip()}</div>
</div>'''

    # Extract highlight/emphasis
    highlight_match = re.search(r'<div class="highlight">\s*<p>(.*?)</p>\s*</div>', html, re.DOTALL)
    if highlight_match:
        emphasis_html = f'''<div class="emphasis">
  <p>{highlight_match.group(1).strip()}</p>
</div>'''

    # Extract signal
    signal_items = re.findall(r'<div class="s-text">(.*?)</div>', html)
    if signal_items:
        items = '\n'.join(f'  <div class="signal-item"><div class="signal-dot"></div><div class="signal-text">{s.strip()}</div></div>' for s in signal_items)
        signal_html = f'''<div class="signal">
  <div class="signal-label">DMP SIGNAL</div>
{items}
</div>'''

    # Extract audience
    aud_h3 = re.search(r'<div class="audience">\s*<h3>(.*?)</h3>\s*<div class="a-num">(.*?)</div>\s*<div class="a-basis">(.*?)</div>', html, re.DOTALL)
    if aud_h3:
        audience_html = f'''<div class="aud-card">
  <h3>{aud_h3.group(1).strip()}</h3>
  <div class="aud-num">{aud_h3.group(2).strip()}</div>
  <div class="aud-basis">{aud_h3.group(3).strip()}</div>
</div>'''

    # Extract use cases
    usecase_items = re.findall(r'<div class="u-who">(.*?)</div>\s*<div class="u-how">(.*?)</div>', html, re.DOTALL)
    if usecase_items:
        items = '\n'.join(f'''  <div class="usecase-item">
    <div class="usecase-who">{who.strip()}</div>
    <div class="usecase-how">{how.strip()}</div>
  </div>''' for who, how in usecase_items)
        usecase_html = f'''<div class="usecase">
  <div class="usecase-label">이 오디언스를 쓸 수 있는 광고주</div>
{items}
</div>'''

    # Combine content
    content_parts = [p for p in [prose_html, num_html, emphasis_html, signal_html, audience_html, usecase_html] if p]
    content = '\n\n'.join(content_parts)

    return title, category, headline, content


def convert_file(filepath):
    fname = os.path.basename(filepath)
    if fname in ('index.html', 'test.html'):
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already converted
    if '#fafaf7' in html:
        return False

    # Must have the essay structure
    if '<div class="body">' not in html and '<div class="num">' not in html:
        return False

    title, category, headline, content = extract_content(html)

    if not headline or not content:
        print(f"  SKIP (no content): {fname}")
        return False

    result = FRITZ_TEMPLATE.format(
        title=title,
        category=category,
        headline=headline,
        content=content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)
    return True


count = 0
for fname in sorted(os.listdir(DOCS_DIR)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(DOCS_DIR, fname)
    if convert_file(fpath):
        print(f"✓ {fname}")
        count += 1
    else:
        print(f"  skip: {fname}")

print(f"\n완료 — {count}개 파일 변환됨")
