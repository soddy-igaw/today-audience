"""정적 사이트 빌드 스크립트 — docs/ 폴더에 생성"""
import os, json

DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DIR, "docs")
os.makedirs(OUT, exist_ok=True)

ESSAYS = [
    {"id":"realestate","tag":"부동산","title":"전세 만기 앞두고 내 차 시세부터 조회한 사람","sub":"주담대 한도가 부족할 때, 자동차가 두 번째 담보가 됩니다","stat":"~34만","stat_label":"부동산+대출앱 동시 사용자 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=400&fit=crop&q=80"},
    {"id":"wegovy","tag":"헬스","title":"위고비 처방받고 헬스장 끊은 사람","sub":"GLP-1 다이어트약 처방이 폭발하면서, 운동으로 빼는 사람과 약으로 빼는 사람이 갈리고 있습니다","stat":"~18만","stat_label":"병원예약+약국앱 동시 활성 (DMP)","date":"2026.04.16","img":"https://images.unsplash.com/photo-1505576399279-0d754c0ce141?w=800&h=400&fit=crop&q=80"},
    {"id":"car","tag":"자동차","title":"전기차 앱 지우고 하이브리드 비교앱 깐 사람","sub":"보조금 축소 뉴스 보고 전기차를 포기한 게 아니라, 선택지를 바꾼 겁니다","stat":"~80만","stat_label":"자동차앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&h=400&fit=crop&q=80"},
    {"id":"game","tag":"게임","title":"스위치2 예약 알림 켜고 게이밍 노트북 비교 시작한 사람","sub":"신작 출시 전 게임 커뮤니티 접속이 3배 뛰면, 하드웨어 지갑이 열립니다","stat":"~140만","stat_label":"게임앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=800&h=400&fit=crop&q=80"},
    {"id":"stock","tag":"증권","title":"미국주식 앱 알림을 끄고 금 시세앱을 깐 사람","sub":"트럼프 관세에 미장을 판 서학개미, 금으로 갈아탔습니다","stat":"~97만","stat_label":"증권앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop&q=80"},
    {"id":"ktx","tag":"여행","title":"KTX 매진 뜨자마자 고속버스앱 깐 사람","sub":"외국인 관광객이 KR Pass로 좌석을 쓸어가면, 내국인은 대안 교통을 찾기 시작합니다","stat":"~27만","stat_label":"코레일+교통앱 동시 활성 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800&h=400&fit=crop&q=80"},
    {"id":"travel","tag":"여행","title":"해외여행 앱을 지우고 국내 펜션앱을 깐 사람","sub":"환율 1,450원 시대, 여행을 포기한 게 아니라 방향을 바꾼 겁니다","stat":"~65만","stat_label":"여행앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&h=400&fit=crop&q=80"},
    {"id":"pet","tag":"반려동물","title":"첫 입양 후 2주, 앱이 폭발하는 사람","sub":"2주 안에 펫앱 3개를 동시에 까는 사람은 3년 고객이 됩니다","stat":"~13만","stat_label":"펫앱+커머스 (DMP)","date":"2026.04.13","img":"https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800&h=400&fit=crop&q=80"},
    {"id":"themestock","tag":"테마주","title":"뉴스 보고 30분 안에 종목 검색한 사람","sub":"광통신 600% 폭등 뉴스에 증권앱 검색이 터진 사람","stat":"~52만","stat_label":"뉴스+증권앱 동시 활성 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop&q=80"},
    {"id":"carinsurance","tag":"금융","title":"자동차보험 만기 알림 뜨고 비교앱 3개 깐 사람","sub":"작년보다 15만원 올랐다면, 지금 갈아타세요","stat":"~41만","stat_label":"보험사+비교앱 동시 활성 (DMP)","date":"2026.04.16","img":"https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&h=400&fit=crop&q=80"},
    {"id":"finance","tag":"금융","title":"대출앱 3개를 동시에 깐 사람의 비밀","sub":"불 난 사람한테 소화기 할인 쿠폰을 보내지 마세요","stat":"~10만","stat_label":"대출탐색 유저 (DMP)","date":"2026.04.10","img":"https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop&q=80"},
    {"id":"running","tag":"러닝","title":"러닝화 2켤레 사고 주말마다 한강에서 뛰는 사람","sub":"커머스에서 15만원짜리 러닝화를 반복 조회하면서, 주말 아침 한강에 나타나는 사람","stat":"~48만","stat_label":"러닝앱+커머스 동시 활성 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800&h=400&fit=crop&q=80"},
    {"id":"golf","tag":"골프","title":"드라이버를 사는 게 아니라 창피를 안 당할 보험을 삽니다","sub":"접대 골프 입문자는 고민하지 않습니다. 빠르게 삽니다.","stat":"~17만","stat_label":"골프앱 사용자 (DMP)","date":"2026.04.11","img":"https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800&h=400&fit=crop&q=80"},
    {"id":"health","tag":"건강","title":"러닝앱 깔고 3일 만에 식단앱까지 깐 사람","sub":"다이어트를 결심한 게 아니라, 몸이 바뀌기 시작한 겁니다","stat":"~103만","stat_label":"운동앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=400&fit=crop&q=80"},
]

