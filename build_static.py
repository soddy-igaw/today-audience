"""정적 사이트 빌드 스크립트 — docs/ 폴더에 생성"""
import os, json

DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DIR, "docs")
os.makedirs(OUT, exist_ok=True)

ESSAYS = [
    {"id":"travel_0423","tag":"여행","title":"해외여행 포기하고 국내앱 깐 사람","sub":"유류할증료 급등으로 국내여행 전환하는 예약 취소자들","stat":"~1.8만","stat_label":"종합여행앱+호텔앱 교차 · DMP 실측","date":"2026.04.26"},
    {"id":"헬스_0425","tag":"헬스","title":"운동앱 2개 깔고 쇼핑앱 여는 사람들","sub":"홈트와 헬스장을 동시에 준비하는 사람들의 구매 패턴","stat":"~89만","stat_label":"운동앱 2개+쇼핑앱 · DMP 실측","date":"2026.04.25"},
    {"id":"coupang_exit","tag":"쇼핑","title":"쿠팡 삭제 후 알리 깐 사람","sub":"236만 이탈자 중 해외직구로 간 진짜 타겟은?","stat":"~5만","stat_label":"쇼핑앱+가격비교앱 교차 · DMP 실측","date":"2026.04.24"},
    {"id":"realestate_0422","tag":"부동산","title":"전세 만기 앞둔 사람이 갑자기 카뱅크를 깐 이유","sub":"전세보증금 돌려받기 불안한 세입자들의 숨은 행동 시그널","stat":"~2만","stat_label":"부동산앱+대출앱 교차 · DMP 실측","date":"2026.04.22"},
    {"id":"game_0422","tag":"게임","title":"스위치2 예약하고 스팀 삭제한 사람","sub":"모바일 게임을 지우고 콘솔로 갈아타는 신호","stat":"~14만","stat_label":"게임앱+가전앱 교차 · DMP 실측","date":"2026.04.22"},
    {"id":"realestate_0421","tag":"부동산","title":"대출 3개 동시 신청하는 전세족","sub":"전세 만기 D-30, 급하게 움직이는 사람들","stat":"~2만","stat_label":"부동산앱+대출앱 교차 · DMP 실측","date":"2026.04.21"},
    {"id":"safehaven_0420","tag":"증권","title":"주식 정리하고 금 사는 사람","sub":"증권앱 삭제 후 3일 내 한국금거래소 설치자가 말하는 것","stat":"~92만","stat_label":"증권앱+은행앱 교차 · DMP 실측","date":"2026.04.20"},
    {"id":"tosspay","tag":"금융","title":"대출 만기 30일 전부터 ETF 앱 깔기 시작한 사람","sub":"빚 줄이기보다 투자로 갚겠다는 사람들","stat":"~7만","stat_label":"대출앱+은행앱 교차 · DMP 실측","date":"2026.04.20"},
    {"id":"realestate","tag":"부동산","title":"전세 만기 D-30에 매매앱 깐 사람","sub":"전세 끝나기 한 달 전, 직방에서 호갱노노로 넘어간 사람들","stat":"~2만","stat_label":"부동산앱+대출앱 교차 · DMP 실측","date":"2026.04.15"},
    {"id":"car","tag":"자동차","title":"전기차 포기하고 하이브리드 찾는 사람","sub":"충전소 앱 삭제 후 하이브리드 매물 검색으로 돌아서는 타겟","stat":"~6만","stat_label":"자동차브랜드앱+중고차앱 교차 · DMP 실측","date":"2026.04.14"},
    {"id":"pet","tag":"반려동물","title":"사료 갈아탄 후 펫닥 3번째 상담 중인 사람","sub":"새 사료 바꾼 후 5일 내 수의사 온라인 상담 앱을 여는 반려인","stat":"~3만","stat_label":"애완동물앱+쇼핑앱 교차 · DMP 실측","date":"2026.04.13"},
    {"id":"golf","tag":"골프","title":"접대 때문에 골프 시작한 입문자","sub":"접대 골프 입문자는 고민하지 않습니다. 빠르게 삽니다.","stat":"~8만","stat_label":"골프앱+비즈니스앱 교차 · DMP 실측","date":"2026.04.11"},
]

