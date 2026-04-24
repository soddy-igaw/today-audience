"""정적 사이트 빌드 스크립트 — docs/ 폴더에 생성"""
import os, json

DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DIR, "docs")
os.makedirs(OUT, exist_ok=True)

ESSAYS = [
    {"id":"travel_0423","tag":"여행","title":"유류할증료 보고 해외여행 취소한 사람","sub":"해외에서 국내로 방향을 바꾼 사람","stat":"~185만","stat_label":"해외앱 감소 + 국내 숙박앱 증가","date":"2026.04.23","img":"https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&h=400&fit=crop&q=80"},
    {"id":"shopping_0423","tag":"쇼핑","title":"하루 더 기다리고 반값에 사는 사람","sub":"구매 채널을 바꾸는 사람","stat":"~67만","stat_label":"쿠팡 감소 + C-커머스 신규","date":"2026.04.23","img":"https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&h=400&fit=crop&q=80"},
    {"id":"realestate_0422","tag":"부동산","title":"5월 9일 전에 팔아야 하는 다주택자","sub":"양도세 중과 유예 만료 D-17","stat":"~43만","stat_label":"부동산앱 매도 전환 + 세무앱 동시 활성","date":"2026.04.22","img":"https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=400&fit=crop&q=80"},
    {"id":"realestate_0421","tag":"부동산","title":"전세 포기하고 10억 이하 매매로 선회한 사람","sub":"전세난에 10억 이하 매매로 전환하는 사람","stat":"~43만","stat_label":"부동산앱 전세→매매 전환 유저","date":"2026.04.21","img":"https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=400&fit=crop&q=80"},
    {"id":"safehaven_0420","tag":"증권","title":"전쟁 뉴스에 증시를 떠나 안전자산으로 이동하는 사람","sub":"KOSPI 폭락 후 주식을 전부 정리하고 금·달러로 갈아탄 사람","stat":"~93만","stat_label":"증권앱 이탈+안전자산앱 동시 활성","date":"2026.04.20","img":"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop&q=80"},
    {"id":"금융_0420","tag":"금융","title":"고정금리 만료 앞두고 갈아타기 준비하는 사람","sub":"2~3년 전 고정금리 대출자들이 만료 시점에서 갈아타기를 검토 중. 금융·핀테크 광고주의 골든타임.","stat":"","stat_label":"금융 오디언스 (DMP)","date":"2026.04.20","img":"https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop&q=80"},
    {"id":"realestate","tag":"부동산","title":"전세→매매 전환 중, 차 담보로 부족분을 메우는 사람","sub":"주담대 한도가 부족할 때, 자동차가 두 번째 담보가 됩니다","stat":"~43만","stat_label":"부동산+대출앱 동시 사용자 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=400&fit=crop&q=80"},
    {"id":"wegovy","tag":"헬스","title":"다이어트약 처방 후 운동을 끊은 사람","sub":"GLP-1 다이어트약 처방이 폭발하면서, 운동으로 빼는 사람과 약으로 빼는 사람이 갈리고 있습니다","stat":"~110만","stat_label":"병원예약+약국앱 동시 활성 (DMP)","date":"2026.04.16","img":"https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800https://images.unsplash.com/photo-1505576399279-0d754c0ce141?w=800&h=400&fit=crop&q=80h=400https://images.unsplash.com/photo-1505576399279-0d754c0ce141?w=800&h=400&fit=crop&q=80fit=crophttps://images.unsplash.com/photo-1505576399279-0d754c0ce141?w=800&h=400&fit=crop&q=80q=80"},
    {"id":"car","tag":"자동차","title":"전기차에서 하이브리드로 선택지를 바꾼 사람","sub":"보조금 축소 뉴스 보고 전기차를 포기한 게 아니라, 선택지를 바꾼 겁니다","stat":"~75만","stat_label":"자동차앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&h=400&fit=crop&q=80"},
    {"id":"game_0422","tag":"게임","title":"GTA6 출시일 확정 후 게이밍 PC를 사전예약하는 사람","sub":"게임 하나 때문에 200만원 쓰는 사람","stat":"~15만","stat_label":"게임앱+쇼핑앱 동시 활성","date":"2026.04.22","img":"https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=800&h=400&fit=crop&q=80"},
    {"id":"game","tag":"게임","title":"신작 발표 후 게이밍 하드웨어 구매 직전인 사람","sub":"신작 출시 전 게임 커뮤니티 접속이 3배 뛰면, 하드웨어 지갑이 열립니다","stat":"~15만","stat_label":"게임앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=800&h=400&fit=crop&q=80"},
    {"id":"stock","tag":"증권","title":"미국주식에서 금으로 갈아타는 사람","sub":"트럼프 관세에 미장을 판 서학개미, 금으로 갈아탔습니다","stat":"~93만","stat_label":"증권앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop&q=80"},
    {"id":"ktx","tag":"여행","title":"KTX 매진 후 대안 교통을 찾는 사람","sub":"외국인 관광객이 KR Pass로 좌석을 쓸어가면, 내국인은 대안 교통을 찾기 시작합니다","stat":"~121만","stat_label":"코레일+교통앱 동시 활성 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800&h=400&fit=crop&q=80"},
    {"id":"travel","tag":"여행","title":"해외여행 대신 국내여행으로 전환한 사람","sub":"환율 1,450원 시대, 여행을 포기한 게 아니라 방향을 바꾼 겁니다","stat":"~185만","stat_label":"여행앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&h=400&fit=crop&q=80"},
    {"id":"pet","tag":"반려동물","title":"반려동물 첫 입양 후 2주 이내 사람","sub":"2주 안에 펫앱 3개를 동시에 까는 사람은 3년 고객이 됩니다","stat":"~11만","stat_label":"펫앱+커머스 (DMP)","date":"2026.04.13","img":"https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800&h=400&fit=crop&q=80"},
    {"id":"themestock","tag":"테마주","title":"테마주 뉴스에 반응해 추격 매수하는 사람","sub":"광통신 600% 폭등 뉴스에 증권앱 검색이 터진 사람","stat":"~81만","stat_label":"뉴스+증권앱 동시 활성 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop&q=80"},
    {"id":"carinsurance","tag":"금융","title":"자동차보험 만기 전 갈아타기 비교 중인 사람","sub":"작년보다 15만원 올랐다면, 지금 갈아타세요","stat":"~9만","stat_label":"보험사+비교앱 동시 활성 (DMP)","date":"2026.04.16","img":"https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&h=400&fit=crop&q=80"},
    {"id":"tosspay","tag":"금융","title":"기존 간편결제 사용이 줄고 새 결제앱을 깐 사람","sub":"간편결제 갈아타기가 시작됐습니다","stat":"~98만","stat_label":"간편결제앱 전환 행동 유저","date":"2026.04.20","img":"https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&h=400&fit=crop&q=80"},
    {"id":"finance","tag":"금융","title":"대출 만기 전 대환을 준비하는 사람","sub":"새벽 2시에 대출앱 3개를 번갈아 여는 사람","stat":"~8만","stat_label":"대출탐색 유저 (DMP)","date":"2026.04.10","img":"https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop&q=80"},
    {"id":"running","tag":"러닝","title":"매주 뛰면서 러닝 장비에 돈 쓰는 사람","sub":"커머스에서 15만원짜리 러닝화를 반복 조회하면서, 주말 아침 한강에 나타나는 사람","stat":"~27만","stat_label":"러닝앱+커머스 동시 활성 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800&h=400&fit=crop&q=80"},
    {"id":"golf","tag":"골프","title":"접대 때문에 골프 시작한 입문자","sub":"접대 골프 입문자는 고민하지 않습니다. 빠르게 삽니다.","stat":"~8만","stat_label":"골프앱 사용자 (DMP)","date":"2026.04.11","img":"https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800&h=400&fit=crop&q=80"},
    {"id":"health","tag":"건강","title":"운동 시작 후 2주째 지속 중인 사람","sub":"다이어트를 결심한 게 아니라, 몸이 바뀌기 시작한 겁니다","stat":"~25만","stat_label":"운동앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=400&fit=crop&q=80"},
]

