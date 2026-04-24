"""에세이 톤 수정: 줄바꿈 복원 + em dash 공백 + 단정 톤 완화"""
import os, re

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "essays_html")

def fix_tone(html):
    # 1. 문장 붙어있는 것 수정: "입니다.지금" → "입니다.<br>지금"
    html = re.sub(r'(입니다|습니다|됩니다|겁니다|있습니다)\.(지금|이|그|이미|살|비교|처음|러닝|신작|약|금|2주|여행|결제|교통|안전|전세|사료)\b',
                  r'\1.<br>\2', html)
    
    # 2. em dash 뒤 공백 없는 것 수정: "—이", "—모든" → "— 이", "— 모든"
    html = re.sub(r'—([^\s<])', r'— \1', html)
    
    # 3. 단정 톤 완화 (highlight-line/span 안에서)
    # "보여주면 됩니다" → "보여주면 됩니다" (이건 OK, 광고주 대상이라 단정 괜찮음)
    
    # 4. punchline 안 줄바꿈 개선: <strong> 앞에 <br> 없으면 추가
    html = re.sub(r'([^>])<strong\s*>', r'\1<br><strong>', html)
    # 이미 <br><strong> 인 경우 중복 방지
    html = html.replace('<br/><br><strong', '<br><strong')
    html = html.replace('<br><br><strong', '<br><strong')
    
    return html

count = 0
for fname in os.listdir(DIR):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(DIR, fname)
    with open(fpath, 'r') as f:
        original = f.read()
    
    fixed = fix_tone(original)
    
    if fixed != original:
        with open(fpath, 'w') as f:
            f.write(fixed)
        print(f"FIXED: {fname}")
        count += 1
    else:
        print(f"OK: {fname}")

print(f"\n{count} files fixed")