CHAPTERS = [
    {"label":"금융","ids":["tosspay","realestate","realestate_0421","realestate_0422","safehaven_0420"]},
    {"label":"여행","ids":["travel_0423"]},
    {"label":"스포츠","ids":["헬스_0425","golf"]},
    {"label":"라이프","ids":["car","pet"]},
    {"label":"게임","ids":["game_0422"]},
    {"label":"쇼핑","ids":["coupang_exit"]},
]

CSS = open(os.path.join(DIR, "essays_html", "realestate.html")).read()[:0]  # just init
# Read CSS from a shared string
CSS = """
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:'Pretendard',sans-serif;-webkit-font-smoothing:antialiased;color:#1a1a1a}
.wrap{max-width:800px;margin:0 auto;padding:0 24px 100px}
.hero-img{width:calc(100% + 48px);margin:0 -24px;height:320px;object-fit:cover;display:none}
.detail-wrap{max-width:800px;margin:0 auto}
.detail-hero,.hero{padding:40px 0 32px}
.detail-tag,.hero .tag{font-size:.72rem;font-weight:600;color:#e8530e;letter-spacing:1px;margin-bottom:16px;display:block}
.detail-emoji{display:none}
.detail-title,.hero h1{font-size:1.8rem;font-weight:900;color:#000;line-height:1.4;letter-spacing:-0.5px}
.detail-sub{display:none}
.detail-meta,.hero .meta{font-size:.78rem;color:#bbb;margin-top:16px}
.body p,.section p,.quote-box p{font-size:1.1rem;color:#333;line-height:2;margin-bottom:16px;letter-spacing:-0.2px}
.body strong,.section strong,.quote-box strong{color:#000;font-weight:800}
.section{padding:24px 0;border-bottom:none}
.section-label{font-size:1.2rem;font-weight:800;color:#000;line-height:1.5;margin:32px 0 12px;letter-spacing:-0.3px}
.quote-box{padding:32px 0;border-top:1px solid #f0f0f0;border-bottom:1px solid #f0f0f0;margin:24px 0;background:none;border-left:none}
.quote-box p{font-style:italic}
.quote-box strong{font-style:normal}
.behavior-cards{display:flex;flex-direction:column;gap:16px;margin-top:20px}
.behavior-card{background:#fafafa;padding:28px;position:relative;overflow:hidden}
.behavior-card.highlight{background:#000}
.behavior-card.highlight .bc-desc{color:#999}
.bc-step{font-size:.62rem;font-weight:700;color:#bbb;letter-spacing:2px;margin-bottom:10px}
.behavior-card.highlight .bc-step{color:#666}
.bc-title{font-size:1.05rem;font-weight:800;color:#000;line-height:1.35;margin-bottom:6px}
.behavior-card.highlight .bc-title{color:#fff}
.bc-desc{font-size:.88rem;color:#777;line-height:1.6}
.bc-num{font-size:2.5rem;font-weight:900;color:#000;opacity:0.06;position:absolute;right:24px;top:50%;transform:translateY(-50%)}
.behavior-card.highlight .bc-num{color:#e8530e;opacity:1;font-size:1.6rem;position:static;transform:none;margin-top:16px}
.insight-box{background:#000;padding:40px 32px;margin:32px -24px}
.insight-box .ins-label{display:none}
.insight-box p{color:#fff;font-size:1.1rem;line-height:2;font-weight:500;margin:0}
.insight-box strong{color:#e8530e;font-weight:700}
.audience-card{background:#000;padding:48px 32px;margin:48px -24px}
.ind-grid,.ind-card{display:none}
.footer{text-align:center;color:#ccc;font-size:.72rem;padding:48px 0 16px}
.back-btn{display:inline-block;background:#000;color:#fff;padding:8px 20px;font-size:.78rem;font-weight:600;text-decoration:none;margin-bottom:16px}
.back-btn:hover{background:#333}
.ch-grid{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding-bottom:8px}
.ch-grid::-webkit-scrollbar{height:3px}
.ch-grid::-webkit-scrollbar-thumb{background:#eee;border-radius:2px}
.ch-card{min-width:200px;max-width:240px;flex-shrink:0;scroll-snap-align:start;text-decoration:none;color:inherit;display:block}
.ch-card:hover .ch-title{color:#e8530e}
.ch-card img{width:100%;height:110px;object-fit:cover;filter:grayscale(100%);margin-bottom:12px}
.ch-card .ch-tag{font-size:.6rem;font-weight:700;color:#e8530e;letter-spacing:0.5px;margin-bottom:8px}
.ch-card .ch-title{font-size:.9rem;font-weight:800;color:#000;line-height:1.4;margin-bottom:6px;transition:color .15s}
.ch-card .ch-stat{font-size:.85rem;font-weight:900;color:#000}
@media(max-width:768px){.ch-card{min-width:180px;max-width:220px}}
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

# SVG 일러스트 생성 — 카테고리별 미니멀 데이터 비주얼
TAG_ICONS = {
    "금융": ("💰", ["앱A 사용량", "앱B 전환", "시그널 포착"]),
    "부동산": ("🏠", ["매물 조회", "대출 비교", "계약 직전"]),
    "쇼핑": ("🛒", ["기존앱 이탈", "비교 탐색", "신규앱 설치"]),
    "배달": ("🛵", ["주문 감소", "비교 시작", "앱 전환"]),
    "골프": ("⛳", ["앱 설치", "예약 증가", "장비 구매"]),
    "교육": ("📚", ["강의앱 설치", "학습 패턴", "결제 전환"]),
    "반려동물": ("🐾", ["펫앱 설치", "병원 예약", "쇼핑 시작"]),
    "패션": ("👗", ["브랜드 탐색", "가격 비교", "구매 전환"]),
    "헬스": ("💪", ["운동앱 설치", "루틴 형성", "장비 구매"]),
    "여행": ("✈️", ["검색 시작", "비교 탐색", "예약 직전"]),
    "증권": ("📈", ["매도 시그널", "자산 이동", "신규 설치"]),
    "게임": ("🎮", ["커뮤니티 급증", "스펙 비교", "구매 직전"]),
    "테마주": ("📈", ["뉴스 반응", "앱 실행 급증", "추격 매수"]),
    "자동차": ("🚗", ["비교 시작", "시승 예약", "견적 조회"]),
    "러닝": ("🏃", ["앱 설치", "루틴 형성", "장비 구매"]),
    "건강": ("💪", ["운동앱 설치", "루틴 형성", "장비 구매"]),
}

def make_hero_svg(tag):
    """카테고리별 미니멀 시그널 플로우 SVG"""
    icon, steps = TAG_ICONS.get(tag, ("📊", ["시그널 A", "시그널 B", "전환 포착"]))
    return f'''<div style="background:#f8f8f8;margin:0 -24px;padding:48px 32px;text-align:center">
  <svg viewBox="0 0 400 120" style="max-width:400px;width:100%;height:auto" xmlns="http://www.w3.org/2000/svg">
    <line x1="60" y1="60" x2="340" y2="60" stroke="#e0e0e0" stroke-width="2" stroke-dasharray="6,4"/>
    <circle cx="80" cy="60" r="24" fill="#fff" stroke="#e0e0e0" stroke-width="2"/>
    <text x="80" y="66" text-anchor="middle" font-size="11" font-weight="700" fill="#bbb">D-14</text>
    <text x="80" y="100" text-anchor="middle" font-size="9" fill="#999" font-family="Pretendard,sans-serif">{steps[0]}</text>
    <circle cx="200" cy="60" r="24" fill="#fff" stroke="#e0e0e0" stroke-width="2"/>
    <text x="200" y="66" text-anchor="middle" font-size="11" font-weight="700" fill="#bbb">D-7</text>
    <text x="200" y="100" text-anchor="middle" font-size="9" fill="#999" font-family="Pretendard,sans-serif">{steps[1]}</text>
    <circle cx="320" cy="60" r="24" fill="#e8530e" stroke="none"/>
    <text x="320" y="66" text-anchor="middle" font-size="11" font-weight="800" fill="#fff">NOW</text>
    <text x="320" y="100" text-anchor="middle" font-size="9" fill="#e8530e" font-weight="700" font-family="Pretendard,sans-serif">{steps[2]}</text>
    <polygon points="145,56 155,60 145,64" fill="#e0e0e0"/>
    <polygon points="265,56 275,60 265,64" fill="#e8530e"/>
  </svg>
</div>'''

# === BUILD INDEX ===
today = ESSAYS[0]
essay_map = {e["id"]: e for e in ESSAYS}

CAT_TITLES = {
    "금융": ("", "돈이 움직이는 시그널"),
    "여행": ("", "여행 계획이 바뀌는 순간"),
    "스포츠": ("", "운동 습관이 바뀌는 사람"),
    "라이프": ("", "생활이 전환되는 타이밍"),
    "게임": ("", "플랫폼을 갈아타는 게이머"),
    "쇼핑": ("", "장바구니가 이동하는 신호"),
}

INDEX_CSS = """
<style>
body{background:#f7f7fa !important}
.wrap{max-width:960px !important;margin:0 auto !important}
.header{padding:48px 0 24px}
.header .label{font-size:.65rem;font-weight:700;letter-spacing:3px;color:#e8530e;margin-bottom:10px}
.header h1{font-size:2rem;font-weight:900;color:#111;letter-spacing:-.5px;margin-bottom:10px}
.header p{font-size:.92rem;color:#999;line-height:1.7}
.essay-grid{display:grid;grid-template-columns:1fr;gap:10px}
@media(min-width:640px){.essay-grid{grid-template-columns:1fr 1fr}}
.today-card{background:#111;border-radius:20px;padding:32px 24px;margin-bottom:32px;text-decoration:none;display:block;color:inherit}
.today-card:hover{background:#1a1a1a}
.today-card .badge{display:inline-flex;align-items:center;gap:6px;margin-bottom:20px}
.today-card .badge span:first-child{font-size:.6rem;font-weight:900;color:#e8530e;letter-spacing:2px}
.today-card .badge span:last-child{font-size:.6rem;font-weight:600;color:#555}
.today-card h2{font-size:1.4rem;font-weight:900;color:#fff;line-height:1.35;margin-bottom:10px}
.today-card .sub{font-size:.85rem;color:#666;line-height:1.6;margin-bottom:20px}
.today-card .bottom{display:flex;align-items:center;gap:10px}
.today-card .stat{font-size:1.1rem;font-weight:900;color:#e8530e}
.today-card .signal{font-size:.65rem;color:#555}
.today-card .arrow{margin-left:auto;font-size:.75rem;font-weight:600;color:#e8530e}
.cat-section{margin-bottom:32px}
.cat-header{display:flex;align-items:baseline;gap:10px;padding:24px 0 14px}
.cat-name{font-size:1.1rem;font-weight:900;color:#111}
.cat-count{font-size:.65rem;color:#bbb;margin-left:auto}
.essay-card{background:#fff;border-radius:16px;padding:20px;margin-bottom:10px;text-decoration:none;display:block;color:inherit;transition:all .15s}
.essay-card:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,.06)}
.essay-card .etag{font-size:.6rem;font-weight:600;color:#e8530e;margin-bottom:8px}
.essay-card h3{font-size:.95rem;font-weight:800;color:#111;line-height:1.4;margin-bottom:6px}
.essay-card .esub{font-size:.78rem;color:#999;line-height:1.5;margin-bottom:12px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.essay-card .meta{display:flex;align-items:center;gap:8px}
.essay-card .stat{font-size:.88rem;font-weight:900;color:#111}
.essay-card .signal{font-size:.6rem;color:#bbb}
.essay-card .date{font-size:.6rem;color:#ccc;margin-left:auto}
.sub-section{background:#111;border-radius:20px;padding:32px 24px;text-align:center;margin-top:40px}
.sub-section .emoji{font-size:1.8rem;margin-bottom:12px}
.sub-section h3{font-size:1rem;font-weight:800;color:#fff;margin-bottom:6px}
.sub-section p{font-size:.78rem;color:#666;line-height:1.6;margin-bottom:20px}
.sub-section input{width:100%;padding:12px 14px;border:1px solid #333;border-radius:10px;background:#1a1a1a;color:#fff;font-size:.85rem;outline:none;margin-bottom:8px;box-sizing:border-box}
.sub-section input::placeholder{color:#555}
.sub-section button{width:100%;padding:12px;background:#e8530e;color:#fff;border:none;border-radius:10px;font-size:.85rem;font-weight:700;cursor:pointer}
.sub-section button:hover{background:#d14a0c}
.sub-msg{font-size:.68rem;color:#555;margin-top:8px;min-height:14px}
</style>
"""

cards_html = INDEX_CSS

# Header
cards_html += """
<div class="header">
  <div class="label">AUDIENCE IDEA BANK</div>
  <h1>오늘의 오디언스</h1>
  <p>매일 트렌드를 읽고, DMP 행동 데이터를 교차 분석해<br><strong style="color:#111">광고주가 바로 쓸 수 있는 오디언스</strong>를 제안합니다.</p>
</div>
"""

# TODAY card
cards_html += f"""
<a class="today-card" href="{today['id']}.html">
  <div class="badge"><span>TODAY</span><span>{today['tag']} · {today['date']}</span></div>
  <h2>{today['title']}</h2>
  <div class="sub">{today['sub']}</div>
  <div class="bottom">
    <span class="stat">{today['stat']}</span>
    <span class="signal">{today['stat_label']}</span>
    <span class="arrow">읽기 →</span>
  </div>
</a>
"""

# Category sections
for ch in CHAPTERS:
    ch_essays = [essay_map[eid] for eid in ch["ids"] if eid in essay_map and eid != today["id"]]
    if not ch_essays:
        continue
    emoji, cat_title = CAT_TITLES.get(ch["label"], ("📊", ch["label"]))
    cards_html += f"""
<div class="cat-section">
  <div class="cat-header">
    <span class="cat-name">{cat_title}</span>
    <span class="cat-count" style="background:#eee;padding:2px 8px;border-radius:4px;font-weight:700;color:#999">{len(ch_essays)}</span>
  </div>
  <div class="essay-grid">"""
    for e in ch_essays:
        date_short = e["date"].replace("2026.", "")
        cards_html += f"""
  <a class="essay-card" href="{e['id']}.html">
    <div class="etag">{e['tag']}</div>
    <h3>{e['title']}</h3>
    <div class="esub">{e['sub']}</div>
    <div class="meta">
      <span class="stat">{e['stat']}</span>
      <span class="signal">{e['stat_label']}</span>
      <span class="date">{date_short}</span>
    </div>
  </a>"""
    cards_html += "\n  </div>\n</div>"

# Subscribe section (inline)
cards_html += """
<div class="sub-section">
  <div class="emoji">🎯</div>
  <h3>매일 새로운 오디언스를 받아보세요</h3>
  <p>매일 아침, 광고주가 바로 쓸 수 있는<br>새로운 오디언스를 이메일로 보내드립니다.</p>
  <form id="sf" onsubmit="return handleSub(event)">
    <input type="email" id="se" placeholder="이메일 주소" required>
    <button type="submit" id="sb">구독하기</button>
  </form>
  <div class="sub-msg" id="sm"></div>
</div>
<script>
var SU='https://script.google.com/macros/s/AKfycbxqiD464kHQ0YMiy724hZvgP359D1kATb5cxJ8qtN7Z6Vylx2GI-vzlMbPt5f-PZPnKNQ/exec';
function handleSub(e){
  e.preventDefault();
  var em=document.getElementById('se').value,btn=document.getElementById('sb');
  btn.disabled=true;btn.textContent='...';
  fetch(SU,{method:'POST',mode:'no-cors',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:em})})
  .then(function(){document.getElementById('sm').textContent='구독 완료! 감사합니다 🎉';document.getElementById('sf').reset()})
  .catch(function(){document.getElementById('sm').textContent='오류가 발생했습니다.'})
  .finally(function(){btn.disabled=false;btn.textContent='구독하기'});
  return false
}
</script>
"""

cards_html += '\n<div class="footer" style="text-align:center;color:#ccc;font-size:.65rem;padding:32px 0 16px;line-height:1.8">본 리포트는 IGAWorks의 DMP 행동 데이터를 시장 트렌드에 맞춰<br>자동 생성한 오디언스 분석입니다.<br>데이터 기준: 모바일인덱스 실측 · © 2026 IGAWorks<br>made by soddy</div>'

with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(page_wrap("오늘의 오디언스", cards_html))
print("OK: index.html")

# === BUILD DETAIL PAGES ===
essay_chapter = {}
for ch in CHAPTERS:
    for eid in ch["ids"]:
        essay_chapter[eid] = ch["label"]

for e in ESSAYS:
    essay_file = os.path.join(DIR, "essays_html", f"{e['id']}.html")
    if not os.path.exists(essay_file):
        print(f"SKIP: {e['id']}")
        continue
    with open(essay_file, "r") as ef:
        essay_html = ef.read()

    ch_label = essay_chapter.get(e["id"], "")
    related = []
    if ch_label:
        for ch in CHAPTERS:
            if ch["label"] == ch_label:
                related = [essay_map[eid] for eid in ch["ids"] if eid in essay_map and eid != e["id"]]
                break

    related_html = ""
    if related:
        related_html = f"""
<div style="margin-top:48px;padding-top:32px;border-top:1px solid #eee">
  <div style="font-size:.82rem;font-weight:800;color:#000;margin-bottom:16px">같은 주제의 오디언스</div>
  <div style="display:flex;gap:14px;overflow-x:auto;padding-bottom:8px;-webkit-overflow-scrolling:touch">"""
        for r in related[:5]:
            related_html += f"""
    <a href="{r['id']}.html" style="min-width:180px;max-width:200px;flex-shrink:0;text-decoration:none;color:inherit;border:1px solid #eee;padding:12px">
      <div style="font-size:.65rem;font-weight:700;color:#e8530e;margin-bottom:6px">{r['tag']}</div>
      <div style="font-size:.82rem;font-weight:800;color:#000;line-height:1.3;margin-bottom:4px">{r['title']}</div>
      <div style="font-size:.68rem;color:#999">{r['stat']}</div>
    </a>"""
        related_html += "\n  </div>\n</div>"

    img_url = e.get("img", "")
    hero_img = ""
    current_idx = next((i for i, x in enumerate(ESSAYS) if x["id"] == e["id"]), -1)
    next_essay = ESSAYS[current_idx + 1] if current_idx >= 0 and current_idx + 1 < len(ESSAYS) else ESSAYS[0]
    # Contact CTA block — 밝은 톤, 같은 주제 아래 배치
    contact_html = """
<div style="background:#f7f7fa;border-radius:16px;padding:32px 28px;margin:24px 0;text-align:center">
  <div style="font-size:.82rem;font-weight:700;color:#111;margin-bottom:6px">이 오디언스를 캠페인에 쓰고 싶다면</div>
  <div style="font-size:.75rem;color:#999;line-height:1.6;margin-bottom:20px">ADID 세그먼트 추출 · DSP 연동 · 커스텀 오디언스 설계</div>
  <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
    <a href="mailto:audiencelab@igaworks.com" style="background:#111;color:#fff;padding:10px 22px;border-radius:8px;font-size:.78rem;font-weight:700;text-decoration:none">이메일 문의</a>
    <a href="https://mobileindex.com" style="background:#fff;color:#111;padding:10px 22px;border-radius:8px;font-size:.78rem;font-weight:700;text-decoration:none;border:1px solid #ddd">모바일인덱스 →</a>
  </div>
</div>
"""

    next_html = f"""
<div style="padding:24px 0;border-top:1px solid #f0f0f0;text-align:center">
<div style="font-size:.68rem;color:#999;margin-bottom:6px">다음 오디언스</div>
<a href="{next_essay['id']}.html" style="font-size:.95rem;font-weight:800;color:#000;text-decoration:none">{next_essay['title']}</a>
</div>"""

    # Detect toss-style essays (contain their own <style> block)
    is_toss_style = '<style>' in essay_html

    # Replace existing cta-bar with contact block
    if '<div class="cta-bar">' in essay_html:
        import re as _re
        essay_html = _re.sub(r'<div class="cta-bar">.*?</div>', '', essay_html, flags=_re.DOTALL)

    if is_toss_style:
        body = f'{hero_img}{essay_html}\n{contact_html}'
    else:
        body = f'<a class="back-btn" href="index.html">← 뒤로</a>\n{hero_img}{essay_html}\n{contact_html}'
    with open(os.path.join(OUT, f"{e['id']}.html"), "w") as f:
        f.write(page_wrap(e["title"], body))
    print(f"OK: {e['id']}.html")

print(f"\nDONE — {len(os.listdir(OUT))} files in docs/")
