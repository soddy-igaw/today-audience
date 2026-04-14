import streamlit as st

st.set_page_config(page_title="오늘의 오디언스", page_icon="🎯", layout="wide")

if "view" not in st.session_state:
    st.session_state.view = "feed"

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
* { margin:0; padding:0; box-sizing:border-box; }
.stApp { background:#f5f6f8; font-family:'Pretendard',sans-serif; }
header, .stDeployButton, #MainMenu, footer, [data-testid="stToolbar"] { display:none!important; }
.block-container { max-width:960px!important; padding:0 32px 100px!important; margin:0 auto!important; }

/* Feed cards */
.feed-card {
  background:#fff; border-radius:20px; padding:28px 24px; margin-bottom:14px;
  cursor:pointer; transition:all 0.2s;
  box-shadow:0 1px 3px rgba(0,0,0,0.04);
}
.feed-card:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(0,0,0,0.08); }
.feed-emoji { font-size:2.4rem; margin-bottom:16px; }
.feed-tag { display:inline-block; font-size:0.68rem; font-weight:600; color:#6366f1; background:#f0eeff; padding:3px 10px; border-radius:100px; margin-bottom:12px; }
.feed-title { font-size:1.15rem; font-weight:800; color:#111; line-height:1.4; margin-bottom:6px; }
.feed-sub { font-size:0.82rem; color:#888; line-height:1.5; }
.feed-bottom { display:flex; align-items:center; justify-content:space-between; margin-top:20px; padding-top:16px; border-top:1px solid #f0f0f0; }
.feed-stat { font-size:0.75rem; color:#aaa; }
.feed-stat strong { color:#6366f1; font-weight:700; }
.feed-arrow { color:#ccc; font-size:1.2rem; }

/* Detail page */
.detail-wrap { max-width:620px; margin:0 auto; }
.detail-back { font-size:0.85rem; color:#888; margin-bottom:24px; cursor:pointer; }
.detail-hero { background:#fff; border-radius:20px; padding:32px 24px; margin-bottom:16px; }
.detail-emoji { font-size:3rem; margin-bottom:16px; }
.detail-tag { display:inline-block; font-size:0.68rem; font-weight:600; color:#6366f1; background:#f0eeff; padding:3px 10px; border-radius:100px; margin-bottom:12px; }
.detail-title { font-size:1.4rem; font-weight:900; color:#111; line-height:1.35; margin-bottom:8px; }
.detail-sub { font-size:0.88rem; color:#888; line-height:1.6; }
.detail-meta { font-size:0.72rem; color:#bbb; margin-top:16px; }

/* Content sections */
.section { background:#fff; border-radius:20px; padding:28px 24px; margin-bottom:14px; }
.section-label { font-size:0.68rem; font-weight:700; color:#6366f1; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:14px; }
.section p { color:#333; font-size:0.9rem; line-height:1.9; margin-bottom:16px; }
.section strong { color:#111; }

.quote-box { background:#f8f7ff; border-radius:16px; padding:24px; margin-bottom:14px; }
.quote-box p { color:#555; font-size:0.95rem; line-height:1.8; font-style:italic; margin:0; }

.signal-item { padding:14px 0; border-bottom:1px solid #f5f5f5; }
.signal-item:last-child { border-bottom:none; }
.signal-title { font-size:0.85rem; font-weight:700; color:#111; margin-bottom:4px; }
.signal-desc { font-size:0.78rem; color:#888; line-height:1.5; }

.cmp-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.cmp-card { border-radius:14px; padding:20px; }
.cmp-card h4 { font-size:0.72rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px; font-weight:700; }
.cmp-card p { font-size:0.82rem; line-height:1.8; margin:0; }
.cmp-left { background:#f8f8f8; }
.cmp-left h4 { color:#999; }
.cmp-left p { color:#888; }
.cmp-right { background:#f0eeff; }
.cmp-right h4 { color:#6366f1; }
.cmp-right p { color:#333; }

.ind-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.ind-card { background:#f8f8f8; border-radius:12px; padding:16px; }
.ind-card .ind-title { font-size:0.82rem; font-weight:700; color:#111; margin-bottom:4px; }
.ind-card .ind-desc { font-size:0.75rem; color:#888; line-height:1.4; }

.insight-box { background:#111; border-radius:20px; padding:28px 24px; margin-bottom:14px; }
.insight-box .ins-label { font-size:0.68rem; color:#a5b4fc; font-weight:700; letter-spacing:1.5px; margin-bottom:12px; }
.insight-box p { color:#fff; font-size:0.92rem; line-height:1.8; font-weight:500; margin:0; }

.audience-card { background:#111; border-radius:20px; padding:28px 24px; margin-bottom:14px; }

.ad-compare { background:#fff; border-radius:20px; padding:28px 24px; margin-bottom:14px; }

/* Timeline */
.tl { padding-left:24px; border-left:3px solid #e5e7eb; margin-left:6px; }
.tl-item { margin-bottom:24px; position:relative; }
.tl-dot { position:absolute; left:-31px; top:3px; width:12px; height:12px; border-radius:50%; border:2px solid #fff; }
.tl-green { background:#14b8a6; box-shadow:0 0 0 2px #14b8a6; }
.tl-yellow { background:#f59e0b; box-shadow:0 0 0 2px #f59e0b; }
.tl-red { background:#ef4444; box-shadow:0 0 0 2px #ef4444; }
.tl-day { font-size:0.68rem; font-weight:700; margin-bottom:4px; }
.tl-title { font-size:0.88rem; font-weight:700; color:#111; margin-bottom:2px; }
.tl-desc { font-size:0.78rem; color:#888; }
.tl-bar-wrap { margin-top:8px; background:#f0fdf4; border-radius:8px; padding:8px 12px; }
.tl-bar-bg { background:#e5e7eb; border-radius:4px; height:8px; overflow:hidden; }
.tl-bar-fill { background:#14b8a6; height:100%; border-radius:4px; }
.tl-flow { margin-top:8px; display:flex; gap:8px; align-items:center; }
.tl-flow-down { background:#fee2e2; border-radius:8px; padding:6px 10px; flex:1; text-align:center; }
.tl-flow-up { background:#f0fdf4; border-radius:8px; padding:6px 10px; flex:1; text-align:center; }
.tl-alert { background:#fef2f2; border-radius:12px; padding:16px; border:1px solid #fecaca; }

/* Countdown */
.cd-item { background:#f8f8f8; border-radius:14px; padding:16px; margin-bottom:10px; border-left:4px solid #e5e7eb; }
.cd-urgent { border-left-color:#ef4444; background:#fef2f2; }
.cd-warn { border-left-color:#f59e0b; }
.cd-info { border-left-color:#6366f1; }

/* App flow */
.af-row { display:flex; align-items:center; gap:8px; margin-bottom:8px; }
.af-gone { background:#f3f4f6; border-radius:10px; padding:8px 14px; text-decoration:line-through; color:#bbb; font-size:0.82rem; flex:1; text-align:center; }
.af-new { background:#f0eeff; border-radius:10px; padding:8px 14px; color:#6366f1; font-weight:700; font-size:0.82rem; flex:1; text-align:center; }
.af-up { background:#f0fdf4; border-radius:10px; padding:8px 14px; color:#14b8a6; font-weight:700; font-size:0.82rem; flex:1; text-align:center; }

.footer { text-align:center; color:#ccc; font-size:0.72rem; padding:32px 0 16px; }

/* Streamlit button overrides - card style */
/* Feed cards */
.hero-card {
  background:#fff; border-radius:24px; padding:36px 32px; margin-bottom:24px;
  box-shadow:0 2px 8px rgba(0,0,0,0.06); cursor:pointer; transition:all 0.25s;
  display:flex; align-items:center; gap:32px;
}
.hero-card:hover { transform:translateY(-3px); box-shadow:0 12px 32px rgba(0,0,0,0.1); }
.hero-left { flex:1; }
.hero-right { font-size:4rem; }

.card-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-bottom:24px; }
.grid-card {
  background:#fff; border-radius:20px; padding:24px 20px; cursor:pointer;
  box-shadow:0 2px 8px rgba(0,0,0,0.06); transition:all 0.25s;
}
.grid-card:hover { transform:translateY(-3px); box-shadow:0 12px 32px rgba(0,0,0,0.1); }

@media(max-width:768px) {
  .block-container { max-width:100%!important; padding:0 16px 80px!important; }
  .card-grid { grid-template-columns:repeat(2,1fr); }
  .hero-card { flex-direction:column; gap:16px; }
}

/* Card buttons */
div[data-testid="stButton"] > button {
  width:100%!important; text-align:left!important; border:none!important;
  background:#fff!important; border-radius:20px!important; padding:24px 20px!important;
  min-height:auto!important; cursor:pointer!important;
  box-shadow:0 2px 8px rgba(0,0,0,0.06)!important; transition:all 0.25s!important;
  color:#111!important; font-size:0.88rem!important; font-weight:600!important;
  line-height:1.6!important; white-space:pre-line!important;
}
div[data-testid="stButton"] > button:hover {
  transform:translateY(-3px)!important; box-shadow:0 12px 32px rgba(0,0,0,0.1)!important;
  background:#fff!important; color:#111!important;
}
div[data-testid="stButton"] > button:focus { box-shadow:0 2px 8px rgba(0,0,0,0.06)!important; }

@media(max-width:768px) {
  .block-container { max-width:100%!important; padding:0 16px 80px!important; }
}
</style>
""", unsafe_allow_html=True)

# ===== CARD DATA =====
ESSAYS = [
    {
        "id": "car", "emoji": "🚗", "tag": "자동차", "number": 8,
        "title": "전기차 앱 지우고\n하이브리드 비교앱 깐 사람",
        "sub": "보조금 축소 뉴스 보고 전기차를 포기한 게 아니라, 선택지를 바꾼 겁니다",
        "stat": "~80만",
        "stat_label": "자동차앱 사용자 (DMP)",
        "date": "2026.04.14",
        "color": "#dc2626",
    },
    {
        "id": "game", "emoji": "🎮", "tag": "게임", "number": 9,
        "title": "스위치2 예약 알림 켜고\n게이밍 노트북 비교 시작한 사람",
        "sub": "신작 출시 전 게임 커뮤니티 접속이 3배 뛰면, 하드웨어 지갑이 열립니다",
        "stat": "~140만",
        "stat_label": "게임앱 사용자 (DMP)",
        "date": "2026.04.14",
        "color": "#7c3aed",
    },
    {
        "id": "stock", "emoji": "📈", "tag": "증권", "number": 7,
        "title": "미국주식 앱 알림을 끄고\n금 시세앱을 깐 사람",
        "sub": "트럼프 관세에 미장을 판 서학개미, 금으로 갈아탔습니다",
        "stat": "~97만",
        "stat_label": "증권앱 사용자 (DMP)",
        "date": "2026.04.14",
        "color": "#eab308",
    },
    {
        "id": "travel", "emoji": "✈️", "tag": "여행", "number": 5,
        "title": "해외여행 앱을 지우고\n국내 펜션앱을 깐 사람",
        "sub": "환율 1,450원 시대, 여행을 포기한 게 아니라 방향을 바꾼 겁니다",
        "stat": "~65만",
        "stat_label": "여행앱 사용자 (DMP)",
        "date": "2026.04.14",
        "color": "#0ea5e9",
    },
    {
        "id": "pet", "emoji": "🐾", "tag": "반려동물", "number": 4,
        "title": "첫 입양 후 2주,\n앱이 폭발하는 사람",
        "sub": "2주 안에 펫앱 3개를 동시에 까는 사람은 3년 고객이 됩니다",
        "stat": "~13만",
        "stat_label": "펫앱+커머스 (DMP)",
        "date": "2026.04.13",
        "color": "#f97316",
    },
    {
        "id": "finance", "emoji": "💰", "tag": "금융", "number": 2,
        "title": "대출앱 3개를 동시에\n깐 사람의 비밀",
        "sub": "불 난 사람한테 소화기 할인 쿠폰을 보내지 마세요",
        "stat": "~10만",
        "stat_label": "대출탐색 유저 (DMP)",
        "date": "2026.04.10",
        "color": "#6366f1",
    },
    {
        "id": "golf", "emoji": "⛳", "tag": "골프", "number": 1,
        "title": "드라이버를 사는 게 아니라\n창피를 안 당할 보험을 삽니다",
        "sub": "접대 골프 입문자는 고민하지 않습니다. 빠르게 삽니다.",
        "stat": "~17만",
        "stat_label": "골프앱 사용자 (DMP)",
        "date": "2026.04.11",
        "color": "#16a34a",
    },
    {
        "id": "health", "emoji": "💪", "tag": "건강", "number": 6,
        "title": "러닝앱 깔고 3일 만에\n식단앱까지 깐 사람",
        "sub": "다이어트를 결심한 게 아니라, 몸이 바뀌기 시작한 겁니다",
        "stat": "~103만",
        "stat_label": "운동앱 사용자 (DMP)",
        "date": "2026.04.14",
        "color": "#14b8a6",
    },
]

# ===== ROUTING =====
if st.session_state.view == "detail_car":
    if st.button("← 뒤로", key="back_car"):
        st.session_state.view = "feed"
        st.rerun()
    st.markdown("""
    <div class="detail-wrap">
    <div class="detail-hero">
      <div class="detail-emoji">🚗</div>
      <span class="detail-tag">자동차</span>
      <div class="detail-title">전기차 앱 지우고 하이브리드 비교앱 깐 사람</div>
      <div class="detail-sub">보조금 축소 뉴스 보고 전기차를 포기한 게 아니라, 선택지를 바꾼 겁니다</div>
      <div class="detail-meta">2026.04.14 · 오늘의 오디언스 #8</div>
    </div>

    <div class="quote-box">
      <p>"테슬라 모델Y 계약 직전이었어요.<br>근데 하반기 보조금 개편 뉴스 보고 멈췄어요.<br>지금은 하이브리드 비교하고 있어요.<br>보조금 빠지면 전기차 가성비가 안 나오거든요."<br><br>— F씨, 39세, 2인 가구 맞벌이</p>
    </div>

    <div class="section">
      <p>2026년 하반기, 전기차 보조금이 전면 개편됩니다. 테슬라가 지원 대상에서 빠질 수 있다는 보도까지.</p>
      <p>동시에 중국산 BYD·테슬라가 한국 시장을 휩쓸면서, 국산 전기차 판매는 주춤. 소비자들은 혼란 속에서 <strong>전기차 → 하이브리드로 선택지를 바꾸고 있습니다.</strong></p>
      <p>자동차 마케터들은 아직 "전기차 관심자"를 타겟합니다. 하지만 이 중 상당수는 <strong>이미 전기차를 포기하고 하이브리드를 보고 있는 사람</strong>입니다.</p>
    </div>

    <div class="quote-box">
      <p>"자동차 커뮤니티에서 하이브리드 후기만 찾아봐요.<br>전기차 충전 인프라도 불안하고, 보조금도 줄고.<br>차라리 하이브리드가 현실적이더라고요.<br>이번 주말에 딜러 시승 예약했어요."<br><br>— F씨</p>
    </div>

    <div class="section">
      <div class="section-label">BEHAVIOR TIMELINE</div>
      <p style="font-size:0.78rem;color:#999;margin-bottom:20px">F씨의 자동차 앱 사용 변화를 DMP로 추적하면</p>
      <div class="tl">
        <div class="tl-item">
          <div class="tl-dot tl-green" style="background:#dc2626;box-shadow:0 0 0 2px #dc2626"></div>
          <div class="tl-day" style="color:#dc2626">DAY 0 · 보조금 뉴스 충격</div>
          <div class="tl-title">📰 뉴스앱 자동차/보조금 기사 집중 소비</div>
          <div class="tl-desc">뉴스앱 접속 빈도 증가 + 자동차 관련 기사 체류 시간 증가</div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-green" style="background:#dc2626;box-shadow:0 0 0 2px #dc2626"></div>
          <div class="tl-day" style="color:#dc2626">DAY 1~5 · 비교 탐색 시작</div>
          <div class="tl-title">🔍 자동차 비교앱 사용 급증</div>
          <div class="tl-desc">자동차 브랜드/구매정보 카테고리 앱 사용 시간 2배+ 증가</div>
          <div class="tl-flow">
            <div class="tl-flow-down">
              <div style="font-size:0.65rem;color:#999">전기차 전용앱</div>
              <div style="font-size:0.85rem;font-weight:800;color:#ef4444">사용↓</div>
            </div>
            <div style="color:#ccc">→</div>
            <div class="tl-flow-up">
              <div style="font-size:0.65rem;color:#999">종합 비교앱</div>
              <div style="font-size:0.85rem;font-weight:800;color:#dc2626">사용↑↑</div>
            </div>
          </div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-yellow"></div>
          <div class="tl-day" style="color:#f59e0b">DAY 7~10 · 딜러 방문 준비</div>
          <div class="tl-title">📍 자동차 딜러십 방문지 데이터 발생</div>
          <div class="tl-desc">주말 딜러십/전시장 체류 시간 발생 → 시승 단계 진입</div>
        </div>
        <div class="tl-item" style="margin-bottom:0">
          <div class="tl-dot tl-red"></div>
          <div class="tl-alert">
            <div style="font-size:0.68rem;color:#ef4444;font-weight:700;margin-bottom:4px">⚡ DAY 14 · 여기서 잡아야 합니다</div>
            <div class="tl-title">계약 / 할부 비교 / 보험 가입</div>
            <div class="tl-desc">시승 후 2주 내 계약 전환율이 가장 높음. 할부/보험/용품 동시 지출</div>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="cmp-grid">
        <div class="cmp-card cmp-left"><h4>자동차 구경꾼</h4><p>자동차앱 가끔 접속<br>특정 브랜드만 탐색<br>딜러 방문 없음<br>뉴스 소비 변화 없음<br>"내년에 바꿀까"</p></div>
        <div class="cmp-card cmp-right"><h4>전환 검토 중인 구매자</h4><p>비교앱 사용 급증<br>전기차→하이브리드 전환<br>주말 딜러십 방문<br>보조금/할부 뉴스 집중<br>2주 내 계약 가능</p></div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">DMP에서 잡는 법</div>
      <p><strong>[전환 검토 중인 구매자]</strong><br>자동차 비교앱 사용 시간 2배+ 증가 (14일 내)<br>+ 딜러십/전시장 방문지 데이터 발생<br>+ 뉴스앱 자동차 관련 소비 증가<br><br><em style="color:#888;font-size:0.8rem">* DMP 실측: 자동차앱 사용자 약 80만명 (30일 기준)</em></p>
    </div>

    <div class="section">
      <div class="ind-grid">
        <div class="ind-card"><div class="ind-title">🚗 완성차 브랜드</div><div class="ind-desc">"보조금 없어도 가성비 1등 하이브리드"</div></div>
        <div class="ind-card"><div class="ind-title">💳 할부/리스</div><div class="ind-desc">"월 39만원, 부담 없는 하이브리드 리스"</div></div>
        <div class="ind-card"><div class="ind-title">🛡️ 자동차보험</div><div class="ind-desc">"신차 구매 시 첫 해 보험료 30% 할인"</div></div>
        <div class="ind-card"><div class="ind-title">⛽ 주유/충전</div><div class="ind-desc">"하이브리드 오너 전용 주유 캐시백"</div></div>
      </div>
    </div>

    <div class="insight-box">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"자동차 관심자"는 오디언스가 아닙니다.<br><br>전기차 앱 사용이 줄고 비교앱이 늘어난 사람,<br>그리고 <strong>주말에 딜러십을 방문한 사람</strong>이 오디언스입니다.<br>이 사람은 포기한 게 아니라 선택지를 바꾼 겁니다.</p>
    </div>

    <div class="ad-compare">
      <p style="font-size:0.85rem;font-weight:700;color:#111;margin-bottom:16px">이 오디언스에게 보내는 광고</p>
      <p style="font-size:0.85rem;color:#999;margin-bottom:8px">❌ "전기차 보조금 최대 780만원! 지금 계약하세요"</p>
      <p style="font-size:0.85rem;color:#111;font-weight:600">✅ "보조금 없어도 연비로 뽑는 하이브리드, 시승 예약하세요"</p>
    </div>

    <div class="audience-card">
      <p style="font-size:0.68rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:20px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.15rem;font-weight:800;margin-bottom:20px">전환 검토 중인 자동차 구매자</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추정 모수 (DMP 실측)</p><p style="color:#6366f1;font-size:1.5rem;font-weight:900">~80만</p><p style="color:#555;font-size:0.7rem">자동차앱 사용자 (DMP 30일)</p></div>
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추천 업종</p><p style="color:#fff;font-size:0.88rem;font-weight:600;line-height:1.6">완성차 · 할부/리스<br>보험 · 주유</p></div>
      </div>
    </div>

    <div class="footer">오늘의 오디언스 #8 · by IGAWorks</div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view == "detail_game":
    if st.button("← 뒤로", key="back_game"):
        st.session_state.view = "feed"
        st.rerun()
    st.markdown("""
    <div class="detail-wrap">
    <div class="detail-hero">
      <div class="detail-emoji">🎮</div>
      <span class="detail-tag">게임</span>
      <div class="detail-title">스위치2 예약 알림 켜고 게이밍 노트북 비교 시작한 사람</div>
      <div class="detail-sub">신작 출시 전 게임 커뮤니티 접속이 3배 뛰면, 하드웨어 지갑이 열립니다</div>
      <div class="detail-meta">2026.04.14 · 오늘의 오디언스 #9</div>
    </div>

    <div class="quote-box">
      <p>"GTA6 트레일러 나온 날, 스팀 앱이랑 게임 커뮤니티를<br>하루에 20번은 들어간 것 같아요.<br>그러다 내 PC 사양이 안 되겠다 싶어서<br>그 주에 게이밍 노트북 비교 시작했어요."<br><br>— G씨, 27세, 대학원생</p>
    </div>

    <div class="section">
      <p>2026년, 게임 업계 빅뱅이 시작됩니다. GTA6 출시 임박, 닌텐도 스위치2는 일본에서 PS5 대비 5배 판매, 포켓몬 챔피언스 등 모바일 신작 러시.</p>
      <p>게임 마케터들은 "게임 유저"를 타겟합니다. 하지만 매일 모바일 게임하는 사람과, <strong>신작 때문에 하드웨어까지 바꾸려는 사람</strong>은 완전히 다릅니다.</p>
      <p>G씨처럼 <strong>게임 커뮤니티 접속이 폭발하면서 동시에 전자기기 쇼핑을 시작한 사람</strong> — 이 사람이 진짜 돈 쓰는 유저입니다.</p>
    </div>

    <div class="quote-box">
      <p>"스위치2도 예약할 거고, PC도 바꿀 거예요.<br>GTA6 나오면 현재 사양으론 안 돌아가거든요.<br>게이밍 노트북 200만원짜리 보고 있어요.<br>게임 하나 때문에 200만원 쓰는 거죠."<br><br>— G씨</p>
    </div>

    <div class="section">
      <div class="section-label">BEHAVIOR TIMELINE</div>
      <p style="font-size:0.78rem;color:#999;margin-bottom:20px">G씨의 앱 사용 변화를 DMP로 추적하면</p>
      <div class="tl">
        <div class="tl-item">
          <div class="tl-dot tl-green" style="background:#7c3aed;box-shadow:0 0 0 2px #7c3aed"></div>
          <div class="tl-day" style="color:#7c3aed">DAY 0 · 신작 발표/트레일러</div>
          <div class="tl-title">🎮 게임 커뮤니티앱 접속 3배+ 급증</div>
          <div class="tl-desc">게임 관련 앱 일일 사용 시간 폭발 → 신작에 반응하는 코어 유저</div>
          <div class="tl-bar-wrap" style="background:#f5f3ff">
            <div style="font-size:0.7rem;color:#888;margin-bottom:4px">게임앱 일일 사용 시간 변화</div>
            <div class="tl-bar-bg"><div class="tl-bar-fill" style="width:90%;background:#7c3aed"></div></div>
            <div style="font-size:0.68rem;color:#7c3aed;font-weight:700;margin-top:2px">+200% — 평소 대비 3배 사용</div>
          </div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-green" style="background:#7c3aed;box-shadow:0 0 0 2px #7c3aed"></div>
          <div class="tl-day" style="color:#7c3aed">DAY 3~5 · 하드웨어 탐색 시작</div>
          <div class="tl-title">💻 전자기기 쇼핑앱에서 게이밍 기기 조회</div>
          <div class="tl-desc">쿠팡/네이버쇼핑에서 게이밍 노트북/콘솔 상품 조회 시작</div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-yellow"></div>
          <div class="tl-day" style="color:#f59e0b">DAY 7~10 · 💰 비교 쇼핑</div>
          <div class="tl-title">🛒 가격비교앱 + 커머스 반복 조회</div>
          <div class="tl-desc">같은 상품 3회+ 반복 조회 → 구매 직전 비교 단계</div>
        </div>
        <div class="tl-item" style="margin-bottom:0">
          <div class="tl-dot tl-red"></div>
          <div class="tl-alert">
            <div style="font-size:0.68rem;color:#ef4444;font-weight:700;margin-bottom:4px">⚡ DAY 14 · 여기서 잡아야 합니다</div>
            <div class="tl-title">게이밍 노트북 구매 / 콘솔 예약 / 주변기기 결제</div>
            <div class="tl-desc">신작 발표 후 2주 내 하드웨어 구매 전환. 객단가 100~200만원+</div>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="cmp-grid">
        <div class="cmp-card cmp-left"><h4>일반 게임 유저</h4><p>모바일 게임 위주<br>게임앱 사용 일정<br>하드웨어 관심 없음<br>커머스 조회 없음<br>월 지출 1~2만원</p></div>
        <div class="cmp-card cmp-right"><h4>신작 대응 코어 유저</h4><p>커뮤니티 접속 3배 급증<br>게이밍 기기 쇼핑 시작<br>상품 반복 조회 (3회+)<br>콘솔+PC 동시 탐색<br>객단가 100~200만원</p></div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">DMP에서 잡는 법</div>
      <p><strong>[신작 대응 코어 유저]</strong><br>게임앱 사용 시간 2배+ 증가 (14일 내)<br>+ 전자기기 커머스에서 게이밍 상품 조회<br>+ 같은 상품 3회+ 반복 조회<br><br><em style="color:#888;font-size:0.8rem">* DMP 실측: 게임앱 사용자 약 140만명 (30일 기준)</em></p>
    </div>

    <div class="section">
      <div class="ind-grid">
        <div class="ind-card"><div class="ind-title">💻 게이밍 노트북/PC</div><div class="ind-desc">"GTA6 풀옵 돌리는 노트북, 지금 사전예약"</div></div>
        <div class="ind-card"><div class="ind-title">🎮 콘솔/주변기기</div><div class="ind-desc">"스위치2 예약 + 프로컨 번들 할인"</div></div>
        <div class="ind-card"><div class="ind-title">🖥️ 모니터/의자</div><div class="ind-desc">"게이밍 환경 업그레이드 세트"</div></div>
        <div class="ind-card"><div class="ind-title">💳 할부/카드</div><div class="ind-desc">"게이밍 기기 무이자 12개월"</div></div>
      </div>
    </div>

    <div class="insight-box">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"게임 유저"는 오디언스가 아닙니다.<br><br>신작 발표 후 <strong>커뮤니티 접속이 3배 뛰면서<br>동시에 하드웨어 쇼핑을 시작한 사람</strong>이 오디언스입니다.<br>게임 하나 때문에 200만원을 쓰는 사람.<br>이 타이밍을 놓치면 다음 신작까지 기다려야 합니다.</p>
    </div>

    <div class="ad-compare">
      <p style="font-size:0.85rem;font-weight:700;color:#111;margin-bottom:16px">이 오디언스에게 보내는 광고</p>
      <p style="font-size:0.85rem;color:#999;margin-bottom:8px">❌ "게이밍 노트북 할인! 최대 30% OFF"</p>
      <p style="font-size:0.85rem;color:#111;font-weight:600">✅ "GTA6 풀옵으로 돌리려면, 이 사양이 필요합니다"</p>
    </div>

    <div class="audience-card">
      <p style="font-size:0.68rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:20px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.15rem;font-weight:800;margin-bottom:20px">신작 대응 코어 게이머</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추정 모수 (DMP 실측)</p><p style="color:#6366f1;font-size:1.5rem;font-weight:900">~140만</p><p style="color:#555;font-size:0.7rem">게임앱 사용자 (DMP 30일)</p></div>
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추천 업종</p><p style="color:#fff;font-size:0.88rem;font-weight:600;line-height:1.6">노트북/PC · 콘솔<br>모니터 · 할부</p></div>
      </div>
    </div>

    <div class="footer">오늘의 오디언스 #9 · by IGAWorks</div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view == "detail_stock":
    if st.button("← 뒤로", key="back_s"):
        st.session_state.view = "feed"
        st.rerun()
    st.markdown("""
    <div class="detail-wrap">
    <div class="detail-hero">
      <div class="detail-emoji">📈</div>
      <span class="detail-tag">증권</span>
      <div class="detail-title">미국주식 앱 알림을 끄고 금 시세앱을 깐 사람</div>
      <div class="detail-sub">트럼프 관세에 미장을 판 서학개미, 금으로 갈아탔습니다</div>
      <div class="detail-meta">2026.04.14 · 오늘의 오디언스 #7</div>
    </div>

    <div class="quote-box">
      <p>"4월 초에 트럼프 관세 뉴스 보고 바로 미국주식 다 팔았어요.<br>그 돈으로 금 ETF 샀어요. 환율도 불안하고, 금값은 계속 오르니까.<br>토스증권 알림은 꺼버렸어요. 대신 금방 앱 매일 확인해요."<br><br>— E씨, 31세, 스타트업 개발자</p>
    </div>

    <div class="section">
      <p>4월, 서학개미가 처음으로 미국주식 순매도로 전환했습니다.</p>
      <p>트럼프의 S301 관세 정책 재점화, 원/달러 환율 1,450원 돌파. "미장 재미없다"는 분위기가 퍼지고 있습니다.</p>
      <p>동시에 금값은 연일 신고가. "연말 6,000달러 간다"는 전망까지. <strong>"나만 안 샀어"</strong> 심리가 개인 투자자를 금으로 몰고 있습니다.</p>
      <p>증권사 마케터들은 아직 "해외주식 관심자"를 타겟합니다. 하지만 이 사람들 중 상당수는 <strong>이미 팔고 나온 사람</strong>입니다.</p>
    </div>

    <div class="quote-box">
      <p>"증권사 앱에서 '미국주식 추천' 푸시가 오는데<br>이미 다 팔았거든요. 짜증나서 알림 끄고<br>금방 앱이랑 한국금거래소 앱 깔았어요.<br>요즘은 금 투자앱을 매일 열어봐요. 증권앱은 안 켜요."<br><br>— E씨</p>
    </div>

    <div class="section">
      <div class="section-label">BEHAVIOR TIMELINE</div>
      <p style="font-size:0.78rem;color:#999;margin-bottom:20px">E씨의 투자 앱 사용 변화를 DMP로 추적하면</p>
      <div class="tl">
        <div class="tl-item">
          <div class="tl-dot tl-green" style="background:#eab308;box-shadow:0 0 0 2px #eab308"></div>
          <div class="tl-day" style="color:#eab308">DAY 0 · 관세 뉴스 충격</div>
          <div class="tl-title">📰 뉴스앱 접속 빈도 2배+ 증가</div>
          <div class="tl-desc">관세/환율/미국주식 관련 뉴스 집중 소비 → 시장 변화에 민감하게 반응</div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-green" style="background:#eab308;box-shadow:0 0 0 2px #eab308"></div>
          <div class="tl-day" style="color:#eab308">DAY 1~3 · 미장 이탈</div>
          <div class="tl-title">📉 증권앱 접속 빈도 급감 + 알림 OFF</div>
          <div class="tl-desc">토스증권/키움증권 일일 접속 70%+ 감소 → 매도 후 관심 끊은 시그널</div>
          <div class="tl-flow">
            <div class="tl-flow-down">
              <div style="font-size:0.65rem;color:#999">증권앱</div>
              <div style="font-size:0.85rem;font-weight:800;color:#ef4444">↓ 70%</div>
            </div>
            <div style="color:#ccc">→</div>
            <div class="tl-flow-up">
              <div style="font-size:0.65rem;color:#999">뉴스앱</div>
              <div style="font-size:0.85rem;font-weight:800;color:#eab308">↑ 2배</div>
            </div>
          </div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-green" style="background:#eab308;box-shadow:0 0 0 2px #eab308"></div>
          <div class="tl-day" style="color:#eab308">DAY 3~5 · 금 투자 진입</div>
          <div class="tl-title">🥇 금방 / 한국금거래소 앱 신규 설치</div>
          <div class="tl-desc">증권앱 이탈 후 3~5일 내 금 투자앱 설치 → 자산 재배치 시그널</div>
          <div class="tl-bar-wrap" style="background:#fefce8">
            <div style="font-size:0.7rem;color:#888;margin-bottom:4px">금 투자앱 신규 설치 속도</div>
            <div class="tl-bar-bg"><div class="tl-bar-fill" style="width:82%;background:#eab308"></div></div>
            <div style="font-size:0.68rem;color:#eab308;font-weight:700;margin-top:2px">82% — 증권앱 이탈 후 5일 내 전환</div>
          </div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-yellow"></div>
          <div class="tl-day" style="color:#f59e0b">DAY 7~10 · 투자 루틴 전환</div>
          <div class="tl-title">🔄 금 투자앱 매일 실행 + 증권앱 미실행</div>
          <div class="tl-desc">기존 증권앱 대신 금 투자앱을 매일 여는 패턴 → 주력 투자처가 바뀐 시그널</div>
          <div class="tl-flow">
            <div class="tl-flow-down">
              <div style="font-size:0.65rem;color:#999">증권앱 실행</div>
              <div style="font-size:0.85rem;font-weight:800;color:#ef4444">주 0~1회</div>
            </div>
            <div style="color:#ccc">→</div>
            <div class="tl-flow-up">
              <div style="font-size:0.65rem;color:#999">금 투자앱 실행</div>
              <div style="font-size:0.85rem;font-weight:800;color:#eab308">매일</div>
            </div>
          </div>
        </div>
        <div class="tl-item" style="margin-bottom:0">
          <div class="tl-dot tl-red"></div>
          <div class="tl-alert">
            <div style="font-size:0.68rem;color:#ef4444;font-weight:700;margin-bottom:4px">⚡ DAY 14 · 여기서 잡아야 합니다</div>
            <div class="tl-title">금 ETF 추가 매수 / 실물 금 구매 / 달러 자산 재배치</div>
            <div class="tl-desc">미장 이탈 후 2주 내 금 투자 확대. 이 시점에 금 관련 상품 광고 전환율 4배+</div>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <p>핵심은 <strong>"증권앱 이탈 + 금 투자앱 진입"의 교차 시그널</strong>입니다.</p>
      <p>금에 관심 있는 사람은 많습니다. 하지만 <strong>미국주식을 실제로 팔고 나온 사람</strong>은 다릅니다. 이 사람은 이미 현금을 들고 있고, 다음 투자처를 찾고 있습니다.</p>
      <p>증권사가 "미국주식 추천" 푸시를 보내면 알림을 끕니다. 하지만 "금 ETF 수수료 0%" 광고를 보면 <strong>바로 클릭합니다.</strong></p>
    </div>

    <div class="section">
      <div class="cmp-grid">
        <div class="cmp-card cmp-left"><h4>주식 구경꾼</h4><p>증권앱 유지, 가끔 접속<br>뉴스 소비 변화 없음<br>금 투자앱 미설치<br>매도 이력 없음<br>"언젠가" 금 사볼까</p></div>
        <div class="cmp-card cmp-right"><h4>미장→금 전환자</h4><p>증권앱 접속 70%+ 감소<br>뉴스앱 관세/환율 집중<br>금 투자앱 5일 내 설치<br>매일 아침 금 시세 확인<br>현금 보유 → 즉시 매수</p></div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">DMP에서 잡는 법</div>
      <p><strong>[미장→금 전환자]</strong><br>증권앱 접속 빈도 70%+ 감소 (14일 내)<br>+ 뉴스앱 접속 빈도 2배+ 증가<br>+ 금 투자앱(금방/한국금거래소) 신규 설치<br>+ 금 투자앱 일일 실행 + 증권앱 미실행 패턴<br><br><em style="color:#888;font-size:0.8rem">* 실제 매도/매수 금액은 DMP로 확인 불가.<br>앱 실행 빈도의 역전(증권↓ 금↑)으로 자산 이동을 추정합니다.</em></p>
    </div>

    <div class="section">
      <div class="ind-grid">
        <div class="ind-card"><div class="ind-title">🥇 금 투자 플랫폼</div><div class="ind-desc">"미장 불안할 때, 금 ETF 수수료 0%"</div></div>
        <div class="ind-card"><div class="ind-title">🏦 증권사</div><div class="ind-desc">"금 ETF/금 현물 원클릭 매수"</div></div>
        <div class="ind-card"><div class="ind-title">💰 자산관리</div><div class="ind-desc">"포트폴리오 리밸런싱 무료 진단"</div></div>
        <div class="ind-card"><div class="ind-title">📊 로보어드바이저</div><div class="ind-desc">"관세 시대 안전자산 자동 배분"</div></div>
      </div>
    </div>

    <div class="insight-box">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"투자 관심자"는 오디언스가 아닙니다.<br><br><strong>증권앱 알림을 끈 사람</strong>이 오디언스입니다.<br>이 사람은 투자를 그만둔 게 아니라<br><strong>투자 방향을 바꾼 겁니다.</strong><br><br>"미국주식 추천"을 보내지 마세요.<br>"금 ETF 수수료 0%"를 보내세요.</p>
    </div>

    <div class="ad-compare">
      <p style="font-size:0.85rem;font-weight:700;color:#111;margin-bottom:16px">이 오디언스에게 보내는 광고</p>
      <p style="font-size:0.85rem;color:#999;margin-bottom:8px">❌ "미국주식 지금이 매수 타이밍! 수수료 무료"</p>
      <p style="font-size:0.85rem;color:#111;font-weight:600">✅ "미장 팔고 뭐 살지 고민 중이라면, 금 ETF 수수료 0%"</p>
    </div>

    <div class="audience-card">
      <p style="font-size:0.68rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:20px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.15rem;font-weight:800;margin-bottom:20px">미장→금 전환 투자자</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추정 모수</p><p style="color:#eab308;font-size:1.5rem;font-weight:900">~97만</p><p style="color:#555;font-size:0.7rem">증권/투자앱 (DMP 30일)</p></div>
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추천 업종</p><p style="color:#fff;font-size:0.88rem;font-weight:600;line-height:1.6">금 투자 · 증권사<br>자산관리 · 로보어드</p></div>
      </div>
    </div>

    <div class="footer">오늘의 오디언스 #7 · by IGAWorks</div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view == "detail_travel":
    if st.button("← 뒤로", key="back_t"):
        st.session_state.view = "feed"
        st.rerun()
    st.markdown("""
    <div class="detail-wrap">
    <div class="detail-hero">
      <div class="detail-emoji">✈️</div>
      <span class="detail-tag">여행</span>
      <div class="detail-title">해외여행 앱을 지우고 국내 펜션앱을 깐 사람</div>
      <div class="detail-sub">환율 1,450원 시대, 여행을 포기한 게 아니라 방향을 바꾼 겁니다</div>
      <div class="detail-meta">2026.04.14 · 오늘의 오디언스 #5</div>
    </div>

    <div class="quote-box">
      <p>"저는 원래 1년에 해외여행 2번은 갔어요.<br>근데 올해는 환율 보고 바로 제주도로 바꿨어요.<br>비행기값이면 제주에서 3박 하거든요."<br><br>— A씨, 32세, 마케팅 회사 재직</p>
    </div>

    <div class="section">
      <p>2026년 4월, 원/달러 환율이 1,450원을 넘었습니다.</p>
      <p>고환율에 유가까지 오르면서 여행자보험 계약이 감소하고 있다는 보도가 나왔습니다. 해외여행 수요가 줄고 있다는 신호.</p>
      <p>하지만 <strong>여행을 포기한 게 아닙니다.</strong></p>
      <p>A씨처럼 <strong>방향을 바꾼 겁니다.</strong> 해외 → 국내로. 호텔 → 펜션으로. 패키지 → 자유여행으로.</p>
      <p>여행 업계 마케터들은 아직 이 변화를 못 잡고 있습니다. "여행 관심자"로 타겟하면 여전히 해외여행 검색자와 국내전환자가 섞입니다.</p>
    </div>

    <div class="quote-box">
      <p>"해외여행 앱은 삭제했는데, 야놀자랑 여기어때는 매일 봐요.<br>주말마다 근교 가성비 숙소 찾고 있거든요.<br>돈을 안 쓰는 게 아니라, 쓰는 방식이 바뀐 거예요."<br><br>— A씨</p>
    </div>

    <div class="section">
      <div class="section-label">APP FLOW — 앱 사용 전환 맵</div>
      <p style="font-size:0.78rem;color:#999;margin-bottom:20px">A씨의 앱 사용이 어떻게 바뀌었는지 DMP로 보면</p>

      <div style="margin-bottom:20px">
        <div style="font-size:0.72rem;font-weight:700;color:#ef4444;margin-bottom:10px">✕ 삭제 / 미사용</div>
        <div class="af-row"><div class="af-gone">✈️ 스카이스캐너</div><div style="color:#ccc">→</div><div class="af-new">🏨 야놀자</div></div>
        <div class="af-row"><div class="af-gone">✈️ 트립닷컴</div><div style="color:#ccc">→</div><div class="af-new">🏨 여기어때</div></div>
        <div class="af-row"><div class="af-gone">✈️ 아고다</div><div style="color:#ccc">→</div><div class="af-new">🍽️ 캐치테이블</div></div>
      </div>

      <div style="margin-bottom:20px">
        <div style="font-size:0.72rem;font-weight:700;color:#14b8a6;margin-bottom:10px">↑ 사용 급증</div>
        <div class="af-row"><div class="af-up">🗺️ 네이버지도 주말 3배↑</div></div>
        <div class="af-row"><div class="af-up">🚗 티맵 주말 사용 신규</div></div>
        <div class="af-row"><div class="af-up">📸 인스타그램 #국내여행 탐색</div></div>
      </div>

      <div class="tl-bar-wrap">
        <div style="font-size:0.7rem;color:#888;margin-bottom:4px">해외여행 앱 사용 감소율</div>
        <div class="tl-bar-bg"><div class="tl-bar-fill" style="width:85%;background:#ef4444"></div></div>
        <div style="font-size:0.68rem;color:#ef4444;font-weight:700;margin-top:2px">-85% — 30일 내 거의 미사용</div>
      </div>
    </div>

    <div class="section">
      <p>핵심은 <strong>"앱 삭제 + 앱 설치"의 교차 시그널</strong>입니다.</p>
      <p>해외여행 앱을 지우는 건 단순히 안 가겠다는 게 아닙니다. <strong>예산을 국내로 돌렸다</strong>는 뜻입니다.</p>
      <p>이 사람들은 돈을 안 쓰는 게 아닙니다. <strong>오히려 국내에서 더 자주, 더 많이 씁니다.</strong> 해외여행 1번 갈 돈으로 국내여행 3~4번을 갑니다. 객단가는 낮지만 빈도가 높습니다.</p>
    </div>

    <div class="section">
      <div class="cmp-grid">
        <div class="cmp-card cmp-left"><h4>여행 구경꾼</h4><p>해외여행 앱 유지<br>숙박앱 가끔 접속<br>"언젠가" 가려는 사람<br>검색만 하고 예약 안 함<br>전환 가능성 낮음</p></div>
        <div class="cmp-card cmp-right"><h4>국내전환 여행자</h4><p>해외앱 삭제/미사용<br>국내 숙박앱 매일 접속<br>주말마다 실제 이동<br>숙박+맛집+네비 동시 사용<br>월 2~3회 실제 지출</p></div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">DMP에서 잡는 법</div>
      <p><strong>[국내전환 여행자]</strong><br>해외여행 앱 사용 80%+ 감소 (30일 내)<br>+ 국내 숙박앱 사용 빈도 2배+ 증가<br>+ 주말 네비앱 사용 급증<br>+ 맛집/카페앱 동시 활성<br><br><em style="color:#888;font-size:0.8rem">* 실제 예약/결제 여부는 DMP로 확인 불가.<br>앱 사용 패턴의 교차(해외↓ 국내↑)와 주말 이동 패턴으로 추정합니다.</em></p>
    </div>

    <div class="section">
      <div class="ind-grid">
        <div class="ind-card"><div class="ind-title">🏨 국내 숙박</div><div class="ind-desc">"이번 주말, 2시간 거리 가성비 펜션"</div></div>
        <div class="ind-card"><div class="ind-title">🚗 렌터카/주유</div><div class="ind-desc">"근교 드라이브 코스 + 주유 할인"</div></div>
        <div class="ind-card"><div class="ind-title">🍽️ 지역 맛집/카페</div><div class="ind-desc">"현지인만 아는 숨은 맛집 코스"</div></div>
        <div class="ind-card"><div class="ind-title">🎫 액티비티/체험</div><div class="ind-desc">"서핑/도예/와이너리 당일 체험"</div></div>
      </div>
    </div>

    <div class="insight-box">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"여행 관심자"는 오디언스가 아닙니다.<br><br>해외여행 앱을 <strong>지운 사람</strong>이 오디언스입니다.<br>이 사람은 여행을 포기한 게 아니라<br><strong>돈 쓰는 방향을 바꾼 겁니다.</strong><br><br>해외 1회 → 국내 3~4회.<br>객단가는 낮지만, 빈도와 총 지출은 더 높습니다.</p>
    </div>

    <div class="ad-compare">
      <p style="font-size:0.85rem;font-weight:700;color:#111;margin-bottom:16px">이 오디언스에게 보내는 광고</p>
      <p style="font-size:0.85rem;color:#999;margin-bottom:8px">❌ "올 여름 해외여행 특가! 방콕 3박 59만원~"</p>
      <p style="font-size:0.85rem;color:#111;font-weight:600">✅ "이번 주말, 차로 2시간. 해외 안 부러운 감성 펜션"</p>
    </div>

    <div class="audience-card">
      <p style="font-size:0.68rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:20px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.15rem;font-weight:800;margin-bottom:20px">국내전환 여행자</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추정 모수</p><p style="color:#6366f1;font-size:1.5rem;font-weight:900">~65만</p><p style="color:#555;font-size:0.7rem">여행+항공+호텔앱 (DMP 30일)</p></div>
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추천 업종</p><p style="color:#fff;font-size:0.88rem;font-weight:600;line-height:1.6">숙박 · 렌터카<br>맛집 · 액티비티</p></div>
      </div>
    </div>

    <div class="footer">오늘의 오디언스 #5 · by IGAWorks</div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view == "detail_golf":
    if st.button("← 뒤로", key="back_g"):
        st.session_state.view = "feed"
        st.rerun()
    st.markdown("""
    <div class="detail-wrap">
    <div class="detail-hero">
      <div class="detail-emoji">⛳</div>
      <span class="detail-tag">골프</span>
      <div class="detail-title">드라이버를 사는 게 아니라 창피를 안 당할 보험을 삽니다</div>
      <div class="detail-sub">접대 골프 입문자는 고민하지 않습니다. 빠르게 삽니다.</div>
      <div class="detail-meta">2026.04.11 · 오늘의 오디언스 #1</div>
    </div>

    <div class="quote-box">
      <p>"부장님이 다음 달 라운딩 가자고 했어요.<br>골프 한 번도 안 쳐봤는데.<br>그날 밤에 골프존 앱 깔고, 레슨 앱 깔고,<br>드라이버 가격 검색하고... 새벽 2시까지 했어요."<br><br>— B씨, 34세, 대기업 영업팀</p>
    </div>

    <div class="section">
      <p>골프 인구 564만 시대. 모든 골프 브랜드가 "골프 관심자"를 타겟합니다.</p>
      <p>문제는 10년 경력 싱글 골퍼부터 유튜브만 보는 구경꾼까지 전부 섞인다는 것.</p>
      <p>B씨는 다릅니다. <strong>골프가 좋아서 시작한 게 아닙니다. 회사 때문에 시작한 겁니다.</strong></p>
    </div>

    <div class="quote-box">
      <p>"드라이버 뭐가 좋은지 모르겠어요.<br>그냥 '이거 사면 창피는 안 당하겠다' 싶은 걸 샀어요.<br>가격은 안 봤어요. 다음 주까지 준비해야 하니까."<br><br>— B씨</p>
    </div>

    <div class="section">
      <div class="section-label">BEHAVIOR TIMELINE</div>
      <p style="font-size:0.78rem;color:#999;margin-bottom:20px">B씨의 앱 사용 변화를 DMP로 추적하면 이렇게 보입니다</p>
      <div class="tl">
        <div class="tl-item">
          <div class="tl-dot tl-green"></div>
          <div class="tl-day" style="color:#16a34a">DAY 0 · 부장님의 한마디</div>
          <div class="tl-title">⛳ 골프존 앱 첫 설치</div>
          <div class="tl-desc">90일간 골프앱 사용 이력 없음 → 완전 신규. 기존 골퍼와 구분되는 핵심 시그널</div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-green"></div>
          <div class="tl-day" style="color:#16a34a">DAY 0~1 · 그날 밤</div>
          <div class="tl-title">🏌️ 레슨앱 + 스마트스코어 추가 설치</div>
          <div class="tl-desc">24시간 내 골프앱 3개 동시 설치 → "빨리 배워야 한다"는 긴급도</div>
          <div class="tl-bar-wrap">
            <div style="font-size:0.7rem;color:#888;margin-bottom:4px">24시간 내 동시 설치 속도</div>
            <div class="tl-bar-bg"><div class="tl-bar-fill" style="width:95%;background:#16a34a"></div></div>
            <div style="font-size:0.68rem;color:#16a34a;font-weight:700;margin-top:2px">상위 3% — 일반 입문자 대비 5배 빠름</div>
          </div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-green"></div>
          <div class="tl-day" style="color:#16a34a">DAY 2~5 · 평일 저녁 집중</div>
          <div class="tl-title">🌙 19~23시 골프 콘텐츠 소비</div>
          <div class="tl-desc">주말이 아닌 평일 저녁 → 퇴근 후 급하게 준비하는 직장인 패턴</div>
          <div class="tl-flow">
            <div class="tl-flow-up" style="background:#f0fdf4">
              <div style="font-size:0.65rem;color:#999">기기 가격대</div>
              <div style="font-size:0.85rem;font-weight:800;color:#16a34a">상위 30%</div>
            </div>
            <div style="color:#ccc">+</div>
            <div class="tl-flow-up" style="background:#f0fdf4">
              <div style="font-size:0.65rem;color:#999">사용 시간대</div>
              <div style="font-size:0.85rem;font-weight:800;color:#16a34a">평일 저녁</div>
            </div>
          </div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-yellow"></div>
          <div class="tl-day" style="color:#f59e0b">DAY 3~7 · 💰 지출 시작</div>
          <div class="tl-title">🛒 골프웨어/용품 쇼핑앱 탐색</div>
          <div class="tl-desc">무신사/크림에서 골프웨어 탐색 → 장비+옷+레슨 한꺼번에 준비</div>
        </div>
        <div class="tl-item" style="margin-bottom:0">
          <div class="tl-dot tl-red"></div>
          <div class="tl-alert">
            <div style="font-size:0.68rem;color:#ef4444;font-weight:700;margin-bottom:4px">⚡ DAY 7 · 여기서 잡아야 합니다</div>
            <div class="tl-title">풀세트 구매 / 레슨 등록 / 골프웨어 결제</div>
            <div class="tl-desc">접대 입문자는 평균 7일 내 첫 구매. 고민 없이 빠르게 삽니다. 객단가 150만원+</div>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <p>이 사람은 <strong>고민하지 않습니다. 빠르게 삽니다.</strong></p>
      <p>장비에 진심인 골퍼는 3개월 비교합니다. 접대 입문자는 3일 만에 풀세트를 삽니다. 객단가가 높고, 전환이 빠릅니다.</p>
    </div>

    <div class="section">
      <div class="cmp-grid">
        <div class="cmp-card cmp-left"><h4>기존 골프 관심자</h4><p>장비에 진심, 3개월 비교<br>스코어에 집착<br>가성비 추구<br>주말 라운딩 중심<br>천천히 구매</p></div>
        <div class="cmp-card cmp-right"><h4>접대 골프 입문자</h4><p>창피 안 당할 정도면 됨<br>매너와 에티켓이 급함<br>무난하게 좋은 걸 원함<br>평일 라운딩 비중 높음<br>3일 만에 풀세트 구매</p></div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">DMP에서 잡는 법</div>
      <p><strong>[접대 골프 입문자]</strong><br>골프앱 첫 설치 (90일 내 이력 없음)<br>+ 3일 내 레슨앱 추가 설치<br>+ 평일 저녁 집중 사용<br>+ 기기 가격대 상위 30%<br>+ 골프웨어 쇼핑앱 동시 활성</p>
    </div>

    <div class="section">
      <div class="ind-grid">
        <div class="ind-card"><div class="ind-title">⛳ 골프 용품</div><div class="ind-desc">"다음 주 라운딩 전에 이것만 준비하세요"</div></div>
        <div class="ind-card"><div class="ind-title">👔 골프웨어</div><div class="ind-desc">"접대 라운딩, 이 옷이면 됩니다"</div></div>
        <div class="ind-card"><div class="ind-title">🏌️ 골프 레슨</div><div class="ind-desc">"4주 만에 필드 나가기" 속성 레슨</div></div>
        <div class="ind-card"><div class="ind-title">💳 프리미엄 카드</div><div class="ind-desc">골프장 할인 + 라운지 혜택</div></div>
      </div>
    </div>

    <div class="insight-box">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"골프 관심자"는 오디언스가 아닙니다.<br><br><strong>왜 골프를 시작했는지</strong>가 오디언스를 만듭니다.<br>접대 입문자는 고민하지 않습니다.<br>빠르게 삽니다. 비싸게 삽니다.</p>
    </div>

    <div class="ad-compare">
      <p style="font-size:0.85rem;font-weight:700;color:#111;margin-bottom:16px">이 오디언스에게 보내는 광고</p>
      <p style="font-size:0.85rem;color:#999;margin-bottom:8px">❌ "골프 시작하셨나요? 입문자 추천 클럽 보기"</p>
      <p style="font-size:0.85rem;color:#111;font-weight:600">✅ "다음 주 라운딩, 창피 안 당하려면 이것만 준비하세요"</p>
    </div>

    <div class="audience-card">
      <p style="font-size:0.68rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:20px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.15rem;font-weight:800;margin-bottom:20px">접대 골프 입문자</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추정 모수</p><p style="color:#6366f1;font-size:1.5rem;font-weight:900">~17만</p><p style="color:#555;font-size:0.7rem">골프앱 사용자 (DMP 30일)</p></div>
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추천 업종</p><p style="color:#fff;font-size:0.88rem;font-weight:600;line-height:1.6">골프 용품 · 골프웨어<br>레슨 · 프리미엄 카드</p></div>
      </div>
    </div>

    <div class="footer">오늘의 오디언스 #1 · by IGAWorks</div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view == "detail_finance":
    if st.button("← 뒤로", key="back_f"):
        st.session_state.view = "feed"
        st.rerun()
    st.markdown("""
    <div class="detail-wrap">
    <div class="detail-hero">
      <div class="detail-emoji">💰</div>
      <span class="detail-tag">금융</span>
      <div class="detail-title">대출앱 3개를 동시에 깐 사람의 비밀</div>
      <div class="detail-sub">불 난 사람한테 소화기 할인 쿠폰을 보내지 마세요</div>
      <div class="detail-meta">2026.04.10 · 오늘의 오디언스 #2</div>
    </div>

    <div class="quote-box">
      <p>"불이 났는데<br>소화기 할인 쿠폰을 보내고 있는 격이죠."<br><br>— K씨, 시중은행 전세대출 담당 마케터</p>
    </div>

    <div class="section">
      <p>4월 1일, 금융위원회가 가계대출 종합 대책을 발표했습니다.</p>
      <p>→ 가계대출 연간 성장률 상한 <strong>1.5%</strong>로 하향<br>→ 다주택자 주담대 만기 연장 <strong>4월 17일부터 금지</strong><br>→ 비거주 1주택자 전세대출 보증 <strong>제한 검토 중</strong></p>
      <p>규제가 만든 건 <strong>데드라인</strong>입니다. 4월 17일이 지나면 다주택자는 만기 연장이 안 됩니다.</p>
      <p><strong>이 사람들은 "관심"이 아니라 "생존"으로 움직이고 있습니다.</strong></p>
    </div>

    <div class="quote-box">
      <p>"뉴스 보고 바로 뱅크샐러드 깔았어요.<br>다음 날 핀다도 깔고, 토스 대출 탭도 매일 확인하고.<br>새벽에 눈 떠서 금리 비교하다 출근해요.<br>4월 17일 전에 안 하면 진짜 끝이거든요."<br><br>— C씨, 38세, 1주택 전세 거주자</p>
    </div>
    </div>

    <div class="section">
      <div class="section-label">BEHAVIOR COUNTDOWN</div>
      <p style="font-size:0.78rem;color:#999;margin-bottom:20px">C씨의 규제 발표 후 행동 변화 — 데드라인이 만든 시그널</p>
      <div class="cd-item cd-info">
        <div class="cd-day" style="color:#6366f1">D-17 · 규제 발표 당일 (4/1)</div>
        <div class="tl-title">📱 뱅크샐러드 + 핀다 동시 설치</div>
        <div class="tl-desc">뉴스 확인 직후 대출 비교앱 2개 설치 → 규제에 직접 영향받는 사람</div>
      </div>
      <div class="cd-item cd-info">
        <div class="cd-day" style="color:#6366f1">D-14 · 탐색 시작</div>
        <div class="tl-title">📊 매일 2회+ 접속, 새벽 시간대 활성</div>
        <div class="tl-desc">23시~02시 대출앱 사용 → 급해서 잠 못 자는 사람</div>
        <div class="tl-bar-wrap" style="background:#f0eeff">
          <div style="font-size:0.7rem;color:#888;margin-bottom:4px">뉴스앱 접속 빈도 변화</div>
          <div class="tl-bar-bg"><div class="tl-bar-fill" style="width:75%;background:#6366f1"></div></div>
          <div style="font-size:0.68rem;color:#6366f1;font-weight:700;margin-top:2px">+50% 증가 — 규제 뉴스 집중 소비</div>
        </div>
      </div>
      <div class="cd-item cd-warn">
        <div class="cd-day" style="color:#f59e0b">D-7 · 기존 은행 이탈 시작</div>
        <div class="tl-title">🏦 주거래 은행앱 사용 빈도 급감</div>
        <div class="tl-desc">기존 은행앱 접속 30%+ 감소 → 떠나려는 이탈 시그널</div>
        <div class="tl-flow">
          <div class="tl-flow-down">
            <div style="font-size:0.65rem;color:#999">기존 은행앱</div>
            <div style="font-size:0.85rem;font-weight:800;color:#ef4444">↓ 30%</div>
          </div>
          <div style="color:#ccc">→</div>
          <div class="tl-flow-up">
            <div style="font-size:0.65rem;color:#999">비교앱</div>
            <div style="font-size:0.85rem;font-weight:800;color:#6366f1">매일 접속</div>
          </div>
        </div>
      </div>
      <div class="cd-item cd-urgent">
        <div class="cd-day" style="color:#ef4444">⚡ D-3 · 여기서 잡아야 합니다</div>
        <div class="tl-title">대환 신청 / 전세보증보험 가입 / 매매 전환 검토</div>
        <div class="tl-desc">4/17 이후 만기 연장 불가. 이 유저 1명의 가치는 평소의 3~5배.</div>
      </div>
    </div>

    <div class="section">
      <p>핵심은 <strong>"동시에 여러 앱을 까는 속도"</strong>입니다.</p>
      <p>금리 비교하는 사람은 앱을 하나 깔고 천천히 봅니다.<br>규제 전에 움직이는 사람은 <strong>대출앱 + 부동산앱 + 뉴스앱을 동시에 깝니다.</strong></p>
      <p>이 사람들에게 광고는 방해가 아닙니다. <strong>지금 당장 필요한 정보</strong>입니다. 전환율이 평소의 3~5배.</p>
    </div>

    <div class="section">
      <div class="cmp-grid">
        <div class="cmp-card cmp-left"><h4>대출 구경꾼</h4><p>부동산앱만 활성 증가<br>대출앱 미설치<br>뉴스 소비 평소와 비슷<br>30일+ 관찰 기간<br>전환 가능성 낮음</p></div>
        <div class="cmp-card cmp-right"><h4>규제 전 급히 움직이는 사람</h4><p>대출앱 2개+ 동시 설치<br>부동산앱 활성 급증<br>뉴스앱 접속 50%+ 증가<br>14일 내 집중 행동<br>전환 가능성 극상</p></div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">DMP에서 잡는 법</div>
      <p><strong>[규제 전 급히 움직이는 사람]</strong><br>대출 카테고리 앱 + 뱅크샐러드 사용자<br>+ 은행앱 동시 사용 (갈아타기 비교 행동)<br><br><em style="color:#888;font-size:0.8rem">* DMP 실측: 대출앱+뱅크샐러드 사용자 약 10.6만명 (30일 기준)</em></p>
    </div>

    <div class="section">
      <div class="ind-grid">
        <div class="ind-card"><div class="ind-title">🏦 은행/저축은행</div><div class="ind-desc">"4/17 전 대환 신청" 긴급 캠페인</div></div>
        <div class="ind-card"><div class="ind-title">📱 핀테크</div><div class="ind-desc">"내 전세대출 규제 영향 확인" 유도</div></div>
        <div class="ind-card"><div class="ind-title">🏠 부동산 플랫폼</div><div class="ind-desc">전세→매매 전환 매물 추천</div></div>
        <div class="ind-card"><div class="ind-title">🛡️ 보험</div><div class="ind-desc">전세보증보험 긴급 가입 타겟팅</div></div>
      </div>
    </div>

    <div class="insight-box">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"대출 관심자"는 오디언스가 아닙니다.<br><br>규제가 만든 건 <strong>데드라인</strong>입니다.<br><strong>대출앱 2개를 동시에 까는 속도</strong>가 오디언스를 만듭니다.<br><br>불 난 사람한테 소화기 할인 쿠폰을 보내지 마세요.<br>소화기를 들고 달려가세요.</p>
    </div>

    <div class="ad-compare">
      <p style="font-size:0.85rem;font-weight:700;color:#111;margin-bottom:16px">이 오디언스에게 보내는 광고</p>
      <p style="font-size:0.85rem;color:#999;margin-bottom:8px">❌ "전세대출 금리 비교, 최저 연 3.2%~"</p>
      <p style="font-size:0.85rem;color:#111;font-weight:600">✅ "4월 17일 전에 대환 신청하세요. 이후엔 만기 연장이 안 됩니다"</p>
    </div>

    <div class="audience-card">
      <p style="font-size:0.68rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:20px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.15rem;font-weight:800;margin-bottom:20px">규제 전 급히 움직이는 유저</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추정 모수 (DMP 실측)</p><p style="color:#6366f1;font-size:1.5rem;font-weight:900">~10만</p><p style="color:#555;font-size:0.7rem">대출앱+뱅크샐러드 사용자</p></div>
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추천 업종</p><p style="color:#fff;font-size:0.88rem;font-weight:600;line-height:1.6">은행 · 핀테크<br>부동산 · 보험</p></div>
      </div>
    </div>

    <div class="footer">오늘의 오디언스 #2 · by IGAWorks</div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view == "detail_health":
    if st.button("← 뒤로", key="back_h"):
        st.session_state.view = "feed"
        st.rerun()
    st.markdown("""
    <div class="detail-wrap">
    <div class="detail-hero">
      <div class="detail-emoji">💪</div>
      <span class="detail-tag">건강</span>
      <div class="detail-title">러닝앱 깔고 3일 만에 식단앱까지 깐 사람</div>
      <div class="detail-sub">다이어트를 결심한 게 아니라, 몸이 바뀌기 시작한 겁니다</div>
      <div class="detail-meta">2026.04.14 · 오늘의 오디언스 #6</div>
    </div>

    <div class="quote-box">
      <p>"건강검진 결과 보고 충격받았어요.<br>그날 바로 나이키런클럽 깔고 다음 날 새벽에 뛰었어요.<br>3일 뒤에 식단 앱 깔고, 일주일 뒤에 PT 등록했어요.<br>지금 한 달째 매일 기록하고 있어요."<br><br>— D씨, 36세, IT 회사 PM</p>
    </div>

    <div class="section">
      <p>건강기능식품 시장 6조 원. 홈트레이닝 시장 2조 원. 다이어트 앱 MAU 800만.</p>
      <p>모든 헬스 브랜드가 "건강 관심자"를 타겟합니다. 문제는 유튜브에서 운동 영상만 보는 사람과, 실제로 몸을 바꾸고 있는 사람이 섞인다는 것.</p>
      <p>D씨는 다릅니다. <strong>관심이 아니라 행동이 바뀐 사람입니다.</strong></p>
    </div>

    <div class="quote-box">
      <p>"예전에도 다이어트 앱 깔아본 적 있어요.<br>근데 3일 만에 삭제했죠.<br>이번엔 달라요. 러닝 → 식단 → PT까지 일주일 만에 다 깔았어요.<br>매일 아침 6시에 알람 맞춰놓고 뛰고 있어요."<br><br>— D씨</p>
    </div>

    <div class="section">
      <div class="section-label">BEHAVIOR TIMELINE</div>
      <p style="font-size:0.78rem;color:#999;margin-bottom:20px">D씨의 실제 앱 사용 변화를 DMP로 추적하면 이렇게 보입니다</p>
      <div class="tl">
        <div class="tl-item">
          <div class="tl-dot tl-green"></div>
          <div class="tl-day" style="color:#14b8a6">DAY 0 · 건강검진 직후</div>
          <div class="tl-title">🏃 나이키런클럽 설치</div>
          <div class="tl-desc">90일간 운동앱 사용 이력 없음 → 완전 신규 진입</div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-green"></div>
          <div class="tl-day" style="color:#14b8a6">DAY 1~7 · 습관 형성</div>
          <div class="tl-title">⏰ 새벽 5~6시 앱 실행 시작</div>
          <div class="tl-desc">기존에 없던 새벽 패턴 → 생활 루틴 자체가 바뀐 시그널</div>
          <div class="tl-bar-wrap">
            <div style="font-size:0.7rem;color:#888;margin-bottom:4px">7일 연속 실행률</div>
            <div class="tl-bar-bg"><div class="tl-bar-fill" style="width:92%"></div></div>
            <div style="font-size:0.68rem;color:#14b8a6;font-weight:700;margin-top:2px">92% — 상위 5% 지속률</div>
          </div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-green"></div>
          <div class="tl-day" style="color:#14b8a6">DAY 3 · 식단 전환</div>
          <div class="tl-title">🥗 식단 관리앱 추가 설치</div>
          <div class="tl-desc">운동 → 식단 3일 만에 전환 = 진지한 행동 변화</div>
          <div class="tl-flow">
            <div class="tl-flow-down">
              <div style="font-size:0.65rem;color:#999">배달앱</div>
              <div style="font-size:0.85rem;font-weight:800;color:#ef4444">↓ 60%</div>
            </div>
            <div style="color:#ccc">→</div>
            <div class="tl-flow-up">
              <div style="font-size:0.65rem;color:#999">식단앱</div>
              <div style="font-size:0.85rem;font-weight:800;color:#14b8a6">매일 기록</div>
            </div>
          </div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-yellow"></div>
          <div class="tl-day" style="color:#f59e0b">DAY 10~14 · 💰 지출 시작</div>
          <div class="tl-title">🛒 프로틴/보충제 쇼핑 탐색</div>
          <div class="tl-desc">쿠팡/아이허브에서 프로틴 검색 → 지출 준비 완료</div>
        </div>
        <div class="tl-item" style="margin-bottom:0">
          <div class="tl-dot tl-red"></div>
          <div class="tl-alert">
            <div style="font-size:0.68rem;color:#ef4444;font-weight:700;margin-bottom:4px">⚡ DAY 14 · 여기서 잡아야 합니다</div>
            <div class="tl-title">PT 등록 / 러닝화 구매 / 구독 전환</div>
            <div class="tl-desc">2주 지속한 사람은 3개월 유지 확률 78%. 이 타이밍을 놓치면 습관이 꺾입니다.</div>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <p>핵심은 <strong>"앱 설치 속도 + 생활 패턴 변화"</strong>의 조합입니다.</p>
      <p>다이어트 앱을 깔았다가 3일 만에 지우는 사람은 매년 수백만 명입니다. 이 사람들에게 광고해봤자 전환이 안 됩니다.</p>
      <p>하지만 러닝앱 깔고 <strong>7일 연속 실행</strong>하면서 <strong>식단앱까지 추가</strong>하고, <strong>배달앱 사용이 줄어든</strong> 사람? 이 사람은 진짜입니다. 프로틴, PT, 운동복, 러닝화 — <strong>전부 삽니다.</strong></p>
    </div>

    <div class="section">
      <div class="cmp-grid">
        <div class="cmp-card cmp-left"><h4>건강 콘텐츠 소비자</h4><p>운동 영상만 시청<br>앱 설치 후 3일 내 삭제<br>배달앱 사용 변화 없음<br>생활 패턴 그대로<br>전환 가능성 낮음</p></div>
        <div class="cmp-card cmp-right"><h4>행동 전환 유저</h4><p>러닝앱 7일 연속 실행<br>3일 내 식단앱 추가<br>배달앱 사용 급감<br>새벽 루틴 신규 발생<br>프로틴/PT 지출 준비</p></div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">DMP에서 잡는 법</div>
      <p><strong>[행동 전환 유저]</strong><br>러닝/운동앱 설치 후 7일 연속 실행<br>+ 3일 내 식단앱 추가 설치<br>+ 배달앱 사용 빈도 50%+ 감소<br>+ 아침 5~7시 신규 사용 패턴<br><br><em style="color:#888;font-size:0.8rem">* 실제 체중/건강 데이터는 DMP로 확인 불가.<br>앱 사용 지속성 + 생활 패턴 변화로 진지도를 추정합니다.</em></p>
    </div>

    <div class="section">
      <div class="ind-grid">
        <div class="ind-card"><div class="ind-title">🥤 프로틴/보충제</div><div class="ind-desc">"운동 시작 2주차, 지금이 프로틴 골든타임"</div></div>
        <div class="ind-card"><div class="ind-title">🏋️ PT/헬스장</div><div class="ind-desc">"혼자 뛰다 한계 느낄 때, 4주 PT"</div></div>
        <div class="ind-card"><div class="ind-title">👟 러닝화/운동복</div><div class="ind-desc">"매일 뛰는 사람을 위한 러닝화"</div></div>
        <div class="ind-card"><div class="ind-title">🥗 식단/밀키트</div><div class="ind-desc">"배달 끊은 당신을 위한 고단백 도시락"</div></div>
      </div>
    </div>

    <div class="insight-box">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"건강 관심자"는 오디언스가 아닙니다.<br><br>러닝앱 깔고 <strong>7일 연속 뛴 사람</strong>이 오디언스입니다.<br>이 사람은 다이어트를 결심한 게 아니라<br><strong>이미 몸이 바뀌기 시작한 겁니다.</strong><br><br>배달앱을 지우고 식단앱을 깐 사람한테<br>"살 빼세요" 광고를 보내지 마세요.<br>"지금 잘 하고 있어요"를 보내세요.</p>
    </div>

    <div class="ad-compare">
      <p style="font-size:0.85rem;font-weight:700;color:#111;margin-bottom:16px">이 오디언스에게 보내는 광고</p>
      <p style="font-size:0.85rem;color:#999;margin-bottom:8px">❌ "올 여름 다이어트! 지금 시작하세요"</p>
      <p style="font-size:0.85rem;color:#111;font-weight:600">✅ "2주째 매일 뛰고 있죠? 이제 프로틴 더할 타이밍입니다"</p>
    </div>

    <div class="audience-card">
      <p style="font-size:0.68rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:20px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.15rem;font-weight:800;margin-bottom:20px">행동 전환 유저</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추정 모수</p><p style="color:#6366f1;font-size:1.5rem;font-weight:900">~103만</p><p style="color:#555;font-size:0.7rem">운동+다이어트앱 (DMP 30일)</p></div>
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추천 업종</p><p style="color:#fff;font-size:0.88rem;font-weight:600;line-height:1.6">프로틴 · PT<br>러닝화 · 식단</p></div>
      </div>
    </div>

    <div class="footer">오늘의 오디언스 #6 · by IGAWorks</div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view == "detail_pet":
    if st.button("← 뒤로", key="back_p"):
        st.session_state.view = "feed"
        st.rerun()
    st.markdown("""
    <div class="detail-wrap">
    <div class="detail-hero">
      <div class="detail-emoji">🐾</div>
      <span class="detail-tag">반려동물</span>
      <div class="detail-title">'반려동물 관심자' 타겟팅 금지!</div>
      <div class="detail-sub">첫 입양 후 2주, 앱이 폭발하는 사람</div>
      <div class="detail-meta">2026.04.13 · 오늘의 오디언스 #4</div>
    </div>

    <div class="quote-box">
      <p>"첫 사료는 선택이 아니라 습관이에요.<br>처음 먹인 사료를 3년을 먹입니다.<br>그 2주를 놓치면, 3년을 놓치는 겁니다."</p>
    </div>

    <div class="section">
      <p>프리미엄 사료 브랜드 마케터 J씨의 말입니다.</p>
      <p>한국 반려동물 인구 1,546만 명. 591만 가구. 월 평균 지출 19만 4천 원.</p>
      <p>모든 펫 브랜드가 이 시장을 잡으려고 합니다. 문제는 <strong>"반려동물 관심자"로 타겟하면 대부분이 귀여운 동물 영상만 보는 사람</strong>이라는 것.</p>
    </div>

    <div class="section">
      <div class="section-label">BEHAVIOR TIMELINE</div>
      <p style="font-size:0.78rem;color:#999;margin-bottom:20px">첫 입양자의 앱 사용 변화 — 2주 골든타임</p>
      <div class="tl">
        <div class="tl-item">
          <div class="tl-dot tl-green" style="background:#f97316;box-shadow:0 0 0 2px #f97316"></div>
          <div class="tl-day" style="color:#f97316">DAY 0 · 입양 결심</div>
          <div class="tl-title">🐾 포인핸드(입양앱) 첫 설치</div>
          <div class="tl-desc">90일간 펫앱 사용 이력 없음 → 완전 신규 반려인 확인</div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-green" style="background:#f97316;box-shadow:0 0 0 2px #f97316"></div>
          <div class="tl-day" style="color:#f97316">DAY 1~3 · 앱 폭발</div>
          <div class="tl-title">📱 펫앱 3개+ 동시 설치</div>
          <div class="tl-desc">건강앱(펫닥) + 쇼핑앱(펫프렌즈) + 정보앱 → 모든 게 처음인 사람</div>
          <div class="tl-bar-wrap" style="background:#fff7ed">
            <div style="font-size:0.7rem;color:#888;margin-bottom:4px">3일 내 동시 설치 속도</div>
            <div class="tl-bar-bg"><div class="tl-bar-fill" style="width:88%;background:#f97316"></div></div>
            <div style="font-size:0.68rem;color:#f97316;font-weight:700;margin-top:2px">88% — 기존 반려인 대비 10배 빠른 설치</div>
          </div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-green" style="background:#f97316;box-shadow:0 0 0 2px #f97316"></div>
          <div class="tl-day" style="color:#f97316">DAY 3~7 · 불안 검색</div>
          <div class="tl-title">🌙 심야 11시~새벽 1시 펫앱 집중 사용</div>
          <div class="tl-desc">아이가 아파서, 밥을 안 먹어서 → 불안해서 밤에 검색하는 패턴</div>
        </div>
        <div class="tl-item">
          <div class="tl-dot tl-yellow"></div>
          <div class="tl-day" style="color:#f59e0b">DAY 7~10 · 💰 첫 지출</div>
          <div class="tl-title">🛒 사료/용품 쇼핑 시작</div>
          <div class="tl-desc">첫 사료 선택 → 이때 선택한 브랜드를 3년 유지. 선점이 핵심</div>
        </div>
        <div class="tl-item" style="margin-bottom:0">
          <div class="tl-dot tl-red"></div>
          <div class="tl-alert">
            <div style="font-size:0.68rem;color:#ef4444;font-weight:700;margin-bottom:4px">⚡ DAY 14 · 이 2주를 놓치면 3년을 놓칩니다</div>
            <div class="tl-title">사료 구독 / 펫보험 가입 / 동물병원 등록</div>
            <div class="tl-desc">첫 입양 2주 내 브랜드 선택 → 3년 고객 전환. 펫보험 가입률 12.8%지만 이 시기 가입자는 유지율 89%.</div>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <p>핵심은 <strong>"2주 안에 3개 이상 펫앱을 동시에 까는 속도"</strong>입니다.</p>
      <p>기존 반려인은 이미 쓰는 앱이 있어요. 새 앱을 잘 안 깝니다.<br>첫 입양자는 <strong>모든 게 처음</strong>이라 한꺼번에 깝니다.</p>
    </div>

    <div class="section">
      <div class="cmp-grid">
        <div class="cmp-card cmp-left"><h4>반려동물 콘텐츠 소비자</h4><p>펫앱 미설치<br>귀여운 영상만 소비<br>구매 의도 없음<br>광고 클릭 후 이탈<br>전환 가능성 낮음</p></div>
        <div class="cmp-card cmp-right"><h4>첫 입양 폭발기 유저</h4><p>2주 내 펫앱 3개+ 설치<br>건강앱+쇼핑앱 동시<br>하루 2회+ 실행<br>모든 카테고리 첫 구매<br>전환 가능성 극상</p></div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">DMP에서 잡는 법</div>
      <p><strong>[첫 입양 폭발기]</strong><br>입양앱(포인핸드) 첫 설치<br>+ 14일 내 펫앱 3개+ 동시 설치 (건강+쇼핑 필수)<br>+ 설치 후 7일간 하루 2회+ 실행<br>+ 최근 90일 펫앱 사용 이력 없음</p>
    </div>

    <div class="section">
      <div class="ind-grid">
        <div class="ind-card"><div class="ind-title">🍖 사료/간식</div><div class="ind-desc">"첫 달 무료 체험" 첫 사료 선점</div></div>
        <div class="ind-card"><div class="ind-title">🛡️ 펫보험</div><div class="ind-desc">"입양 첫 달 가입 시 30% 할인"</div></div>
        <div class="ind-card"><div class="ind-title">🏥 동물병원</div><div class="ind-desc">"첫 건강검진 무료" 신규 등록</div></div>
        <div class="ind-card"><div class="ind-title">🧸 용품/장난감</div><div class="ind-desc">"첫 입양 스타터 키트" 번들</div></div>
      </div>
    </div>

    <div class="insight-box">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"반려동물 관심자"는 오디언스가 아닙니다.<br><strong>첫 입양 후 2주</strong>가 오디언스를 만듭니다.<br>그 2주를 놓치면, 3년을 놓칩니다.</p>
    </div>

    <div class="ad-compare">
      <p style="font-size:0.85rem;font-weight:700;color:#111;margin-bottom:16px">이 오디언스에게 보내는 광고</p>
      <p style="font-size:0.85rem;color:#999;margin-bottom:8px">❌ "우리 아이에게 좋은 사료, 지금 할인 중!"</p>
      <p style="font-size:0.85rem;color:#111;font-weight:600">✅ "첫 달 사료 무료 체험. 우리 아이 첫 끼를 함께하세요"</p>
    </div>

    <div class="audience-card">
      <p style="font-size:0.68rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:20px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.15rem;font-weight:800;margin-bottom:20px">첫 입양 폭발기 유저</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추정 모수</p><p style="color:#6366f1;font-size:1.5rem;font-weight:900">~13만</p><p style="color:#555;font-size:0.7rem">펫앱+커머스 조회 (DMP 30일)</p></div>
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추천 업종</p><p style="color:#fff;font-size:0.88rem;font-weight:600;line-height:1.6">사료 · 펫보험<br>동물병원 · 용품</p></div>
      </div>
    </div>

    <div class="footer">오늘의 오디언스 #4 · by IGAWorks</div>
    </div>
    """, unsafe_allow_html=True)

else:
    # ===== FEED =====
    st.markdown("""
    <div style="padding:40px 0 32px">
      <p style="font-size:0.72rem;color:#6366f1;font-weight:700;letter-spacing:2px;margin-bottom:12px">AUDIENCE IDEA BANK</p>
      <h1 style="font-size:1.8rem;font-weight:900;color:#111;line-height:1.3;letter-spacing:-0.5px;margin-bottom:8px">다음 캠페인,<br>누구한테 해야 하지?</h1>
      <p style="color:#999;font-size:0.82rem;line-height:1.6">트렌드를 읽고, 행동 시그널을 조합해<br>아직 아무도 안 쓰는 오디언스를 제안합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    # Hero — 최신 에세이
    e = ESSAYS[0]
    st.markdown(f"""
    <p style="font-size:0.72rem;color:#6366f1;font-weight:700;letter-spacing:2px;margin-bottom:16px">🎯 오늘의 오디언스</p>
    """, unsafe_allow_html=True)
    if st.button(f"{e['emoji']}  {e['tag']}  ·  추정 {e['stat']}\n\n{e['title'].replace(chr(10), chr(10))}\n\n{e['sub']}\n\n자세히 보기 →", key=f"go_{e['id']}"):
        st.session_state.view = f"detail_{e['id']}"
        st.rerun()

    # Grid — 나머지
    st.markdown('<p style="font-size:0.72rem;color:#6366f1;font-weight:700;letter-spacing:2px;margin:32px 0 16px">📚 지난 오디언스</p>', unsafe_allow_html=True)
    cols_per_row = 3
    past = ESSAYS[1:]
    for row_start in range(0, len(past), cols_per_row):
        row = past[row_start:row_start + cols_per_row]
        cols = st.columns(len(row))
        for col, e in zip(cols, row):
            with col:
                label = f"{e['emoji']}\n{e['tag']}  ·  {e['stat']}\n\n{e['title'].replace(chr(10), chr(10))}\n\n{e['sub'][:40]}…"
                if st.button(label, key=f"go_{e['id']}"):
                    st.session_state.view = f"detail_{e['id']}"
                    st.rerun()

    st.markdown('<div class="footer">오늘의 오디언스 · by IGAWorks · © 2026</div>', unsafe_allow_html=True)