CHAPTERS = [
    {"label":"금융","ids":["finance","stock","realestate","themestock","carinsurance"]},
    {"label":"여행","ids":["travel","ktx"]},
    {"label":"스포츠","ids":["running","golf","health","wegovy"]},
    {"label":"라이프","ids":["car","pet"]},
    {"label":"게임","ids":["game"]},
]

CSS = open(os.path.join(DIR, "essays_html", "realestate.html")).read()[:0]  # just init
# Read CSS from a shared string
CSS = """
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:'Pretendard',sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:900px;margin:0 auto;padding:0 24px 100px}
.hero-img{width:100%;height:280px;object-fit:cover;filter:grayscale(100%)}
.detail-wrap{max-width:600px;margin:0 auto}
.detail-hero{padding:32px 0;margin-bottom:16px;border-bottom:1px solid #e5e5e5}
.detail-emoji{font-size:2.4rem;margin-bottom:16px}
.detail-tag{display:inline-block;font-size:.68rem;font-weight:600;color:#000;background:#f0f0f0;padding:3px 10px;margin-bottom:12px}
.detail-title{font-size:1.4rem;font-weight:900;color:#000;line-height:1.35;margin-bottom:8px}
.detail-sub{font-size:.88rem;color:#666;line-height:1.6}
.detail-meta{font-size:.72rem;color:#999;margin-top:16px}
.section{padding:28px 0;border-bottom:1px solid #f0f0f0}
.section-label{font-size:.68rem;font-weight:700;color:#000;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:14px}
.section p{color:#333;font-size:1.02rem;line-height:1.85;margin-bottom:16px}
.section strong{color:#000}
.quote-box{background:#f7f7f7;padding:24px;margin-bottom:14px;border-left:3px solid #000}
.quote-box p{color:#444;font-size:1rem;line-height:1.8;font-style:italic;margin:0}
.cmp-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.cmp-card{padding:20px}
.cmp-card h4{font-size:.72rem;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;font-weight:700}
.cmp-card p{font-size:.82rem;line-height:1.8;margin:0}
.cmp-left{background:#f7f7f7}.cmp-left h4{color:#999}.cmp-left p{color:#888}
.cmp-right{background:#000}.cmp-right h4{color:#999}.cmp-right p{color:#fff}
.ind-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.ind-card{background:#f7f7f7;padding:16px}
.ind-card .ind-title{font-size:.82rem;font-weight:700;color:#000;margin-bottom:4px}
.ind-card .ind-desc{font-size:.75rem;color:#888;line-height:1.4}
.insight-box{background:#000;padding:28px 24px;margin-bottom:14px}
.insight-box .ins-label{font-size:.68rem;color:#888;font-weight:700;letter-spacing:1.5px;margin-bottom:12px}
.insight-box p{color:#fff;font-size:.92rem;line-height:1.8;font-weight:500;margin:0}
.audience-card{background:#000;padding:28px 24px;margin-bottom:14px}
.ad-compare{background:#fff;padding:28px 24px;margin-bottom:14px;border:1px solid #e5e5e5}
.tl{padding-left:24px;border-left:2px solid #ddd;margin-left:6px}
.tl-item{margin-bottom:24px;position:relative}
.tl-dot{position:absolute;left:-30px;top:3px;width:10px;height:10px;border-radius:50%;border:2px solid #fff}
.tl-green{background:#000;box-shadow:0 0 0 2px #000}
.tl-yellow{background:#888;box-shadow:0 0 0 2px #888}
.tl-red{background:#000;box-shadow:0 0 0 2px #000}
.tl-day{font-size:.68rem;font-weight:700;margin-bottom:4px;color:#000}
.tl-title{font-size:.88rem;font-weight:700;color:#000;margin-bottom:2px}
.tl-desc{font-size:.78rem;color:#888}
.tl-bar-wrap{margin-top:8px;background:#f7f7f7;padding:8px 12px}
.tl-bar-bg{background:#e5e5e5;height:6px;overflow:hidden}
.tl-bar-fill{background:#000;height:100%}
.tl-flow{margin-top:8px;display:flex;gap:8px;align-items:center}
.tl-flow-down{background:#f7f7f7;padding:6px 10px;flex:1;text-align:center}
.tl-flow-up{background:#000;padding:6px 10px;flex:1;text-align:center;color:#fff}
.tl-alert{background:#f7f7f7;padding:16px;border:1px solid #000}
.cd-item{background:#f7f7f7;padding:16px;margin-bottom:10px;border-left:3px solid #ddd}
.cd-urgent{border-left-color:#000}.cd-warn{border-left-color:#888}.cd-info{border-left-color:#000}
.af-row{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.af-gone{background:#f7f7f7;padding:8px 14px;text-decoration:line-through;color:#bbb;font-size:.82rem;flex:1;text-align:center}
.af-new{background:#000;padding:8px 14px;color:#fff;font-weight:700;font-size:.82rem;flex:1;text-align:center}
.af-up{background:#f7f7f7;padding:8px 14px;color:#000;font-weight:700;font-size:.82rem;flex:1;text-align:center}
.footer{text-align:center;color:#bbb;font-size:.72rem;padding:32px 0 16px}
.back-btn{display:inline-block;background:#000;color:#fff;padding:8px 20px;font-size:.78rem;font-weight:600;text-decoration:none;margin-bottom:16px}
.back-btn:hover{background:#333}
.ch-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:0;border-top:1px solid #e5e5e5}
.ch-card{background:#fff;border:1px solid #e5e5e5;border-top:none;border-right:1px solid #e5e5e5;padding:24px 20px;text-decoration:none;color:inherit;transition:background .15s}
.ch-card:last-child{border-right:none}
.ch-card:hover{background:#fafafa}
.ch-card img{width:100%;height:120px;object-fit:cover;filter:grayscale(100%);margin-bottom:12px}
.today-card{padding:36px 0;border-bottom:1px solid #e5e5e5;display:block;text-decoration:none;color:inherit}
.today-card:hover{opacity:.9}
.today-card img{width:100%;height:240px;object-fit:cover;filter:grayscale(100%);margin-bottom:24px}
@media(max-width:768px){.ch-grid{grid-template-columns:1fr!important}.ch-card{border-right:none!important;border-bottom:1px solid #e5e5e5}}
"""