CHAPTERS = [
    {"label":"금융","ids":["finance","tosspay","stock","realestate","realestate_0421","realestate_0422","themestock","carinsurance","safehaven_0420","금융_0420"]},
    {"label":"여행","ids":["travel","ktx","travel_0423"]},
    {"label":"스포츠","ids":["running","golf","health","wegovy"]},
    {"label":"라이프","ids":["car","pet"]},
    {"label":"게임","ids":["game","game_0422"]},
]

CSS = open(os.path.join(DIR, "essays_html", "realestate.html")).read()[:0]  # just init
# Read CSS from a shared string
CSS = """
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff;font-family:'Pretendard',sans-serif;-webkit-font-smoothing:antialiased;color:#1a1a1a}
.wrap{max-width:640px;margin:0 auto;padding:0 24px 100px}
.hero-img{width:calc(100% + 48px);margin:0 -24px;height:320px;object-fit:cover;filter:grayscale(100%)}
.detail-wrap{max-width:640px;margin:0 auto}
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

# === BUILD INDEX ===
today = ESSAYS[0]
essay_map = {e["id"]: e for e in ESSAYS}

cards_html = ""
# Header
cards_html += """
<div style="padding:48px 0 40px">
  <div style="font-size:.72rem;font-weight:700;letter-spacing:3px;color:#e8530e;margin-bottom:12px">AUDIENCE IDEA BANK</div>
  <h1 style="font-size:1.6rem;font-weight:900;color:#000;letter-spacing:-0.5px;margin-bottom:12px">오늘의 오디언스</h1>
  <div style="font-size:.92rem;color:#666;line-height:1.7;margin-bottom:20px">매일 트렌드를 읽고, DMP 행동 데이터를 교차 분석해<br><strong style="color:#000">광고주가 바로 쓸 수 있는 오디언스</strong>를 제안합니다.</div>
  <div style="font-size:.75rem;color:#999;margin-top:4px">매일 아침, 새로운 오디언스가 업데이트됩니다.</div>
