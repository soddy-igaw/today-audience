import streamlit as st
import os

_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="오늘의 오디언스", page_icon="🎯", layout="wide")

@st.cache_data
def load_essay(name):
    with open(os.path.join(_DIR, "essays_html", f"{name}.html"), "r") as f:
        return f.read()

# URL 쿼리 파라미터 ↔ 세션 상태 연동
params = st.query_params
if "view" in params:
    st.session_state.view = params["view"]
elif "view" not in st.session_state:
    st.session_state.view = "feed"

def go(view):
    st.session_state.view = view
    st.query_params["view"] = view
    

def go_feed():
    st.session_state.view = "feed"
    st.query_params.clear()
    

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
* { margin:0; padding:0; box-sizing:border-box; }
.stApp { background:#fff; font-family:'Pretendard',sans-serif; }
header, .stDeployButton, #MainMenu, footer, [data-testid="stToolbar"] { display:none!important; }
.block-container { max-width:900px!important; padding:0 24px 100px!important; margin:0 auto!important; }

/* Feed cards */
.feed-card {
  background:#fff; border:1px solid #e5e5e5; border-radius:0; padding:24px 20px;
  cursor:pointer; transition:all 0.15s;
}
.feed-card:hover { background:#fafafa; }

.ch-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:0; border-top:1px solid #e5e5e5; }
.ch-grid .feed-card { border-top:none; border-right:1px solid #e5e5e5; }
.ch-grid .feed-card:last-child { border-right:none; }

/* Hero image */
.hero-img { width:100%; height:280px; object-fit:cover; margin-bottom:0; filter:grayscale(100%); }

/* Detail page */
.detail-wrap { max-width:600px; margin:0 auto; }
.detail-hero { background:#fff; border-radius:0; padding:32px 0; margin-bottom:16px; border-bottom:1px solid #e5e5e5; }
.detail-emoji { font-size:2.4rem; margin-bottom:16px; }
.detail-tag { display:inline-block; font-size:0.68rem; font-weight:600; color:#000; background:#f0f0f0; padding:3px 10px; border-radius:0; margin-bottom:12px; }
.detail-title { font-size:1.4rem; font-weight:900; color:#000; line-height:1.35; margin-bottom:8px; }
.detail-sub { font-size:0.88rem; color:#666; line-height:1.6; }
.detail-meta { font-size:0.72rem; color:#999; margin-top:16px; }

/* Content sections */
.section { background:#fff; border-radius:0; padding:28px 0; margin-bottom:0; border-bottom:1px solid #f0f0f0; }
.section-label { font-size:0.68rem; font-weight:700; color:#000; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:14px; }
.section p { color:#333; font-size:1.02rem; line-height:1.85; margin-bottom:16px; }
.section strong { color:#000; }

.quote-box { background:#f7f7f7; border-radius:0; padding:24px; margin-bottom:14px; border-left:3px solid #000; }
.quote-box p { color:#444; font-size:1rem; line-height:1.8; font-style:italic; margin:0; }

.signal-item { padding:14px 0; border-bottom:1px solid #f0f0f0; }
.signal-item:last-child { border-bottom:none; }
.signal-title { font-size:0.85rem; font-weight:700; color:#000; margin-bottom:4px; }
.signal-desc { font-size:0.78rem; color:#888; line-height:1.5; }

.cmp-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.cmp-card { border-radius:0; padding:20px; }
.cmp-card h4 { font-size:0.72rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px; font-weight:700; }
.cmp-card p { font-size:0.82rem; line-height:1.8; margin:0; }
.cmp-left { background:#f7f7f7; }
.cmp-left h4 { color:#999; }
.cmp-left p { color:#888; }
.cmp-right { background:#000; }
.cmp-right h4 { color:#999; }
.cmp-right p { color:#fff; }

.ind-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.ind-card { background:#f7f7f7; border-radius:0; padding:16px; }
.ind-card .ind-title { font-size:0.82rem; font-weight:700; color:#000; margin-bottom:4px; }
.ind-card .ind-desc { font-size:0.75rem; color:#888; line-height:1.4; }

.insight-box { background:#000; border-radius:0; padding:28px 24px; margin-bottom:14px; }
.insight-box .ins-label { font-size:0.68rem; color:#888; font-weight:700; letter-spacing:1.5px; margin-bottom:12px; }
.insight-box p { color:#fff; font-size:0.92rem; line-height:1.8; font-weight:500; margin:0; }

.audience-card { background:#000; border-radius:0; padding:28px 24px; margin-bottom:14px; }

.ad-compare { background:#fff; border-radius:0; padding:28px 24px; margin-bottom:14px; border:1px solid #e5e5e5; }

/* Timeline */
.tl { padding-left:24px; border-left:2px solid #ddd; margin-left:6px; }
.tl-item { margin-bottom:24px; position:relative; }
.tl-dot { position:absolute; left:-30px; top:3px; width:10px; height:10px; border-radius:50%; border:2px solid #fff; }
.tl-green { background:#000; box-shadow:0 0 0 2px #000; }
.tl-yellow { background:#888; box-shadow:0 0 0 2px #888; }
.tl-red { background:#000; box-shadow:0 0 0 2px #000; }
.tl-day { font-size:0.68rem; font-weight:700; margin-bottom:4px; color:#000; }
.tl-title { font-size:0.88rem; font-weight:700; color:#000; margin-bottom:2px; }
.tl-desc { font-size:0.78rem; color:#888; }
.tl-bar-wrap { margin-top:8px; background:#f7f7f7; border-radius:0; padding:8px 12px; }
.tl-bar-bg { background:#e5e5e5; border-radius:0; height:6px; overflow:hidden; }
.tl-bar-fill { background:#000; height:100%; border-radius:0; }
.tl-flow { margin-top:8px; display:flex; gap:8px; align-items:center; }
.tl-flow-down { background:#f7f7f7; border-radius:0; padding:6px 10px; flex:1; text-align:center; }
.tl-flow-up { background:#000; border-radius:0; padding:6px 10px; flex:1; text-align:center; color:#fff; }
.tl-alert { background:#f7f7f7; border-radius:0; padding:16px; border:1px solid #000; }

/* Countdown */
.cd-item { background:#f7f7f7; border-radius:0; padding:16px; margin-bottom:10px; border-left:3px solid #ddd; }
.cd-urgent { border-left-color:#000; background:#f7f7f7; }
.cd-warn { border-left-color:#888; }
.cd-info { border-left-color:#000; }

/* App flow */
.af-row { display:flex; align-items:center; gap:8px; margin-bottom:8px; }
.af-gone { background:#f7f7f7; border-radius:0; padding:8px 14px; text-decoration:line-through; color:#bbb; font-size:0.82rem; flex:1; text-align:center; }
.af-new { background:#000; border-radius:0; padding:8px 14px; color:#fff; font-weight:700; font-size:0.82rem; flex:1; text-align:center; }
.af-up { background:#f7f7f7; border-radius:0; padding:8px 14px; color:#000; font-weight:700; font-size:0.82rem; flex:1; text-align:center; }

.footer { text-align:center; color:#bbb; font-size:0.72rem; padding:32px 0 16px; }

/* Hide helper buttons */
.hidden-btn { display:none!important; }

/* Streamlit button overrides */
div[data-testid="stButton"] > button {
  width:auto!important; background:#000!important; border:none!important;
  border-radius:0!important; padding:8px 20px!important; min-height:auto!important;
  font-size:0.78rem!important; color:#fff!important; font-weight:600!important;
  cursor:pointer!important; margin:8px 0 0!important;
}
div[data-testid="stButton"] > button:hover { background:#333!important; }
div[data-testid="stButton"] > button:focus { box-shadow:none!important; }

@media(max-width:768px) {
  .block-container { max-width:100%!important; }
  .ch-grid { grid-template-columns:1fr!important; }
  .ch-grid .feed-card { border-right:none!important; border-bottom:1px solid #e5e5e5; }
}
</style>
""", unsafe_allow_html=True)

# ===== CARD DATA =====
ESSAYS = [
    {
        "id": "realestate", "emoji": "🏠", "tag": "부동산", "number": 10,
        "title": "전세→매매 전환 중,\n차 담보로 부족분을 메우는 사람",
        "sub": "주담대 한도가 부족할 때, 자동차가 두 번째 담보가 됩니다",
        "stat": "~34만",
        "stat_label": "부동산+대출앱 동시 사용자 (DMP)",
        "date": "2026.04.15",
        "color": "#000",
        "img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "wegovy", "emoji": "💊", "tag": "헬스", "number": 14,
        "title": "다이어트약 처방 후\n운동을 끊은 사람",
        "sub": "GLP-1 다이어트약 처방이 폭발하면서, 운동으로 빼는 사람과 약으로 빼는 사람이 갈리고 있습니다",
        "stat": "~18만",
        "stat_label": "병원예약+약국앱 동시 활성 (DMP)",
        "date": "2026.04.16",
        "color": "#000",
        "img": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800https://images.unsplash.com/photo-1505576399279-0d754c0ce141?w=800&h=400&fit=crop&q=80h=400https://images.unsplash.com/photo-1505576399279-0d754c0ce141?w=800&h=400&fit=crop&q=80fit=crophttps://images.unsplash.com/photo-1505576399279-0d754c0ce141?w=800&h=400&fit=crop&q=80q=80",
    },
    {
        "id": "car", "emoji": "🚗", "tag": "자동차", "number": 8,
        "title": "전기차에서 하이브리드로\n선택지를 바꾼 사람",
        "sub": "보조금 축소 뉴스 보고 전기차를 포기한 게 아니라, 선택지를 바꾼 겁니다",
        "stat": "~80만",
        "stat_label": "자동차앱 사용자 (DMP)",
        "date": "2026.04.14",
        "color": "#dc2626",
        "img": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "game", "emoji": "🎮", "tag": "게임", "number": 9,
        "title": "신작 발표 후\n게이밍 하드웨어 구매 직전인 사람",
        "sub": "신작 출시 전 게임 커뮤니티 접속이 3배 뛰면, 하드웨어 지갑이 열립니다",
        "stat": "~140만",
        "stat_label": "게임앱 사용자 (DMP)",
        "date": "2026.04.14",
        "color": "#7c3aed",
        "img": "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "stock", "emoji": "📈", "tag": "증권", "number": 7,
        "title": "미국주식에서\n금으로 갈아타는 사람",
        "sub": "트럼프 관세에 미장을 판 서학개미, 금으로 갈아탔습니다",
        "stat": "~97만",
        "stat_label": "증권앱 사용자 (DMP)",
        "date": "2026.04.14",
        "color": "#eab308",
        "img": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "ktx", "emoji": "🚄", "tag": "여행", "number": 13,
        "title": "KTX 매진 후\n대안 교통을 찾는 사람",
        "sub": "외국인 관광객이 KR Pass로 좌석을 쓸어가면, 내국인은 대안 교통을 찾기 시작합니다",
        "stat": "~27만",
        "stat_label": "코레일+교통앱 동시 활성 (DMP)",
        "date": "2026.04.15",
        "color": "#000",
        "img": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "travel", "emoji": "✈️", "tag": "여행", "number": 5,
        "title": "해외여행 대신\n국내여행으로 전환한 사람",
        "sub": "환율 1,450원 시대, 여행을 포기한 게 아니라 방향을 바꾼 겁니다",
        "stat": "~65만",
        "stat_label": "여행앱 사용자 (DMP)",
        "date": "2026.04.14",
        "color": "#0ea5e9",
        "img": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "pet", "emoji": "🐾", "tag": "반려동물", "number": 4,
        "title": "반려동물 첫 입양 후\n2주 이내 사람",
        "sub": "2주 안에 펫앱 3개를 동시에 까는 사람은 3년 고객이 됩니다",
        "stat": "~13만",
        "stat_label": "펫앱+커머스 (DMP)",
        "date": "2026.04.13",
        "color": "#f97316",
        "img": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "themestock", "emoji": "🔥", "tag": "테마주", "number": 12,
        "title": "테마주 뉴스에 반응해\n추격 매수하는 사람",
        "sub": "광통신 600% 폭등 뉴스에 증권앱 검색이 터진 사람, 테마주 추격 매수 직전입니다",
        "stat": "~52만",
        "stat_label": "뉴스+증권앱 동시 활성 (DMP)",
        "date": "2026.04.15",
        "color": "#000",
        "img": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "carinsurance", "emoji": "🛡️", "tag": "금융", "number": 15,
        "title": "자동차보험 만기 전\n갈아타기 비교 중인 사람",
        "sub": "작년보다 15만원 올랐다면, 지금 갈아타세요. 3분이면 비교 끝",
        "stat": "~41만",
        "stat_label": "보험사+비교앱 동시 활성 (DMP)",
        "date": "2026.04.16",
        "color": "#000",
        "img": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "finance", "emoji": "💰", "tag": "금융", "number": 2,
        "title": "대출 만기 전\n대환을 준비하는 사람",
        "sub": "새벽 2시에 대출앱 3개를 번갈아 여는 사람",
        "stat": "~10만",
        "stat_label": "대출탐색 유저 (DMP)",
        "date": "2026.04.10",
        "color": "#6366f1",
        "img": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "running", "emoji": "🏃", "tag": "러닝", "number": 11,
        "title": "매주 뛰면서\n러닝 장비에 돈 쓰는 사람",
        "sub": "커머스에서 15만원짜리 러닝화를 반복 조회하면서, 주말 아침 한강에 나타나는 사람",
        "stat": "~48만",
        "stat_label": "러닝앱+커머스 동시 활성 (DMP)",
        "date": "2026.04.15",
        "color": "#000",
        "img": "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "golf", "emoji": "⛳", "tag": "골프", "number": 1,
        "title": "접대 때문에\n골프 시작한 입문자",
        "sub": "접대 골프 입문자는 고민하지 않습니다. 빠르게 삽니다.",
        "stat": "~17만",
        "stat_label": "골프앱 사용자 (DMP)",
        "date": "2026.04.11",
        "color": "#16a34a",
        "img": "https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=800&h=400&fit=crop&q=80",
    },
    {
        "id": "health", "emoji": "💪", "tag": "건강", "number": 6,
        "title": "운동 시작 후\n2주째 지속 중인 사람",
        "sub": "다이어트를 결심한 게 아니라, 몸이 바뀌기 시작한 겁니다",
        "stat": "~103만",
        "stat_label": "운동앱 사용자 (DMP)",
        "date": "2026.04.14",
        "color": "#14b8a6",
        "img": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=400&fit=crop&q=80",
    },
]

# ===== ROUTING =====
if st.session_state.view == "detail_wegovy":
    if st.button("← 뒤로", key="back_wg"):
        go_feed()
    st.markdown(load_essay("wegovy"), unsafe_allow_html=True)

elif st.session_state.view == "detail_carinsurance":
    if st.button("← 뒤로", key="back_ci"):
        go_feed()
    st.markdown(load_essay("carinsurance"), unsafe_allow_html=True)

elif st.session_state.view == "detail_realestate":
    if st.button("← 뒤로", key="back_re"):
        go_feed()
    st.markdown(load_essay("realestate"), unsafe_allow_html=True)

elif st.session_state.view == "detail_running":
    if st.button("← 뒤로", key="back_run"):
        go_feed()
    st.markdown(load_essay("running"), unsafe_allow_html=True)

elif st.session_state.view == "detail_car":
    if st.button("← 뒤로", key="back_car"):
        go_feed()
    st.markdown(load_essay("car"), unsafe_allow_html=True)

elif st.session_state.view == "detail_game":
    if st.button("← 뒤로", key="back_game"):
        go_feed()
    st.markdown(load_essay("game"), unsafe_allow_html=True)

elif st.session_state.view == "detail_themestock":
    if st.button("← 뒤로", key="back_ts"):
        go_feed()
    st.markdown(load_essay("themestock"), unsafe_allow_html=True)

elif st.session_state.view == "detail_stock":
    if st.button("← 뒤로", key="back_s"):
        go_feed()
    st.markdown(load_essay("stock"), unsafe_allow_html=True)

elif st.session_state.view == "detail_ktx":
    if st.button("← 뒤로", key="back_ktx"):
        go_feed()
    st.markdown(load_essay("ktx"), unsafe_allow_html=True)

elif st.session_state.view == "detail_travel":
    if st.button("← 뒤로", key="back_t"):
        go_feed()
    st.markdown(load_essay("travel"), unsafe_allow_html=True)

elif st.session_state.view == "detail_golf":
    if st.button("← 뒤로", key="back_g"):
        go_feed()
    st.markdown(load_essay("golf"), unsafe_allow_html=True)

elif st.session_state.view == "detail_finance":
    if st.button("← 뒤로", key="back_f"):
        go_feed()
    st.markdown(load_essay("finance"), unsafe_allow_html=True)

elif st.session_state.view == "detail_health":
    if st.button("← 뒤로", key="back_h"):
        go_feed()
    st.markdown(load_essay("health"), unsafe_allow_html=True)

elif st.session_state.view == "detail_pet":
    if st.button("← 뒤로", key="back_p"):
        go_feed()
    st.markdown(load_essay("pet"), unsafe_allow_html=True)

else:
    # ===== FEED (롱블랙 스타일 · B&W) =====

    CHAPTERS = [
        {"label": "금융", "ids": ["finance", "stock", "realestate", "themestock", "carinsurance"]},
        {"label": "여행", "ids": ["travel", "ktx"]},
        {"label": "스포츠", "ids": ["running", "golf", "health", "wegovy"]},
        {"label": "라이프", "ids": ["car", "pet"]},
        {"label": "게임", "ids": ["game"]},
    ]
    ESSAY_MAP = {e["id"]: e for e in ESSAYS}
    today = ESSAYS[0]

    # --- 헤더 ---
    st.markdown("""
    <div style="padding:48px 0 16px;border-bottom:3px solid #000;margin-bottom:0">
      <p style="font-size:0.68rem;font-weight:700;letter-spacing:3px;color:#999;margin-bottom:10px">AUDIENCE IDEA BANK</p>
      <h1 style="font-size:2rem;font-weight:900;color:#000;line-height:1.2;letter-spacing:-1px">오늘의 오디언스</h1>
      <p style="color:#999;font-size:0.82rem;line-height:1.6;margin-top:8px">트렌드를 읽고, 행동 시그널을 조합해<br>아직 아무도 안 쓰는 오디언스를 제안합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- 오늘의 오디언스 (크게) ---
    today_img = today.get("img", "")
    img_html = f'<img loading="lazy" src="{today_img}" style="width:100%;height:240px;object-fit:cover;filter:grayscale(100%);margin-bottom:24px">' if today_img else ""
    st.markdown(f"""
    <div style="padding:36px 0;border-bottom:1px solid #e5e5e5">
      {img_html}
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:20px">
        <span style="font-size:0.68rem;font-weight:900;color:#e8530e;background:#000;padding:4px 10px;letter-spacing:2px">TODAY</span>
        <span style="font-size:0.68rem;font-weight:700;color:#000;background:#f0f0f0;padding:4px 12px">{today["tag"]}</span>
        <span style="font-size:0.68rem;color:#999">{today["date"]}</span>
      </div>
      <div style="font-size:1.8rem;font-weight:900;color:#000;line-height:1.3;margin-bottom:12px">{today["title"].replace(chr(10), "<br>")}</div>
      <div style="font-size:0.9rem;color:#666;line-height:1.7;margin-bottom:24px">{today["sub"]}</div>
      <div style="display:flex;align-items:center;gap:12px">
        <span style="font-size:1.2rem;font-weight:900;color:#000">{today["stat"]}</span>
        <span style="font-size:0.72rem;color:#999">{today["stat_label"]}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("읽기 →", key=f"go_{today['id']}", use_container_width=True):
        go(f"detail_{today['id']}")
        

    # --- 챕터별 섹션 (3열 그리드) ---
    for ch in CHAPTERS:
        ch_essays = [ESSAY_MAP[eid] for eid in ch["ids"] if eid in ESSAY_MAP and eid != today["id"]]
        if not ch_essays:
            continue

        st.markdown(f"""
        <div style="margin-top:48px;margin-bottom:16px;padding-bottom:12px;border-bottom:2px solid #000">
          <span style="font-size:0.95rem;font-weight:900;color:#000">{ch["label"]}</span>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        for i, e in enumerate(ch_essays):
            with cols[i % 3]:
                card_img = e.get("img", "").replace("w=800", "w=400")
                img_tag = f'<img loading="lazy" src="{card_img}" style="width:100%;height:120px;object-fit:cover;filter:grayscale(100%);margin-bottom:12px">' if card_img else ""
                st.markdown(f"""
                <div style="padding:4px 0">
                  {img_tag}
                  <div style="font-size:0.62rem;font-weight:700;color:#999;letter-spacing:1px;margin-bottom:10px">{e["tag"].upper()}</div>
                  <div style="font-size:1rem;font-weight:800;color:#000;line-height:1.4;margin-bottom:6px">{e["title"].replace(chr(10), " ")}</div>
                  <div style="font-size:0.72rem;color:#999;line-height:1.5;margin-bottom:12px">{e["sub"][:50]}...</div>
                  <div style="font-size:0.95rem;font-weight:900;color:#000">{e["stat"]}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("읽기 →", key=f"go_{e['id']}"):
                    go(f"detail_{e['id']}")

    st.markdown('<div class="footer">오늘의 오디언스 · by IGAWorks · © 2026</div>', unsafe_allow_html=True)
