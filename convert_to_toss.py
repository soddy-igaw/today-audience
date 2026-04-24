"""기존 essays_html을 토스 스타일로 변환"""
import os, re
from bs4 import BeautifulSoup

DIR = os.path.dirname(os.path.abspath(__file__))
ESSAYS_DIR = os.path.join(DIR, "essays_html")

TOSS_CSS = """<style>
body{background:#f7f7fa !important}
.wrap{max-width:800px}
a{color:inherit;text-decoration:none}
.back{display:inline-block;padding:18px 0;font-size:.85rem;color:#999;cursor:pointer}
.back:hover{color:#333}
.hero{padding:8px 0 32px}
.hero .tag{font-size:.72rem;font-weight:600;color:#888;letter-spacing:.3px;margin-bottom:16px}
.hero h1{font-size:1.75rem;font-weight:900;line-height:1.38;letter-spacing:-.5px;color:#111;margin-bottom:14px}
.hero .sub{font-size:.95rem;color:#888;line-height:1.7}
.hero .meta{font-size:.72rem;color:#ccc;margin-top:16px}
.punchline{background:#111;margin:0 -24px;padding:36px 28px}
.punchline p{font-size:1.15rem;font-weight:700;color:#fff;line-height:1.7}
.punchline strong{color:#e8530e;font-weight:800}
.card{background:#fff;border-radius:16px;padding:28px 24px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.quote{border-left:3px solid #ddd;padding:22px 24px;background:#fff;border-radius:0 14px 14px 0;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.quote p{font-size:.93rem;color:#888;line-height:1.85;font-style:italic}
.quote strong{color:#333;font-style:normal}
.quote .from{font-size:.72rem;color:#bbb;margin-top:10px;font-style:normal}
.s-label{font-size:.68rem;font-weight:700;color:#bbb;letter-spacing:1.5px;margin-bottom:14px}
.s-title{font-size:1.15rem;font-weight:800;line-height:1.4;color:#111;margin-bottom:16px}
.steps{display:flex;flex-direction:column;gap:10px}
.step{background:#f7f7fa;border-radius:12px;padding:20px 22px}
.step.active{background:#fff;border:1.5px solid #111}
.step-num{font-size:.6rem;font-weight:700;color:#ccc;letter-spacing:1.5px;margin-bottom:6px}
.step.active .step-num{color:#111}
.step-title{font-size:.95rem;font-weight:700;color:#333;margin-bottom:4px}
.step.active .step-title{color:#111;font-weight:800}
.step-desc{font-size:.82rem;color:#999;line-height:1.6}
.highlight-line{padding:28px 0;text-align:center}
.highlight-line p{font-size:1.05rem;font-weight:800;color:#111;line-height:1.6}
.highlight-line span{color:#888;font-weight:500}
.compare{display:grid;grid-template-columns:1fr 1fr;gap:0;border-radius:12px;overflow:hidden;margin-top:12px}
.compare-col{padding:20px}
.compare-col:first-child{background:#f7f7fa}
.compare-col:last-child{background:#111}
.compare-col h4{font-size:.66rem;font-weight:700;color:#bbb;letter-spacing:1px;margin-bottom:10px}
.compare-col:last-child h4{color:#888}
.compare-col li{list-style:none;font-size:.82rem;color:#999;padding:3px 0;line-height:1.5}
.compare-col:last-child li{color:#aaa}
.compare-col:last-child strong{color:#fff}
.audience-box{background:#111;border-radius:16px;padding:40px 28px;margin-bottom:14px;text-align:center;color:#fff}
.audience-box h3{font-size:1.1rem;font-weight:800;margin-bottom:10px}
.audience-box .a-num{font-size:2.4rem;font-weight:900;color:#e8530e;margin-bottom:6px}
.audience-box .a-basis{font-size:.7rem;color:#666}
.audience-box .a-desc{font-size:.92rem;color:#999;margin-top:20px;line-height:1.7}
.audience-box .a-desc strong{color:#fff}
.biz-item{border-bottom:1px solid #f0f0f0}
.biz-item:last-child{border:none}
.biz-head{display:flex;align-items:center;gap:12px;padding:16px 0;cursor:pointer}
.biz-icon{font-size:1.2rem}
.biz-name{font-size:.88rem;font-weight:700;flex:1;color:#222}
.biz-toggle{font-size:1rem;color:#ccc;transition:transform .2s}
.biz-item.open .biz-toggle{transform:rotate(45deg);color:#111}
.biz-body{max-height:0;overflow:hidden;transition:max-height .3s ease}
.biz-item.open .biz-body{max-height:200px}
.biz-body-inner{padding:0 0 16px}
.biz-body-inner p{font-size:.85rem;color:#888;line-height:1.7;margin-bottom:8px}
.biz-action{font-size:.82rem;font-weight:700;color:#111}
.cta-bar{background:#111;border-radius:12px;padding:18px 24px;text-align:center;margin-bottom:14px}
.cta-bar p{font-size:.85rem;font-weight:700;color:#fff;margin:0}
.footer{text-align:center;color:#ccc;font-size:.68rem;padding:32px 0 16px}
</style>"""

