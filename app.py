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
.block-container { max-width:480px!important; padding:0 20px 100px!important; margin:0 auto!important; }

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
.detail-wrap { max-width:520px; margin:0 auto; }
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

.footer { text-align:center; color:#ccc; font-size:0.72rem; padding:32px 0 16px; }

/* Streamlit button overrides */
div[data-testid="stButton"] > button {
  width:100%!important; border:none!important; background:transparent!important;
  padding:0!important; margin:0!important; min-height:0!important; cursor:pointer!important;
}
div[data-testid="stButton"] > button:hover { background:transparent!important; }
div[data-testid="stButton"] > button:focus { box-shadow:none!important; }
div[data-testid="stButton"] > button p { display:none; }

@media(max-width:768px) { .block-container { max-width:100%!important; } }
</style>
""", unsafe_allow_html=True)

# ===== CARD DATA =====
ESSAYS = [
    {
        "id": "pet", "emoji": "🐾", "tag": "반려동물", "number": 4,
        "title": "'반려동물 관심자'\n타겟팅 금지!",
        "sub": "첫 입양 후 2주, 앱이 폭발하는 사람",
        "stat": "반려동물 인구 <strong>1,546만</strong> 중 첫 입양자",
        "date": "2026.04.13",
    },
    {
        "id": "finance", "emoji": "💰", "tag": "금융", "number": 2,
        "title": "'대출 관심자'\n타겟팅 금지!",
        "sub": "다음 달 이자가 올라가는 사람",
        "stat": "대출 비교앱 <strong>3개+</strong> 동시 설치자",
        "date": "2026.04.10",
    },
    {
        "id": "golf", "emoji": "⛳", "tag": "골프", "number": 1,
        "title": "'골프 관심자'\n타겟팅 금지!",
        "sub": "접대 골프 입문자의 숨겨진 구매 시그널",
        "stat": "골프 인구 <strong>564만</strong> 중 접대 입문자",
        "date": "2026.04.11",
    },
]

# ===== ROUTING =====
if st.session_state.view == "detail_golf":
    if st.button("← 뒤로", key="back_g"):
        st.session_state.view = "feed"
        st.rerun()
    st.markdown("""
    <div class="detail-wrap">
    <div class="detail-hero">
      <div class="detail-emoji">⛳</div>
      <span class="detail-tag">골프</span>
      <div class="detail-title">'골프 관심자' 타겟팅 금지!</div>
      <div class="detail-sub">접대 골프 입문자의 숨겨진 구매 시그널</div>
      <div class="detail-meta">2026.04.11 · 오늘의 오디언스 #1</div>
    </div>

    <div class="quote-box">
      <p>"드라이버를 사는 게 아니라,<br>창피를 안 당할 보험을 사는 겁니다."</p>
    </div>

    <div class="section">
      <p>골프 시장이 커졌다는 건 다 압니다. 문제는 "골프 관심자"로 타겟팅하면 10년 경력 싱글 골퍼부터 유튜브만 보는 구경꾼까지 전부 섞인다는 것.</p>
      <p>우리가 주목한 건 <strong>완전히 다른 종류의 골퍼</strong>였습니다.</p>
    </div>

    <div class="section">
      <div class="section-label">BEHAVIOR SIGNALS</div>
      <div class="signal-item"><div class="signal-title">30대 초중반, 대기업 재직 추정</div><div class="signal-desc">기기 가격대 + 출퇴근 시간대 패턴으로 추정</div></div>
      <div class="signal-item"><div class="signal-title">최근 3개월 내 골프 앱 첫 설치</div><div class="signal-desc">90일간 골프 관련 앱 사용 이력 없음 → 신규 진입</div></div>
      <div class="signal-item"><div class="signal-title">골프 용품 비교 앱 탐색 시작</div><div class="signal-desc">골프존 + 스마트스코어 동시 설치 (14일 내)</div></div>
      <div class="signal-item"><div class="signal-title">평일 저녁 골프 콘텐츠 소비</div><div class="signal-desc">주말이 아닌 평일 19-22시 집중 사용 → 접대 준비</div></div>
      <div class="signal-item"><div class="signal-title">레슨 예약 앱 탐색</div><div class="signal-desc">속성 레슨 니즈 → 빠르게 필드에 나가야 하는 사람</div></div>
    </div>

    <div class="section">
      <p>이 조합이 의미하는 건 하나입니다.</p>
      <p><strong style="font-size:1.1rem">"회사 때문에 골프를 시작한 사람."</strong></p>
      <p>접대, 임원 라운딩, 거래처 미팅. 이 사람들은 기존 골퍼와 완전히 다른 니즈를 가지고 있습니다.</p>
      <p>장비에 진심인 골퍼와 달리 <strong>창피 안 당할 정도면 됩니다.</strong><br>스코어에 집착하는 골퍼와 달리 <strong>매너와 에티켓이 급합니다.</strong><br>가성비를 따지는 골퍼와 달리 <strong>무난하게 좋은 걸 원합니다.</strong></p>
      <p>그래서 이 사람은 고민하지 않습니다. <strong>빠르게 삽니다.</strong> 객단가가 높고, 전환이 빠릅니다.</p>
    </div>

    <div class="section">
      <div class="cmp-grid">
        <div class="cmp-card cmp-left"><h4>기존 골프 관심자</h4><p>장비에 진심<br>스코어에 집착<br>가성비 추구<br>주말 라운딩<br>천천히 구매</p></div>
        <div class="cmp-card cmp-right"><h4>접대 골프 입문자</h4><p>창피 안 당할 정도면 됨<br>매너와 에티켓이 급함<br>무난하게 좋은 걸 원함<br>평일 라운딩 비중 높음<br>빠르게 풀세트 구매</p></div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">DMP에서 잡는 법</div>
      <p><strong>[접대 골프 입문자]</strong><br>골프앱 첫 설치 + 30대 + 대기업 재직 추정<br>+ 평일 저녁 골프 콘텐츠 소비<br>+ 골프 용품 비교 검색 시작 (60일 내)</p>
    </div>

    <div class="section">
      <div class="ind-grid">
        <div class="ind-card"><div class="ind-title">⛳ 골프 용품</div><div class="ind-desc">입문자 풀세트, "처음 사는 드라이버"</div></div>
        <div class="ind-card"><div class="ind-title">👔 골프웨어</div><div class="ind-desc">"접대 라운딩에 입고 갈 옷"</div></div>
        <div class="ind-card"><div class="ind-title">🏌️ 골프 레슨</div><div class="ind-desc">"4주 만에 필드 나가기" 속성 레슨</div></div>
        <div class="ind-card"><div class="ind-title">💳 프리미엄 카드</div><div class="ind-desc">골프 특화 혜택 소구</div></div>
      </div>
    </div>

    <div class="insight-box">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"골프 관심자"는 오디언스가 아닙니다.<br><strong>왜 골프를 시작했는지</strong>가 오디언스를 만듭니다.</p>
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
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추정 모수</p><p style="color:#6366f1;font-size:1.5rem;font-weight:900">50~80만</p><p style="color:#555;font-size:0.7rem">골프 인구 564만 중</p></div>
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
      <div class="detail-title">'대출 관심자' 타겟팅 금지!</div>
      <div class="detail-sub">다음 달 이자가 올라가는 사람</div>
      <div class="detail-meta">2026.04.10 · 오늘의 오디언스 #2</div>
    </div>

    <div class="quote-box">
      <p>"매달 대출 광고에 3000만 원을 씁니다.<br>클릭은 되는데, 실제로 갈아타는 사람은<br>열 명 중 한 명도 안 돼요."</p>
    </div>

    <div class="section">
      <p>저축은행 마케터 K씨의 말입니다. "대출 관심자"를 타겟하면 클릭은 나옵니다. 금리가 궁금한 사람은 많으니까요.</p>
      <p>문제는 <strong>궁금한 사람과 시급한 사람이 완전히 다르다</strong>는 것.</p>
      <p>궁금한 사람은 클릭하고 나갑니다.<br>시급한 사람은 클릭하고 <strong>신청합니다.</strong></p>
    </div>

    <div class="section">
      <div class="section-label">BEHAVIOR SIGNALS</div>
      <div class="signal-item"><div class="signal-title">대출 비교앱 3개 이상 동시 설치 (7일 내)</div><div class="signal-desc">뱅크샐러드+핀다+토스를 일주일 안에 설치 → 비교쇼핑 단계 진입</div></div>
      <div class="signal-item"><div class="signal-title">설치 후 매일 반복 접속</div><div class="signal-desc">하루 2회+ 실행 → 조건 비교 중. 가끔 보는 사람과 완전히 다른 패턴</div></div>
      <div class="signal-item"><div class="signal-title">기존 은행앱 접속 빈도 감소</div><div class="signal-desc">주거래 은행앱 사용이 줄어듦 → 떠나려는 이탈 시그널</div></div>
      <div class="signal-item"><div class="signal-title">새벽·출퇴근 시간대 집중 탐색</div><div class="signal-desc">23시~02시, 07~09시 사용 → 급해서 틈틈이 찾는 사람</div></div>
      <div class="signal-item"><div class="signal-title">금융 뉴스앱 사용 빈도 급증</div><div class="signal-desc">금리 관련 뉴스 소비 증가 → 시장 변화에 반응하는 사람</div></div>
    </div>

    <div class="section">
      <p>핵심은 <strong>앱 설치 개수와 접속 빈도</strong>입니다.</p>
      <p>앱을 1개 깔고 가끔 보는 사람은 "언젠가" 갈아탈 사람입니다. 급하지 않아요.</p>
      <p>앱을 <strong>3개 깔고 매일 여는 사람</strong>은 다릅니다. 이 사람은 지금 금리를 비교하고 있고, 조건이 맞으면 <strong>이번 달 안에 움직입니다.</strong></p>
    </div>

    <div class="section">
      <div class="cmp-grid">
        <div class="cmp-card cmp-left"><h4>대출 구경꾼</h4><p>앱 1개, 가끔 접속<br>금리 궁금한 정도<br>은행앱 그대로 사용<br>낮 시간 가끔 확인<br>"나중에" 갈아탈 생각</p></div>
        <div class="cmp-card cmp-right"><h4>갈아타기 직전</h4><p>앱 3개+ 동시 설치<br>매일 반복 접속<br>기존 은행앱 사용 감소<br>새벽/출퇴근 집중 탐색<br>이번 달 안에 실행</p></div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">DMP에서 잡는 법</div>
      <p><strong>[대출 갈아타기 직전]</strong><br>대출 비교앱 3개+ (7일 내 동시 설치)<br>+ 매일 2회+ 접속<br>+ 기존 은행앱 사용 빈도 30%+ 감소<br>+ 새벽/출퇴근 시간대 집중</p>
    </div>

    <div class="section">
      <div class="ind-grid">
        <div class="ind-card"><div class="ind-title">🏦 은행/저축은행</div><div class="ind-desc">"지금 갈아타면 금리 0.3% 추가 인하"</div></div>
        <div class="ind-card"><div class="ind-title">📱 핀테크</div><div class="ind-desc">"3분 만에 내 대출 갈아타기 비교"</div></div>
        <div class="ind-card"><div class="ind-title">🛡️ 보험</div><div class="ind-desc">대출 연계 보험 리파이낸싱</div></div>
        <div class="ind-card"><div class="ind-title">💳 카드</div><div class="ind-desc">대출 이자 캐시백 카드</div></div>
      </div>
    </div>

    <div class="insight-box">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"대출 관심자"는 오디언스가 아닙니다.<br><strong>앱 3개를 동시에 까는 속도</strong>가 오디언스를 만듭니다.</p>
    </div>

    <div class="ad-compare">
      <p style="font-size:0.85rem;font-weight:700;color:#111;margin-bottom:16px">이 오디언스에게 보내는 광고</p>
      <p style="font-size:0.85rem;color:#999;margin-bottom:8px">❌ "대출 금리 비교, 최저 연 3.2%~"</p>
      <p style="font-size:0.85rem;color:#111;font-weight:600">✅ "지금 갈아타면 이번 달부터 이자가 줄어듭니다"</p>
    </div>

    <div class="audience-card">
      <p style="font-size:0.68rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:20px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.15rem;font-weight:800;margin-bottom:20px">대출 갈아타기 직전 유저</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추정 모수</p><p style="color:#6366f1;font-size:1.5rem;font-weight:900">120~200만</p><p style="color:#555;font-size:0.7rem">대출 비교앱 사용자 중</p></div>
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추천 업종</p><p style="color:#fff;font-size:0.88rem;font-weight:600;line-height:1.6">은행 · 핀테크<br>보험 · 카드</p></div>
      </div>
    </div>

    <div class="footer">오늘의 오디언스 #2 · by IGAWorks</div>
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
      <div class="section-label">BEHAVIOR SIGNALS</div>
      <div class="signal-item"><div class="signal-title">입양 앱(포인핸드) 첫 설치</div><div class="signal-desc">입양 의사결정의 시작점. 90일간 펫앱 사용 이력 없음 → 신규 확인</div></div>
      <div class="signal-item"><div class="signal-title">2주 내 펫 관련 앱 3개+ 동시 설치</div><div class="signal-desc">건강앱(펫닥)+쇼핑앱(펫프렌즈)+정보앱 동시 → 모든 게 처음인 사람</div></div>
      <div class="signal-item"><div class="signal-title">설치 후 하루 2회 이상 실행</div><div class="signal-desc">매일 반복 접속 → 불안해서 계속 확인하는 첫 반려인</div></div>
      <div class="signal-item"><div class="signal-title">심야 시간대 펫앱 사용 급증</div><div class="signal-desc">밤 11시~새벽 1시 집중 → 아이가 아파서 검색하는 패턴</div></div>
      <div class="signal-item"><div class="signal-title">기존 90일간 펫앱 사용 이력 없음</div><div class="signal-desc">기존 반려인이 아닌 완전 신규 → 모든 카테고리 첫 구매</div></div>
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
        <div><p style="color:#666;font-size:0.7rem;margin-bottom:4px">추정 모수</p><p style="color:#6366f1;font-size:1.5rem;font-weight:900">36~124만</p><p style="color:#555;font-size:0.7rem">연간 (1,546만 중 3~8%)</p></div>
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

    for e in ESSAYS:
        title_display = e["title"].replace(chr(10), "<br>")
        st.markdown(f"""
        <div class="feed-card">
          <div class="feed-emoji">{e["emoji"]}</div>
          <span class="feed-tag">{e["tag"]}</span>
          <div class="feed-title">{title_display}</div>
          <div class="feed-sub">{e["sub"]}</div>
          <div class="feed-bottom">
            <div class="feed-stat">{e["stat"]}</div>
            <div class="feed-arrow">→</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"open_{e['id']}", key=f"go_{e['id']}"):
            st.session_state.view = f"detail_{e['id']}"
            st.rerun()

    st.markdown('<div class="footer">오늘의 오디언스 · by IGAWorks · © 2026</div>', unsafe_allow_html=True)
