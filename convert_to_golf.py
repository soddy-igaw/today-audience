#!/usr/bin/env python3
"""Convert old-style essays to golf.html structure (indigo/longblack tone)."""
import re, os
from bs4 import BeautifulSoup

TEMPLATE_TOP = '''<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/sun-typeface/SUIT@2/fonts/variable/woff2/SUIT-Variable.css">
<style>
body{background:#fff !important;margin:0;padding:0;font-family:'SUIT',sans-serif;letter-spacing:-.2px}
*{box-sizing:border-box}
.wrap{max-width:580px;margin:0 auto;padding:32px 24px 60px}
a{color:inherit;text-decoration:none}
.back{display:inline-block;padding:0 0 40px;font-size:.82rem;color:#bbb}
.tag-line{font-size:.75rem;font-weight:600;color:#999;letter-spacing:.3px;margin-bottom:32px}
.title{font-size:1.6rem;font-weight:900;color:#111;line-height:1.4;margin-bottom:48px}
.body{font-size:.93rem;color:#444;line-height:2.8}
.body p{margin:0 0 32px}
.body .editor{color:#111;font-weight:600}
.body .accent{color:#111;font-weight:700}
.body .muted{color:#bbb}
.body .orange{color:#6366F1;font-weight:700}
.body .divider{border:none;border-top:1px solid #f0f0f0;margin:48px 0}
.body .speaker{font-size:.72rem;font-weight:700;color:#6366F1;letter-spacing:1px;margin-bottom:8px}
.num-block{text-align:center;padding:48px 0}
.num-block .num{font-size:2.8rem;font-weight:900;color:#6366F1}
.num-block .label{font-size:.72rem;color:#999;margin-top:6px}
.usecase{margin:48px 0;background:#f5f3ff;border-radius:14px;padding:28px 24px}
.usecase-title{font-size:.82rem;font-weight:800;color:#111;margin-bottom:20px}
.usecase-item{padding:16px 0;border-bottom:1px solid rgba(0,0,0,.05)}
.usecase-item:last-child{border:none}
.usecase-item .who{font-size:.88rem;font-weight:700;color:#111;margin-bottom:6px}
.usecase-item .how{font-size:.82rem;color:#888;line-height:1.7}
.cta{text-align:center;padding:48px 0;border-top:1px solid #f0f0f0}
.cta a{font-size:.82rem;font-weight:700;color:#fff;background:#6366F1;padding:14px 32px;border-radius:8px;display:inline-block}
.footer{text-align:center;color:#ddd;font-size:.62rem;padding:24px 0;line-height:1.8}
</style>
'''

