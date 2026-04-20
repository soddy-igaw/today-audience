"""정적 사이트 빌드 스크립트 — docs/ 폴더에 생성"""
import os, json

DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DIR, "docs")
os.makedirs(OUT, exist_ok=True)

ESSAYS = [
    {"id":"safehaven_0420","tag":"증권","title":"전쟁 뉴스에 증시를 떠나 안전자산으로 이동하는 사람","sub":"KOSPI 폭락 후 주식을 전부 정리하고 금·달러로 갈아탄 사람","stat":"~85만","stat_label":"증권앱 이탈+안전자산앱 동시 활성","date":"2026.04.20","img":"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop&q=80"},
    {"id":"금융_0420","tag":"금융","title":"고정금리 만료 앞두고 갈아타기 준비하는 사람","sub":"2~3년 전 고정금리 대출자들이 만료 시점에서 갈아타기를 검토 중. 금융·핀테크 광고주의 골든타임.","stat":"","stat_label":"금융 오디언스 (DMP)","date":"2026.04.20","img":"https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop&q=80"},
    {"id":"realestate","tag":"부동산","title":"전세→매매 전환 중, 차 담보로 부족분을 메우는 사람","sub":"주담대 한도가 부족할 때, 자동차가 두 번째 담보가 됩니다","stat":"~34만","stat_label":"부동산+대출앱 동시 사용자 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=400&fit=crop&q=80"},
    {"id":"wegovy","tag":"헬스","title":"다이어트약 처방 후 운동을 끊은 사람","sub":"GLP-1 다이어트약 처방이 폭발하면서, 운동으로 빼는 사람과 약으로 빼는 사람이 갈리고 있습니다","stat":"~18만","stat_label":"병원예약+약국앱 동시 활성 (DMP)","date":"2026.04.16","img":"https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800https://images.unsplash.com/photo-1505576399279-0d754c0ce141?w=800&h=400&fit=crop&q=80h=400https://images.unsplash.com/photo-1505576399279-0d754c0ce141?w=800&h=400&fit=crop&q=80fit=crophttps://images.unsplash.com/photo-1505576399279-0d754c0ce141?w=800&h=400&fit=crop&q=80q=80"},
    {"id":"car","tag":"자동차","title":"전기차에서 하이브리드로 선택지를 바꾼 사람","sub":"보조금 축소 뉴스 보고 전기차를 포기한 게 아니라, 선택지를 바꾼 겁니다","stat":"~80만","stat_label":"자동차앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&h=400&fit=crop&q=80"},
    {"id":"game","tag":"게임","title":"신작 발표 후 게이밍 하드웨어 구매 직전인 사람","sub":"신작 출시 전 게임 커뮤니티 접속이 3배 뛰면, 하드웨어 지갑이 열립니다","stat":"~140만","stat_label":"게임앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=800&h=400&fit=crop&q=80"},
    {"id":"stock","tag":"증권","title":"미국주식에서 금으로 갈아타는 사람","sub":"트럼프 관세에 미장을 판 서학개미, 금으로 갈아탔습니다","stat":"~97만","stat_label":"증권앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop&q=80"},
    {"id":"ktx","tag":"여행","title":"KTX 매진 후 대안 교통을 찾는 사람","sub":"외국인 관광객이 KR Pass로 좌석을 쓸어가면, 내국인은 대안 교통을 찾기 시작합니다","stat":"~27만","stat_label":"코레일+교통앱 동시 활성 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800&h=400&fit=crop&q=80"},
    {"id":"travel","tag":"여행","title":"해외여행 대신 국내여행으로 전환한 사람","sub":"환율 1,450원 시대, 여행을 포기한 게 아니라 방향을 바꾼 겁니다","stat":"~65만","stat_label":"여행앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&h=400&fit=crop&q=80"},
    {"id":"pet","tag":"반려동물","title":"반려동물 첫 입양 후 2주 이내 사람","sub":"2주 안에 펫앱 3개를 동시에 까는 사람은 3년 고객이 됩니다","stat":"~13만","stat_label":"펫앱+커머스 (DMP)","date":"2026.04.13","img":"https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800&h=400&fit=crop&q=80"},
    {"id":"themestock","tag":"테마주","title":"테마주 뉴스에 반응해 추격 매수하는 사람","sub":"광통신 600% 폭등 뉴스에 증권앱 검색이 터진 사람","stat":"~52만","stat_label":"뉴스+증권앱 동시 활성 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop&q=80"},
    {"id":"carinsurance","tag":"금융","title":"자동차보험 만기 전 갈아타기 비교 중인 사람","sub":"작년보다 15만원 올랐다면, 지금 갈아타세요","stat":"~41만","stat_label":"보험사+비교앱 동시 활성 (DMP)","date":"2026.04.16","img":"https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&h=400&fit=crop&q=80"},
    {"id":"tosspay","tag":"금융","title":"기존 간편결제 사용이 줄고 새 결제앱을 깐 사람","sub":"간편결제 갈아타기가 시작됐습니다","stat":"~120만","stat_label":"간편결제앱 전환 행동 유저","date":"2026.04.20","img":"https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&h=400&fit=crop&q=80"},
    {"id":"finance","tag":"금융","title":"대출 만기 전 대환을 준비하는 사람","sub":"새벽 2시에 대출앱 3개를 번갈아 여는 사람","stat":"~10만","stat_label":"대출탐색 유저 (DMP)","date":"2026.04.10","img":"https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop&q=80"},
    {"id":"running","tag":"러닝","title":"매주 뛰면서 러닝 장비에 돈 쓰는 사람","sub":"커머스에서 15만원짜리 러닝화를 반복 조회하면서, 주말 아침 한강에 나타나는 사람","stat":"~48만","stat_label":"러닝앱+커머스 동시 활성 (DMP)","date":"2026.04.15","img":"https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800&h=400&fit=crop&q=80"},
    {"id":"golf","tag":"골프","title":"접대 때문에 골프 시작한 입문자","sub":"접대 골프 입문자는 고민하지 않습니다. 빠르게 삽니다.","stat":"~17만","stat_label":"골프앱 사용자 (DMP)","date":"2026.04.11","img":"https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800&h=400&fit=crop&q=80"},
    {"id":"health","tag":"건강","title":"운동 시작 후 2주째 지속 중인 사람","sub":"다이어트를 결심한 게 아니라, 몸이 바뀌기 시작한 겁니다","stat":"~103만","stat_label":"운동앱 사용자 (DMP)","date":"2026.04.14","img":"https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=400&fit=crop&q=80"},
]

