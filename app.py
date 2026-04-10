import streamlit as st

st.set_page_config(page_title="오늘의 오디언스 — IGAWorks", page_icon="🎯", layout="wide")

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
.stApp { background:#0a0a0f; font-family:'Pretendard',sans-serif; }
header, .stDeployButton, #MainMenu, footer, [data-testid="stToolbar"] { display:none!important; }
.block-container { max-width:1200px!important; padding:40px 48px 80px!important; }

/* Hero */
.hero { text-align:center; padding:80px 0 60px; position:relative; }
.hero::before { content:''; position:absolute; top:-40px; left:50%; transform:translateX(-50%); width:600px; height:400px; background:radial-gradient(ellipse,rgba(99,102,241,0.12) 0%,transparent 70%); pointer-events:none; }
.hero-badge { display:inline-block; background:rgba(99,102,241,0.12); border:1px solid rgba(99,102,241,0.25); color:#a5b4fc; padding:8px 20px; border-radius:100px; font-size:0.82rem; letter-spacing:0.5px; margin-bottom:28px; }
.hero h1 { font-size:3.6rem; font-weight:900; color:#fff; line-height:1.15; margin-bottom:20px; letter-spacing:-1px; }
.hero h1 span { background:linear-gradient(135deg,#6366f1,#a78bfa,#f472b6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero-sub { color:#94a3b8; font-size:1.15rem; line-height:1.7; max-width:560px; margin:0 auto; }

/* Divider */
.section-div { border:none; border-top:1px solid rgba(255,255,255,0.06); margin:60px 0; }

/* Section */
.sec-label { font-size:0.75rem; color:#6366f1; letter-spacing:2px; text-transform:uppercase; font-weight:600; margin-bottom:10px; }
.sec-title { font-size:2rem; font-weight:800; color:#fff; margin-bottom:8px; line-height:1.3; }
.sec-desc { color:#94a3b8; font-size:1rem; line-height:1.6; margin-bottom:40px; max-width:600px; }

/* Feed card (wide) */
.feed-card {
  background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
  border-radius:20px; padding:36px 40px; margin-bottom:20px;
  display:grid; grid-template-columns:1fr 1fr; gap:48px; align-items:center;
  transition:border-color 0.3s,transform 0.2s; cursor:pointer;
}
.feed-card:hover { border-color:rgba(99,102,241,0.4); transform:translateY(-3px); }
.feed-card.dim { opacity:0.3; pointer-events:none; grid-template-columns:1fr; }
.card-left .card-label { font-size:0.72rem; color:#6366f1; font-weight:600; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:8px; }
.card-left h2 { font-size:1.6rem; font-weight:800; color:#fff; margin-bottom:12px; line-height:1.3; }
.card-left .card-summary { color:#94a3b8; font-size:0.95rem; line-height:1.65; margin-bottom:20px; }
.card-left .card-arrow { color:#6366f1; font-size:0.9rem; font-weight:600; }
.card-right { display:flex; flex-direction:column; gap:12px; }
.card-right .tag-row { display:flex; flex-wrap:wrap; gap:8px; }
.tag { padding:6px 16px; border-radius:100px; font-size:0.8rem; font-weight:500; }
.tag-ind { background:rgba(251,191,36,0.12); color:#fbbf24; }
.tag-sig { background:rgba(99,102,241,0.12); color:#a5b4fc; }
.card-right .signals { list-style:none; padding:0; }
.card-right .signals li { color:#cbd5e1; font-size:0.88rem; padding:5px 0; display:flex; align-items:center; gap:8px; }
.card-right .signals li::before { content:''; width:5px; height:5px; background:#6366f1; border-radius:50%; flex-shrink:0; }

/* Problem grid */
.prob-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; }
.prob-card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.06); border-radius:16px; padding:32px; transition:border-color 0.3s,transform 0.2s; }
.prob-card:hover { border-color:rgba(99,102,241,0.3); transform:translateY(-3px); }
.prob-card .emoji { font-size:2rem; margin-bottom:14px; }
.prob-card h3 { font-size:1.05rem; font-weight:700; color:#fff; margin-bottom:8px; }
.prob-card p { color:#94a3b8; font-size:0.9rem; line-height:1.55; }
.prob-card .solve { color:#a5b4fc; font-size:0.85rem; margin-top:12px; font-weight:500; }

/* How grid */
.how-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; }
.how-card { text-align:center; padding:40px 28px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:16px; }
.how-card .step-num { display:inline-flex; align-items:center; justify-content:center; width:36px; height:36px; border-radius:50%; background:rgba(99,102,241,0.15); color:#a5b4fc; font-size:0.85rem; font-weight:700; margin-bottom:16px; }
.how-card .how-emoji { font-size:2.2rem; margin-bottom:12px; }
.how-card h3 { font-size:1.05rem; font-weight:700; color:#fff; margin-bottom:8px; }
.how-card p { color:#94a3b8; font-size:0.88rem; line-height:1.5; }

/* CTA */
.cta-section { text-align:center; padding:80px 0 40px; }
.cta-section h2 { font-size:2.4rem; font-weight:800; color:#fff; margin-bottom:14px; line-height:1.3; }
.cta-section p { color:#94a3b8; font-size:1.05rem; margin-bottom:36px; }
.cta-btn { display:inline-flex; align-items:center; gap:8px; background:linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff; padding:16px 40px; border-radius:100px; font-size:1.05rem; font-weight:600; text-decoration:none; transition:transform 0.2s,box-shadow 0.2s; }
.cta-btn:hover { transform:translateY(-2px); box-shadow:0 8px 30px rgba(99,102,241,0.4); }

.footer { text-align:center; color:#334155; font-size:0.8rem; padding:40px 0 20px; border-top:1px solid rgba(255,255,255,0.04); }

@media(max-width:768px) {
  .hero h1 { font-size:2.2rem; }
  .feed-card { grid-template-columns:1fr; gap:24px; }
  .prob-grid, .how-grid { grid-template-columns:1fr; }
}
</style>
""", unsafe_allow_html=True)

# ===== HERO =====
st.markdown("""
<div class="hero">
  <div class="hero-badge">🎯 IGAWorks Audience Idea Bank</div>
  <h1>아이지에이웍스<br><span>오늘의 오디언스</span></h1>
  <p class="hero-sub">광고주가 미처 생각하지 못한 타겟을 매일 발견하는 곳.<br>트렌드를 자동으로 읽고, 새로운 오디언스를 제안합니다.</p>
</div>
""", unsafe_allow_html=True)

# ===== PROBLEM =====
st.markdown('<hr class="section-div">', unsafe_allow_html=True)
st.markdown("""
<div class="sec-label">PROBLEM</div>
<div class="sec-title">모두가 같은 고민을 하고 있습니다</div>
<div class="sec-desc">쓸 만한 오디언스를 찾는 데 시간이 너무 오래 걸리고, 결국 뻔한 타겟으로 돌아갑니다.</div>
<div class="prob-grid">
  <div class="prob-card">
    <div class="emoji">📢</div>
    <h3>광고주</h3>
    <p>"항상 같은 타겟에 광고하고 있다"</p>
    <div class="solve">→ 경쟁사가 모르는 오디언스를 먼저 발견</div>
  </div>
  <div class="prob-card">
    <div class="emoji">📋</div>
    <h3>AE</h3>
    <p>"제안서마다 차별점이 없다"</p>
    <div class="solve">→ 데이터 근거와 함께 바로 제안서에</div>
  </div>
  <div class="prob-card">
    <div class="emoji">💡</div>
    <h3>마케팅 팀</h3>
    <p>"분기마다 기획 아이디어가 고갈된다"</p>
    <div class="solve">→ 트렌드 기반 캠페인 아이디어 자동 제공</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ===== TODAY'S AUDIENCE =====
st.markdown('<hr class="section-div">', unsafe_allow_html=True)
st.markdown("""
<div class="sec-label">TODAY'S AUDIENCE</div>
<div class="sec-title">오늘의 오디언스</div>
<div class="sec-desc">행동 시그널의 조합으로 발굴한, 아직 아무도 안 쓰는 오디언스.</div>
""", unsafe_allow_html=True)

# 메인 카드 (wide)
st.markdown("""
<div class="feed-card">
  <div class="card-left">
    <div class="card-label">⛳ Today's Pick</div>
    <h2>접대 골프를 시작한 30대</h2>
    <p class="card-summary">회사 때문에 골프에 입문한 30대 대기업 직장인. 취미가 아니라 업무의 연장. 이 사람은 고민하지 않는다. 빠르게 산다.</p>
    <div class="card-arrow">자세히 보기 →</div>
  </div>
  <div class="card-right">
    <div class="tag-row">
      <span class="tag tag-ind">골프 용품</span>
      <span class="tag tag-ind">골프웨어</span>
      <span class="tag tag-ind">골프 레슨</span>
      <span class="tag tag-ind">프리미엄 카드</span>
    </div>
    <ul class="signals">
      <li>30대 초중반, 대기업 재직 추정</li>
      <li>최근 3개월 내 골프 앱 첫 설치</li>
      <li>골프 용품 비교 검색 시작</li>
      <li>평일 저녁 골프 콘텐츠 소비</li>
    </ul>
  </div>
</div>
""", unsafe_allow_html=True)

st.button("⛳ 접대 골프를 시작한 30대 — 상세 보기", key="detail_golf")

# Coming soon
st.markdown("""
<div class="feed-card dim">
  <div class="card-left">
    <div class="card-label">✈️ Coming Soon</div>
    <h2>90일 이내 해외여행 준비자</h2>
    <p class="card-summary">항공앱 탐색 + 환전앱 설치 + 여행 콘텐츠 소비. 출발 전 집중 소비 구간에 있는 유저.</p>
  </div>
</div>
<div class="feed-card dim">
  <div class="card-left">
    <div class="card-label">👶 Coming Soon</div>
    <h2>첫 아이 출산 준비 부부</h2>
    <p class="card-summary">모든 카테고리에서 '처음' 구매하는 고가치 유저. 브랜드 선점 효과가 가장 큰 오디언스.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ===== HOW IT WORKS =====
st.markdown('<hr class="section-div">', unsafe_allow_html=True)
st.markdown("""
<div class="sec-label">HOW IT WORKS</div>
<div class="sec-title">어떻게 작동하나요</div>
<div class="sec-desc"></div>
<div class="how-grid">
  <div class="how-card">
    <div class="step-num">01</div>
    <div class="how-emoji">📡</div>
    <h3>트렌드 자동 수집</h3>
    <p>뉴스·소셜·검색 트렌드를 실시간으로 수집하고 분석합니다.</p>
  </div>
  <div class="how-card">
    <div class="step-num">02</div>
    <div class="how-emoji">🧬</div>
    <h3>오디언스 자동 설계</h3>
    <p>AI가 트렌드를 행동 시그널 조합으로 변환해 새로운 오디언스를 생성합니다.</p>
  </div>
  <div class="how-card">
    <div class="step-num">03</div>
    <div class="how-emoji">🎯</div>
    <h3>업종별 맞춤 추천</h3>
    <p>업종만 선택하면, 지금 주목할 오디언스 리스트를 받아볼 수 있습니다.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ===== CTA =====
st.markdown("""
<div class="cta-section">
  <h2>뻔한 타겟팅,<br>이제 그만하세요</h2>
  <p>내가 모르는 트렌드를 알려주고, 바로 쓸 수 있는 오디언스로 만들어줍니다.</p>
  <a href="#" class="cta-btn">오디언스 아이디어 받기 →</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="footer">© 2026 IGAWorks — 오늘의 오디언스 · Audience Idea Bank</div>', unsafe_allow_html=True)