def page_wrap(title, body):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} — 오늘의 오디언스</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
{body}
</div>
</body>
</html>"""

# === BUILD INDEX ===
today = ESSAYS[0]
essay_map = {e["id"]: e for e in ESSAYS}

cards_html = ""
# Today hero
cards_html += f"""
<div style="padding:48px 0 16px;border-bottom:3px solid #000">
  <p style="font-size:.68rem;font-weight:700;letter-spacing:3px;color:#999;margin-bottom:10px">AUDIENCE IDEA BANK</p>
  <h1 style="font-size:2rem;font-weight:900;color:#000;line-height:1.2;letter-spacing:-1px">오늘의 오디언스</h1>
  <p style="color:#999;font-size:.82rem;line-height:1.6;margin-top:8px">트렌드를 읽고, 행동 시그널을 조합해<br>아직 아무도 안 쓰는 오디언스를 제안합니다.</p>
</div>
<a class="today-card" href="{today['id']}.html">
  <img loading="lazy" src="{today['img']}" alt="">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:20px">
    <span style="font-size:.68rem;font-weight:900;color:#e8530e;background:#000;padding:4px 10px;letter-spacing:2px">TODAY</span>
    <span style="font-size:.68rem;font-weight:700;color:#000;background:#f0f0f0;padding:4px 12px">{today['tag']}</span>
    <span style="font-size:.68rem;color:#999">{today['date']}</span>
  </div>
  <div style="font-size:1.8rem;font-weight:900;color:#000;line-height:1.3;margin-bottom:12px">{today['title']}</div>
  <div style="font-size:.9rem;color:#666;line-height:1.7;margin-bottom:24px">{today['sub']}</div>
  <div style="display:flex;align-items:center;gap:12px">
    <span style="font-size:1.2rem;font-weight:900;color:#000">{today['stat']}</span>
    <span style="font-size:.72rem;color:#999">{today['stat_label']}</span>
    <span style="margin-left:auto;font-size:.8rem;font-weight:600;color:#000">읽기 →</span>
  </div>