def extract_info(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    # Title
    title = ''
    h1 = soup.find('h1')
    if h1:
        title = h1.get_text(strip=True)
    if not title:
        t = soup.find(class_='title')
        if t:
            title = t.get_text(strip=True)
    
    # Tag line
    tag_line = ''
    tag_el = soup.find(class_='tag')
    if tag_el:
        tag_line = tag_el.get_text(strip=True)
    if not tag_line:
        tag_el = soup.find(class_='tag-line')
        if tag_el:
            tag_line = tag_el.get_text(strip=True)
    
    # Subtitle/hook
    sub = ''
    sub_el = soup.find(class_='sub')
    if sub_el:
        sub = sub_el.get_text(strip=True)
    if not sub:
        sub_el = soup.find(class_='hook-sub')
        if sub_el:
            sub = sub_el.get_text(strip=True)
    
    # Audience number
    num = ''
    num_el = soup.find(class_='a-num')
    if num_el:
        num = num_el.get_text(strip=True)
    if not num:
        num_el = soup.find(class_='num')
        if num_el:
            num = num_el.get_text(strip=True)
    
    # Audience basis/label
    basis = ''
    basis_el = soup.find(class_='a-basis')
    if basis_el:
        basis = basis_el.get_text(strip=True)
    if not basis:
        basis_el = soup.find(class_='label')
        if basis_el:
            basis = basis_el.get_text(strip=True)
    
    # Business items (usecase)
    usecases = []
    # Old card style
    biz_items = soup.find_all(class_='biz-item')
    if biz_items:
        for bi in biz_items:
            name_el = bi.find(class_='biz-name')
            body_el = bi.find(class_='biz-body-inner')
            if name_el and body_el:
                name = name_el.get_text(strip=True)
                desc_p = body_el.find('p')
                desc = desc_p.get_text(strip=True) if desc_p else ''
                usecases.append((name, desc))
    
    # New usecase style
    if not usecases:
        uc_items = soup.find_all(class_='usecase-item')
        for ui in uc_items:
            who_el = ui.find(class_='who')
            how_el = ui.find(class_='how')
            if who_el and how_el:
                usecases.append((who_el.get_text(strip=True), how_el.get_text(strip=True)))
    
    # Steps for timeline
    steps = []
    step_els = soup.find_all(class_='step')
    for s in step_els:
        sn = s.find(class_='step-num')
        st = s.find(class_='step-title')
        sd = s.find(class_='step-desc')
        if st and sd:
            label = sn.get_text(strip=True) if sn else ''
            steps.append((label, st.get_text(strip=True), sd.get_text(strip=True)))
    
    # Punchline
    punch = ''
    punch_el = soup.find(class_='punchline')
    if punch_el:
        p_tag = punch_el.find('p')
        if p_tag:
            punch = p_tag.get_text(' ', strip=True)
    
    # Quote
    quote = ''
    quote_el = soup.find(class_='quote')
    if quote_el:
        p_tag = quote_el.find('p')
        if p_tag:
            quote = p_tag.get_text(' ', strip=True)

    # Highlight
    highlight = ''
    hl_el = soup.find(class_='highlight-line')
    if hl_el:
        p_tag = hl_el.find('p')
        if p_tag:
            highlight = p_tag.get_text(' ', strip=True)

    return {
        'title': title,
        'tag_line': tag_line,
        'sub': sub,
        'num': num,
        'basis': basis,
        'usecases': usecases,
        'steps': steps,
        'punch': punch,
        'quote': quote,
        'highlight': highlight,
    }


def build_timeline(steps):
    if not steps:
        return ''
    items = ''
    for i, (label, title, desc) in enumerate(steps):
        is_last = (i == len(steps) - 1)
        padding = '0 0 0 24px' if is_last else '0 0 28px 24px'
        items += f'''    <div style="position:relative;padding:{padding}">
      <div style="position:absolute;left:-6px;top:6px;width:14px;height:14px;background:#6366F1;border-radius:50%;border:3px solid #f5f3ff"></div>
      <div style="font-size:.68rem;font-weight:700;color:#6366F1;margin-bottom:4px">{label}</div>
      <div style="font-size:.88rem;font-weight:700;color:#111">{title}</div>
      <div style="font-size:.75rem;color:#888;margin-top:3px">{desc}</div>
    </div>
'''
    return f'''<div style="background:#f5f3ff;border-radius:14px;padding:28px 24px;margin:36px 0">
  <div style="font-size:.82rem;font-weight:800;color:#6366F1;margin-bottom:24px">시그널 타임라인</div>
  <div style="position:relative;padding:0 0 0 20px">
    <div style="position:absolute;left:8px;top:8px;bottom:8px;width:2px;background:linear-gradient(to bottom,#6366F1,#a5b4fc)"></div>
{items}  </div>
</div>'''


def build_usecase(usecases):
    if not usecases:
        return ''
    items = ''
    for who, how in usecases:
        items += f'''  <div class="usecase-item">
    <div class="who">{who}</div>
    <div class="how">{how}</div>
  </div>
'''
    return f'''<div class="usecase">
  <div class="usecase-title">이 사람한테 뭘 팔 수 있을까요?</div>
{items}</div>'''


def convert_file(filepath):
    info = extract_info(filepath)
    if not info['title']:
        print(f"SKIP (no title): {filepath}")
        return
    
    # Build body narrative from available content
    body_parts = []
    
    if info['sub']:
        body_parts.append(f'<p>{info["sub"]}</p>')
    if info['punch']:
        body_parts.append(f'<p class="muted">{info["punch"]}</p>')
    
    body_parts.append('<hr class="divider">')
    body_parts.append('<p class="speaker">이 사람은 누구인가</p>')
    
    if info['highlight']:
        body_parts.append(f'<p><span class="accent">{info["highlight"]}</span></p>')
    elif info['quote']:
        body_parts.append(f'<p><span class="accent">{info["quote"]}</span></p>')
    else:
        body_parts.append(f'<p><span class="accent">이 사람은 지금 행동하는 중입니다.</span></p>')
    
    body_parts.append('<hr class="divider">')
    body_parts.append('<p class="speaker">우리가 잡은 시그널</p>')
    body_parts.append('<p><span class="editor">앱 하나로는 안 잡힙니다. 우리는 앱 조합과 타이밍을 봤습니다.</span></p>')
    
    body_content = '\n\n'.join(body_parts)
    
    timeline = build_timeline(info['steps'])
    usecase_html = build_usecase(info['usecases'])
    
    # Urgency paragraph
    urgency = f'<div class="body">\n<p><span class="editor">이 {info["num"]}을 지금 누가 찾고 있을까요? 지금이 광고 타이밍입니다.</span></p>\n</div>' if info['num'] else ''
    
    num_block = ''
    if info['num']:
        num_block = f'''<div class="num-block">
  <div class="num">{info["num"]}</div>
  <div class="label">{info["basis"]}</div>
  <div style="font-size:.65rem;color:#ccc;margin-top:4px">* 예상 모수 · 조건 세분화 시 변동 가능</div>
</div>'''

    output = f'''{TEMPLATE_TOP}
<div class="back" onclick="history.back()">← 오늘의 오디언스</div>
<div class="tag-line">{info["tag_line"]}</div>

<div class="title">{info["title"]}</div>

<div class="body">

{body_content}

</div>

{timeline}

{urgency}

{num_block}

{usecase_html}

<div class="cta">
  <a href="mailto:audiencelab@igaworks.com">이 오디언스 활용 문의 →</a>
</div>

<div class="footer">IGAWorks DMP 행동 데이터 기반 · 모바일인덱스 실측 · © 2026<br>made by soddy</div>
'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"OK: {os.path.basename(filepath)}")


if __name__ == '__main__':
    target_dir = '/home/soddy/today-audience/essays_html'
    files = [
        'car.html', 'carinsurance.html', 'finance.html', 'finance_0427.html',
        'game.html', 'health.html', 'health_0428.html', 'ktx.html',
        'realestate.html', 'realestate_0421.html', 'realestate_0422.html',
        'running.html', 'shopping_0423.html', 'stock.html', 'themestock.html',
        'travel.html', 'wegovy.html', '금융_0420.html', '자동차_0425.html'
    ]
    for f in files:
        convert_file(os.path.join(target_dir, f))