def convert_essay(filepath):
    with open(filepath, 'r') as f:
        html = f.read()
    
    # Already converted
    if 'body{background:#f7f7fa' in html:
        return False
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract data from old structure
    tag_el = soup.select_one('.detail-tag')
    title_el = soup.select_one('.detail-title')
    meta_el = soup.select_one('.detail-meta')
    
    if not tag_el or not title_el:
        return False
    
    tag = tag_el.get_text(strip=True)
    title_html = str(title_el).replace('<div class="detail-title">', '').replace('</div>', '')
    meta = meta_el.get_text(strip=True) if meta_el else ''
    
    # Extract quote
    quote_box = soup.select_one('.quote-box')
    quote_html = ""
    if quote_box:
        quote_p = quote_box.find('p')
        quote_from_el = quote_box.select_one('div[style*="color:#999"]')
        quote_from = quote_from_el.get_text(strip=True) if quote_from_el else ''
        if quote_p:
            # Fix strong style for toss
            p_html = str(quote_p)
            p_html = p_html.replace('style="color:#000;font-style:normal"', '')
            quote_html = f"""<div class="quote">
  {p_html}
  <div class="from">{quote_from}</div>
</div>"""
    
    # Extract punchline (the bold statement after quote)
    punchline_text = ""
    punch_divs = soup.select('div[style*="padding:32px 0"]')
    if punch_divs:
        first_punch = punch_divs[0]
        p = first_punch.find('p')
        if p:
            p_str = str(p)
            p_str = re.sub(r'style="[^"]*"', '', p_str)
            punchline_text = p_str
    
    # Extract "왜 지금인가" section
    why_now_html = ""
    sections = soup.select('.section')
    for sec in sections:
        label = sec.select_one('.section-label')
        if label and '왜 지금인가' in label.get_text():
            paragraphs = sec.select('p')
            content = '\n'.join(str(p) for p in paragraphs)
            # Wrap in card
            why_now_html = f"""<div class="card">
  <div class="s-label">왜 지금인가</div>
  {content}
</div>"""
            break
    
    # Extract behavior steps
    steps_html = ""
    for sec in sections:
        label = sec.select_one('.section-label')
        if label and '일주일' in label.get_text():
            cards = sec.select('.behavior-card')
            steps_inner = ""
            for card in cards:
                step_el = card.select_one('.bc-step')
                title_step = card.select_one('.bc-title')
                desc_el = card.select_one('.bc-desc')
                is_active = 'highlight' in card.get('class', [])
                cls = ' active' if is_active else ''
                steps_inner += f"""    <div class="step{cls}">
      <div class="step-num">{step_el.get_text(strip=True) if step_el else ''}</div>
      <div class="step-title">{title_step.get_text(strip=True) if title_step else ''}</div>
      <div class="step-desc">{desc_el.get_text(strip=True) if desc_el else ''}</div>
    </div>\n"""
            steps_html = f"""<div class="card">
  <div class="s-label">이 사람의 일주일</div>
  <div class="steps">
{steps_inner}  </div>
</div>"""
            break
    
    # Extract "왜 매력적인가"
    attractive_html = ""
    for pd in punch_divs:
        p = pd.find('p')
        if p and '매력적' in p.get_text():
            all_p = pd.select('p')
            text_parts = []
            for ap in all_p:
                text_parts.append(ap.get_text(strip=True))
            if len(text_parts) >= 2:
                attractive_html = f"""<div class="highlight-line">
  <p>{text_parts[0]}<br><span>{text_parts[1]}</span></p>
</div>"""
            elif text_parts:
                attractive_html = f"""<div class="highlight-line">
  <p>{text_parts[0]}</p>
</div>"""
            break
    
    # Extract compare grid
    compare_html = ""
    compare_grid = soup.select('div[style*="grid-template-columns:1fr 1fr"]')
    if compare_grid:
        cols = compare_grid[0].select('div[style*="padding:20px"]')
        if len(cols) >= 2:
            col1_label = cols[0].select_one('div[style*="font-weight:700"]')
            col1_items = cols[0].select_one('div[style*="line-height:1.8"]')
            col2_label = cols[1].select_one('div[style*="font-weight:700"]')
            col2_items = cols[1].select_one('div[style*="line-height:1.8"]')
            
            def items_to_li(el):
                if not el: return ''
                text = str(el)
                # Split by <br> or <br/>
                parts = re.split(r'<br\s*/?>', text)
                lis = ''
                for part in parts:
                    clean = re.sub(r'<[^>]+>', '', part).strip()
                    if clean:
                        if '<strong' in part:
                            strong_match = re.search(r'<strong[^>]*>(.*?)</strong>', part)
                            if strong_match:
                                lis += f'        <li><strong>{strong_match.group(1)}</strong></li>\n'
                                continue
                        lis += f'        <li>{clean}</li>\n'
                return lis
            
            l1 = col1_label.get_text(strip=True) if col1_label else ''
            l2 = col2_label.get_text(strip=True) if col2_label else ''
            
            compare_html = f"""<div class="card">
  <div class="s-label">뭐가 다른가</div>
  <div class="compare">
    <div class="compare-col">
      <h4>{l1}</h4>
      <ul>
{items_to_li(col1_items)}      </ul>
    </div>
    <div class="compare-col">
      <h4>{l2}</h4>
      <ul>
{items_to_li(col2_items)}      </ul>
    </div>
  </div>
</div>"""
    
    # Extract audience box
    audience_html = ""
    aud_div = soup.select_one('div[style*="background:#000"][style*="padding:48px"]')
    if aud_div:
        h3 = aud_div.find('h3')
        num_el = aud_div.select_one('p[style*="font-size:2rem"]')
        basis_el = aud_div.select_one('p[style*="font-size:.72rem"]')
        desc_el = aud_div.select_one('p[style*="font-size:.92rem"]')
        
        h3_text = str(h3).replace('<h3', '<h3').strip() if h3 else ''
        h3_inner = h3.decode_contents() if h3 else ''
        num_text = num_el.get_text(strip=True) if num_el else ''
        basis_text = basis_el.get_text(strip=True) if basis_el else ''
        desc_inner = desc_el.decode_contents() if desc_el else ''
        
        audience_html = f"""<div class="audience-box">
  <h3>{h3_inner}</h3>
  <div class="a-num">{num_text}</div>
  <div class="a-basis">{basis_text}</div>
  <div class="a-desc">{desc_inner}</div>
</div>"""
    
    # Extract biz items
    biz_html = ""
    biz_items = soup.select('.biz-item')
    if biz_items:
        biz_inner = ""
        for item in biz_items:
            icon_el = item.select_one('.biz-icon')
            for_el = item.select_one('.biz-for')
            body_el = item.select_one('.biz-body')
            
            icon = icon_el.get_text(strip=True) if icon_el else ''
            for_text = for_el.get_text(strip=True) if for_el else ''
            
            body_content = ""
            if body_el:
                h4 = body_el.find('h4')
                p = body_el.find('p')
                action = body_el.select_one('.biz-action')
                h4_text = h4.get_text(strip=True) if h4 else ''
                p_text = p.get_text(strip=True) if p else ''
                action_text = action.get_text(strip=True) if action else ''
                body_content = f'<div class="biz-body-inner"><p>{p_text}</p><div class="biz-action">{action_text}</div></div>'
            
            biz_inner += f"""  <div class="biz-item" onclick="this.classList.toggle('open')">
    <div class="biz-head"><span class="biz-icon">{icon}</span><span class="biz-name">{for_text}</span><span class="biz-toggle">+</span></div>
    <div class="biz-body">{body_content}</div>
  </div>\n"""
        
        biz_html = f"""<div class="card">
  <div class="s-label">이 오디언스를 쓸 수 있는 광고주</div>
{biz_inner}</div>"""
    
    # Extract footer
    footer_el = soup.select_one('.footer')
    footer_text = footer_el.get_text(strip=True) if footer_el else ''
    
    # Extract sub from punchline
    sub_text = ""
    if punchline_text:
        # Get text without tags for sub
        sub_soup = BeautifulSoup(punchline_text, 'html.parser')
        sub_text = sub_soup.get_text(strip=True)
    
    # Build toss-style HTML
    result = f"""{TOSS_CSS}

<div class="back" onclick="history.back()">← 오늘의 오디언스</div>

<div class="hero">
  <div class="tag">{tag} · {meta.split('·')[0].strip() if '·' in meta else ''}</div>
  <h1>{title_html}</h1>
  <div class="meta">{meta}</div>
</div>

<div class="punchline">
  {punchline_text}
</div>

<div style="height:20px"></div>

{quote_html}

{why_now_html}

{steps_html}

{attractive_html}

{compare_html}

{audience_html}

{biz_html}

<div class="cta-bar">
  <p>이 오디언스 활용 요청하기 → audiencelab@igaworks.com</p>
</div>

<div class="footer">{footer_text}</div>
"""
    
    with open(filepath, 'w') as f:
        f.write(result)
    return True

# Convert all essays
count = 0
for fname in os.listdir(ESSAYS_DIR):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(ESSAYS_DIR, fname)
    if convert_essay(fpath):
        print(f"CONVERTED: {fname}")
        count += 1
    else:
        print(f"SKIP: {fname}")

print(f"\nDone — {count} files converted")