</a>
"""

# Chapters
for ch in CHAPTERS:
    ch_essays = [essay_map[eid] for eid in ch["ids"] if eid in essay_map and eid != today["id"]]
    if not ch_essays:
        continue
    cards_html += f"""
<div style="margin-top:48px;margin-bottom:16px;padding-bottom:12px;border-bottom:2px solid #000">
  <span style="font-size:.95rem;font-weight:900;color:#000">{ch['label']}</span>
</div>
<div class="ch-grid">"""
    for e in ch_essays:
        thumb = e["img"].replace("w=800", "w=400")
        cards_html += f"""
  <a class="ch-card" href="{e['id']}.html">
    <img loading="lazy" src="{thumb}" alt="">
    <div style="font-size:.62rem;font-weight:700;color:#999;letter-spacing:1px;margin-bottom:10px">{e['tag'].upper()}</div>
    <div style="font-size:1rem;font-weight:800;color:#000;line-height:1.4;margin-bottom:6px">{e['title']}</div>
    <div style="font-size:.72rem;color:#999;line-height:1.5;margin-bottom:12px">{e['sub'][:50]}...</div>
    <div style="font-size:.95rem;font-weight:900;color:#000">{e['stat']}</div>
  </a>"""
    cards_html += "\n</div>"

cards_html += '\n<div class="footer">오늘의 오디언스 · by IGAWorks · © 2026</div>'

with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(page_wrap("오늘의 오디언스", cards_html))
print("OK: index.html")

# === BUILD DETAIL PAGES ===
for e in ESSAYS:
    essay_file = os.path.join(DIR, "essays_html", f"{e['id']}.html")
    if not os.path.exists(essay_file):
        print(f"SKIP: {e['id']}")
        continue
    with open(essay_file, "r") as ef:
        essay_html = ef.read()
    body = f'<a class="back-btn" href="index.html">← 뒤로</a>\n{essay_html}'
    with open(os.path.join(OUT, f"{e['id']}.html"), "w") as f:
        f.write(page_wrap(e["title"], body))
    print(f"OK: {e['id']}.html")

print(f"\nDONE — {len(os.listdir(OUT))} files in docs/")