</div>
"""
# Today hero (검정 배경)
cards_html += f"""
<div style="background:#000;padding:48px 32px;margin:0 -24px">
  <a href="{today['id']}.html" style="text-decoration:none;color:inherit;display:block">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:28px">
      <span style="font-size:.72rem;font-weight:900;color:#e8530e;letter-spacing:2px">TODAY</span>
      <span style="font-size:.65rem;font-weight:600;color:#666">{today['tag']} · {today['date']}</span>
    </div>
    <div style="font-size:1.8rem;font-weight:900;color:#fff;line-height:1.35;letter-spacing:-0.5px;margin-bottom:16px">{today['title']}</div>
    <div style="font-size:1rem;color:#888;line-height:1.7;margin-bottom:32px">{today['sub']}</div>
    <div style="display:flex;align-items:center;gap:12px">
      <span style="font-size:1.3rem;font-weight:900;color:#e8530e">{today['stat']}</span>
      <span style="font-size:.72rem;color:#666">{today['stat_label']}</span>
      <span style="margin-left:auto;font-size:.78rem;font-weight:600;color:#e8530e">읽기 →</span>
    </div>
  </a>
</div>
"""

# Chapters
for ch in CHAPTERS:
    ch_essays = [essay_map[eid] for eid in ch["ids"] if eid in essay_map and eid != today["id"]]
    if not ch_essays:
        continue
    cards_html += f"""
<div style="margin-top:48px;margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid #eee">
  <span style="font-size:.85rem;font-weight:900;color:#000">{ch['label']}</span>
</div>
<div class="ch-grid">"""
    for e in ch_essays:
        thumb = e["img"].replace("w=800", "w=400")
        cards_html += f"""
  <a class="ch-card" href="{e['id']}.html">
    <img loading="lazy" src="{thumb}" alt="">
    <div class="ch-tag">{e['tag']}</div>
    <div class="ch-title">{e['title']}</div>
    <div class="ch-stat">{e['stat']}</div>
  </a>"""
    cards_html += "\n</div>"

cards_html += '\n<div class="footer">오늘의 오디언스 · by IGAWorks · © 2026</div>'

with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(page_wrap("오늘의 오디언스", cards_html))
print("OK: index.html")

# === BUILD DETAIL PAGES ===
# Build chapter lookup: essay_id -> chapter label
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

    # Build related essays (same chapter, exclude self)
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
            thumb = r["img"].replace("w=800", "w=300") if r.get("img") else ""
            img_tag = f'<img loading="lazy" src="{thumb}" style="width:100%;height:80px;object-fit:cover;filter:grayscale(100%);margin-bottom:8px">' if thumb else ""
            related_html += f"""
    <a href="{r['id']}.html" style="min-width:180px;max-width:200px;flex-shrink:0;text-decoration:none;color:inherit;border:1px solid #eee;padding:12px">
      {img_tag}
      <div style="font-size:.65rem;font-weight:700;color:#e8530e;margin-bottom:6px">{r['tag']}</div>
      <div style="font-size:.82rem;font-weight:800;color:#000;line-height:1.3;margin-bottom:4px">{r['title']}</div>
      <div style="font-size:.68rem;color:#999">{r['stat']}</div>
    </a>"""
        related_html += "\n  </div>\n</div>"

    # Add hero image before essay content
    img_url = e.get("img", "")
    hero_img = f'<img class="hero-img" loading="lazy" src="{img_url}" alt="">\n' if img_url else ""
    # Next audience preview
    current_idx = next((i for i, x in enumerate(ESSAYS) if x["id"] == e["id"]), -1)
    next_essay = ESSAYS[current_idx + 1] if current_idx >= 0 and current_idx + 1 < len(ESSAYS) else ESSAYS[0]
    next_html = f"""
<div style="padding:24px 0;border-top:1px solid #f0f0f0;text-align:center">
<div style="font-size:.68rem;color:#999;margin-bottom:6px">다음 오디언스</div>
<a href="{next_essay['id']}.html" style="font-size:.95rem;font-weight:800;color:#000;text-decoration:none">{next_essay['title']}</a>
</div>"""

    body = f'<a class="back-btn" href="index.html">← 뒤로</a>\n{hero_img}{essay_html}\n{next_html}\n{related_html}'
    with open(os.path.join(OUT, f"{e['id']}.html"), "w") as f:
        f.write(page_wrap(e["title"], body))
    print(f"OK: {e['id']}.html")

print(f"\nDONE — {len(os.listdir(OUT))} files in docs/")