CHAPTERS = [
    {"label":"금융","ids":["finance","tosspay","stock","realestate","themestock","carinsurance","safehaven_0420","금융_0420"]},
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
body{background:#fff;font-family:'Pretendard',sans-serif;-webkit-font-smoothing:antialiased;color:#1a1a1a}
.wrap{max-width:900px;margin:0 auto;padding:0 24px 100px}
/* 에세이 상세 */
.detail-wrap{max-width:620px;margin:0 auto}
.detail-hero{padding:60px 0 40px;border-bottom:1px solid #eee}
.detail-tag{font-size:.72rem;font-weight:600;color:#e8530e;letter-spacing:1px;margin-bottom:16px;display:block}
.detail-emoji{display:none}
.detail-title{font-size:1.8rem;font-weight:900;color:#000;line-height:1.35;letter-spacing:-0.5px;margin-bottom:16px}
.detail-sub{font-size:1.05rem;color:#666;line-height:1.7}
.detail-meta{font-size:.78rem;color:#bbb;margin-top:20px}
/* 인터뷰 */
.quote-box{padding:48px 0;border-bottom:1px solid #f0f0f0;background:none;border-left:none;margin:0}
.quote-box p{font-size:1.15rem;color:#333;line-height:2;font-style:italic;letter-spacing:-0.2px;margin:0}
.quote-box strong{color:#000;font-style:normal;font-weight:800}
/* 섹션 */
.section{padding:48px 0;border-bottom:1px solid #f0f0f0}
.section-label{font-size:1.15rem;font-weight:900;color:#e8530e;margin-bottom:24px;letter-spacing:-0.3px}
.section p{color:#444;font-size:1.02rem;line-height:2;margin-bottom:20px;letter-spacing:-0.1px}
.section strong{color:#000}
/* STEP 카드 */
.behavior-cards{display:flex;flex-direction:column;gap:20px}
.behavior-card{background:#fafafa;padding:28px;position:relative;overflow:hidden}
.behavior-card.highlight{background:#000}
.behavior-card.highlight .bc-desc{color:#999}
.bc-step{font-size:.65rem;font-weight:700;color:#bbb;letter-spacing:2px;margin-bottom:12px}
.behavior-card.highlight .bc-step{color:#666}
.bc-title{font-size:1.1rem;font-weight:900;color:#000;line-height:1.35;margin-bottom:8px}
.behavior-card.highlight .bc-title{color:#fff}
.bc-desc{font-size:.88rem;color:#777;line-height:1.6}
.bc-num{font-size:2.5rem;font-weight:900;color:#000;opacity:0.06;position:absolute;right:24px;top:50%;transform:translateY(-50%)}
.behavior-card.highlight .bc-num{color:#e8530e;opacity:1;font-size:1.6rem;position:static;transform:none;margin-top:16px}
/* 인사이트 */
.insight-box{background:#000;padding:40px 32px;margin:48px 0}
.insight-box .ins-label{font-size:.68rem;color:#666;font-weight:700;letter-spacing:2px;margin-bottom:16px}
.insight-box p{color:#fff;font-size:1.05rem;line-height:1.9;font-weight:500;margin:0}
.insight-box strong{color:#e8530e;font-weight:700}
/* 오디언스 카드 */
.audience-card{background:#111;padding:32px;margin-bottom:16px}
/* 기타 레거시 */
.ind-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.ind-card{background:#f7f7f7;padding:16px}
.ind-card .ind-title{font-size:.82rem;font-weight:700;color:#000;margin-bottom:4px}
.ind-card .ind-desc{font-size:.75rem;color:#888;line-height:1.4}
.hero-img{width:100%;height:280px;object-fit:cover;filter:grayscale(100%)}
.footer{text-align:center;color:#ccc;font-size:.72rem;padding:40px 0 16px}
.back-btn{display:inline-block;background:#000;color:#fff;padding:8px 20px;font-size:.78rem;font-weight:600;text-decoration:none;margin-bottom:16px}
.back-btn:hover{background:#333}
/* 메인 피드 */
.ch-grid{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding-bottom:8px}
.ch-grid::-webkit-scrollbar{height:4px}
.ch-grid::-webkit-scrollbar-thumb{background:#ddd;border-radius:2px}
.ch-card{min-width:220px;max-width:260px;flex-shrink:0;scroll-snap-align:start;background:#fff;border:1px solid #e5e5e5;padding:20px;text-decoration:none;color:inherit;transition:background .15s}
.ch-card:hover{background:#fafafa}
.ch-card img{width:100%;height:120px;object-fit:cover;filter:grayscale(100%);margin-bottom:12px}
.today-card{padding:36px 0;border-bottom:1px solid #e5e5e5;display:block;text-decoration:none;color:inherit}
.today-card:hover{opacity:.9}
.today-card img{width:100%;height:240px;object-fit:cover;filter:grayscale(100%);margin-bottom:24px}
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

    body = f'<a class="back-btn" href="index.html">← 뒤로</a>\n{essay_html}\n{related_html}'
    with open(os.path.join(OUT, f"{e['id']}.html"), "w") as f:
        f.write(page_wrap(e["title"], body))
    print(f"OK: {e['id']}.html")

print(f"\nDONE — {len(os.listdir(OUT))} files in docs/")
