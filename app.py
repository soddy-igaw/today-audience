import streamlit as st

st.set_page_config(page_title="오늘의 오디언스 — IGAWorks", page_icon="🎯", layout="wide")

if "view" not in st.session_state:
    st.session_state.view = "feed"

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
.stApp { background:#fff; font-family:'Pretendard',sans-serif; }
header, .stDeployButton, #MainMenu, footer, [data-testid="stToolbar"] { display:none!important; }
.block-container { max-width:960px!important; padding:0 32px 80px!important; }

/* Nav */
.nav { display:flex; align-items:center; justify-content:space-between; padding:16px 0; border-bottom:1px solid #f0f0f0; margin-bottom:40px; }
.nav-logo { font-size:1rem; font-weight:800; color:#111; letter-spacing:-0.5px; }
.nav-logo span { color:#6366f1; }
.nav-sub { color:#bbb; font-size:0.72rem; }

/* Author */
.author { display:flex; align-items:center; gap:12px; margin-bottom:32px; }
.author-avatar { width:40px; height:40px; border-radius:50%; background:#6366f1; display:flex; align-items:center; justify-content:center; color:#fff; font-size:0.85rem; font-weight:700; }
.author-name { font-size:0.85rem; font-weight:600; color:#111; }
.author-date { font-size:0.75rem; color:#bbb; }

/* Body text */
.note-body p { color:#333; font-size:0.95rem; line-height:2; margin-bottom:24px; }
.note-body strong { color:#111; }
.note-body .lead { color:#111; font-size:1.2rem; font-weight:700; line-height:1.6; margin-bottom:28px; }
.note-body .quote { color:#555; font-size:1.1rem; line-height:1.8; font-style:italic; margin:32px 0; padding-left:20px; border-left:3px solid #6366f1; }

/* Signal box */
.sig-box { background:#f8f7ff; border-radius:12px; padding:24px 28px; margin:32px 0; }
.sig-box .sig-label { font-size:0.7rem; color:#6366f1; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:14px; }
.sig-box p { color:#333; font-size:0.9rem; line-height:2; margin:0; }

/* Compare */
.cmp-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:32px 0; }
.cmp-card { border-radius:12px; padding:20px; }
.cmp-card h4 { font-size:0.72rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px; font-weight:700; }
.cmp-card p { font-size:0.85rem; line-height:1.9; }
.cmp-left { background:#f8f8f8; }
.cmp-left h4 { color:#999; }
.cmp-left p { color:#888; }
.cmp-right { background:#f8f7ff; }
.cmp-right h4 { color:#6366f1; }
.cmp-right p { color:#333; }

/* Industry grid */
.ind-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:32px 0; }
.ind-card { background:#f8f8f8; border-radius:10px; padding:18px; }
.ind-card .ind-title { font-size:0.82rem; font-weight:700; color:#111; margin-bottom:4px; }
.ind-card .ind-desc { font-size:0.78rem; color:#888; line-height:1.4; }

/* Insight */
.insight { background:#111; border-radius:12px; padding:28px; margin:36px 0; }
.insight .ins-label { font-size:0.7rem; color:#a5b4fc; font-weight:700; letter-spacing:1.5px; margin-bottom:10px; }
.insight p { color:#fff; font-size:0.98rem; line-height:1.8; font-weight:500; }

/* Upcoming */
.upcoming-item { display:flex; align-items:center; gap:16px; padding:18px 0; border-bottom:1px solid #f5f5f5; }
.upcoming-item.dim { opacity:0.45; }
.up-emoji { font-size:1.6rem; }
.up-cat { font-size:0.68rem; color:#6366f1; font-weight:600; letter-spacing:1px; margin-bottom:1px; }
.up-title { font-size:0.95rem; font-weight:700; color:#111; margin-bottom:1px; }
.up-desc { font-size:0.78rem; color:#999; }
.up-badge { color:#ccc; font-size:0.72rem; font-weight:500; white-space:nowrap; margin-left:auto; }
.up-dday { background:#f0eeff; color:#6366f1; font-size:0.7rem; font-weight:700; padding:3px 10px; border-radius:100px; white-space:nowrap; margin-left:auto; }

/* Footer */
.footer { text-align:center; color:#ccc; font-size:0.75rem; padding:48px 0 20px; }

/* Card buttons - full width, looks like card */
div[data-testid="stButton"] > button {
  width:100%!important; text-align:left!important; border:1px solid #e8e8e8!important;
  border-radius:20px!important; padding:28px 36px!important; background:#fff!important;
  color:#111!important; font-size:0.95rem!important; font-weight:700!important;
  line-height:1.4!important; cursor:pointer!important; transition:box-shadow 0.2s!important;
  margin-bottom:8px!important; min-height:auto!important;
}
div[data-testid="stButton"] > button:hover {
  box-shadow:0 8px 30px rgba(0,0,0,0.08)!important; border-color:#d0d0d0!important;
  background:#fff!important; color:#111!important;
}
div[data-testid="stButton"] > button:focus { box-shadow:none!important; }
/* Back button - small */
div[data-testid="stButton"] > button[kind="secondary"] {
  width:auto!important; padding:8px 16px!important; border-radius:8px!important;
  font-size:0.85rem!important; font-weight:500!important;
}
.note-end { color:#bbb; font-size:0.78rem; margin-top:48px; padding-top:20px; border-top:1px solid #f0f0f0; }

/* Section header */
.sec-header { margin:48px 0 24px; padding-top:40px; border-top:1px solid #f0f0f0; }
.sec-header .sec-label { font-size:0.7rem; color:#6366f1; font-weight:700; letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }
.sec-header h2 { font-size:1.3rem; font-weight:800; color:#111; margin-bottom:4px; }
.sec-header p { font-size:0.85rem; color:#999; }

@media(max-width:768px) {
  .block-container { max-width:100%!important; }
}
</style>
""", unsafe_allow_html=True)

# ===== ROUTING =====
if st.session_state.view == "detail_golf":
    if st.button("← 돌아가기", key="back"):
        st.session_state.view = "feed"
        st.rerun()

    golf_html = """
    <style>.block-container { max-width:620px!important; padding:0 20px 80px!important; }</style>
    <div class="nav"><div>
      <div class="nav-logo"><span>오늘의</span> 오디언스</div>
      <div class="nav-sub">by IGAWorks</div>
    </div></div>

    <div class="author">
      <div class="author-avatar">IG</div>
      <div>
        <div class="author-name">IGAWorks 오디언스 랩</div>
        <div class="author-date">2026.04.11 · 오늘의 오디언스 #1</div>
      </div>
    </div>

    <div class="note-body">
      <p class="lead">'골프 관심자' 타겟팅 금지!<br>접대 골프 입문자의 숨겨진 구매 시그널</p>

      <div class="quote">"드라이버를 사는 게 아니라,<br>창피를 안 당할 보험을 사는 겁니다."</div>

      <p>광고 기획자의 말이 아닙니다.<br>IGAWorks DMP에서 발견한 실제 행동 데이터의 해석이죠.</p>

      <p>골프 시장이 커졌다는 건 다 압니다. 문제는 "골프 관심자"로 타겟팅하면 10년 경력 싱글 골퍼부터 유튜브만 보는 구경꾼까지 전부 섞인다는 것.</p>

      <p>우리가 주목한 건 <strong>완전히 다른 종류의 골퍼</strong>였습니다.</p>
    </div>

    <div class="sig-box">
      <div class="sig-label">BEHAVIOR SIGNALS</div>
      <p>→ 30대 초중반, 대기업 재직 추정<br>→ 최근 3개월 내 골프 앱 <strong>첫</strong> 설치<br>→ 골프 용품 비교 검색 시작<br>→ 골프 레슨 예약 앱 탐색<br>→ <strong>평일 저녁</strong> 골프 콘텐츠 소비</p>
    </div>

    <div class="note-body">
      <p>이 조합이 의미하는 건 하나입니다.</p>
      <p class="lead">"회사 때문에 골프를 시작한 사람."</p>
      <p>접대, 임원 라운딩, 거래처 미팅. 이 사람들은 기존 골퍼와 완전히 다른 니즈를 가지고 있습니다.</p>
      <p>장비에 진심인 골퍼와 달리 <strong>창피 안 당할 정도면 됩니다.</strong><br>스코어에 집착하는 골퍼와 달리 <strong>매너와 에티켓이 급합니다.</strong><br>가성비를 따지는 골퍼와 달리 <strong>무난하게 좋은 걸 원합니다.</strong></p>
      <p>그래서 이 사람은 고민하지 않습니다. <strong>빠르게 삽니다.</strong> 객단가가 높고, 전환이 빠릅니다.</p>
    </div>

    <div class="cmp-grid">
      <div class="cmp-card cmp-left">
        <h4>기존 골프 관심자</h4>
        <p>장비에 진심<br>스코어에 집착<br>가성비 추구<br>주말 라운딩<br>천천히 구매</p>
      </div>
      <div class="cmp-card cmp-right">
        <h4>접대 골프 입문자</h4>
        <p>창피 안 당할 정도면 됨<br>매너와 에티켓이 급함<br>무난하게 좋은 걸 원함<br>평일 라운딩 비중 높음<br>빠르게 풀세트 구매</p>
      </div>
    </div>

    <div class="sig-box">
      <div class="sig-label">DMP에서 잡는 법</div>
      <p><strong>[접대 골프 입문자]</strong><br>골프앱 첫 설치 + 30대 + 대기업 재직 추정<br>+ 평일 저녁 골프 콘텐츠 소비<br>+ 골프 용품 비교 검색 시작 (60일 내)</p>
    </div>

    <div class="ind-grid">
      <div class="ind-card"><div class="ind-title">⛳ 골프 용품</div><div class="ind-desc">입문자 풀세트, "처음 사는 드라이버" 소구</div></div>
      <div class="ind-card"><div class="ind-title">👔 골프웨어</div><div class="ind-desc">"접대 라운딩에 입고 갈 옷" 포지셔닝</div></div>
      <div class="ind-card"><div class="ind-title">🏌️ 골프 레슨</div><div class="ind-desc">"4주 만에 필드 나가기" 속성 레슨</div></div>
      <div class="ind-card"><div class="ind-title">💳 프리미엄 카드</div><div class="ind-desc">골프 특화 혜택 소구</div></div>
    </div>

    <div class="insight">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"골프 관심자"는 오디언스가 아닙니다.<br><strong>왜 골프를 시작했는지</strong>가 오디언스를 만듭니다.<br><br>같은 골프인데, 접대 입문자 / 취미 입문자 / 은퇴 후 입문자는 완전히 다른 사람입니다. 행동 시그널의 조합으로 이걸 구분할 수 있습니다.</p>
    </div>

    <div class="note-body">
      <p class="lead" style="font-size:1.05rem">이 오디언스에게 보내는 광고</p>
      <p>❌ 기존 "골프 관심자" 타겟:<br><span style="color:#999">"골프 시작하셨나요? 입문자 추천 클럽 보기"</span></p>
      <p>✅ 접대 골프 입문자 타겟:<br><strong>"다음 주 라운딩, 창피 안 당하려면 이것만 준비하세요"</strong></p>
      <p>같은 골프 광고인데, 메시지 하나로 전환율이 달라집니다.</p>
    </div>

    <div style="background:#111;border-radius:20px;padding:32px;margin:36px 0">
      <p style="font-size:0.7rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:24px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.2rem;font-weight:800;margin-bottom:20px">접대 골프 입문자</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px">
        <div>
          <p style="color:#666;font-size:0.72rem;margin-bottom:4px">추정 모수</p>
          <p style="color:#6366f1;font-size:1.6rem;font-weight:900">50~80만</p>
          <p style="color:#555;font-size:0.72rem">골프 인구 564만 중</p>
        </div>
        <div>
          <p style="color:#666;font-size:0.72rem;margin-bottom:4px">추천 업종</p>
          <p style="color:#fff;font-size:0.95rem;font-weight:600;line-height:1.6">골프 용품 · 골프웨어<br>레슨 · 프리미엄 카드</p>
        </div>
      </div>
      <div style="border-top:1px solid #222;padding-top:16px;display:flex;flex-direction:column;gap:10px">
        <div style="display:flex;justify-content:space-between"><span style="color:#666;font-size:0.8rem">시그널</span><span style="color:#ccc;font-size:0.8rem">골프앱 첫 설치 + 30대 + 평일 저녁</span></div>
        <div style="display:flex;justify-content:space-between"><span style="color:#666;font-size:0.8rem">추천 업종</span><span style="color:#ccc;font-size:0.8rem">골프 용품 · 웨어 · 레슨 · 카드</span></div>
        <div style="display:flex;justify-content:space-between"><span style="color:#666;font-size:0.8rem">메시지</span><span style="color:#fff;font-size:0.8rem;font-weight:600">"다음 주 라운딩 전에 준비하세요"</span></div>
      </div>
      <p style="color:#333;font-size:0.68rem;margin-top:16px">출처: 레저백서 2023 · IGAWorks DMP P030902</p>
    </div>

    <div class="note-end">오늘의 오디언스 #1 · 접대 골프를 시작한 30대 · by IGAWorks</div>
    """
    st.markdown(golf_html, unsafe_allow_html=True)

elif st.session_state.view == "detail_finance":
    # ===== FINANCE DETAIL =====
    if st.button("← 돌아가기", key="back_fin"):
        st.session_state.view = "feed"
        st.rerun()

    finance_html = """
    <style>.block-container { max-width:620px!important; padding:0 20px 80px!important; }</style>
    <div class="nav"><div>
      <div class="nav-logo"><span>오늘의</span> 오디언스</div>
      <div class="nav-sub">by IGAWorks</div>
    </div></div>

    <div class="author">
      <div class="author-avatar">IG</div>
      <div>
        <div class="author-name">IGAWorks 오디언스 랩</div>
        <div class="author-date">2026.04.10 · 오늘의 오디언스 #2</div>
      </div>
    </div>

    <div class="note-body">
      <p class="lead">'대출 관심자' 타겟팅 금지!<br>다음 달 이자가 올라가는 사람</p>

      <div class="quote">"매달 대출 광고에 3000만 원을 씁니다.<br>클릭은 되는데, 실제로 갈아타는 사람은<br>열 명 중 한 명도 안 돼요."</div>

      <p>저축은행 마케터 K씨의 말입니다. 대출 상품 광고를 집행하는 거의 모든 금융사가 같은 고민을 하고 있어요.</p>

      <p>"대출 관심자"를 타겟하면 클릭은 나옵니다. 금리가 궁금한 사람은 많으니까요. 문제는 <strong>궁금한 사람과 시급한 사람이 완전히 다르다</strong>는 것.</p>

      <p>궁금한 사람은 클릭하고 나갑니다.<br>시급한 사람은 클릭하고 <strong>신청합니다.</strong></p>

      <p>그런데 대부분의 광고는 이 둘을 구분하지 못합니다.</p>
    </div>

    <div class="sig-box">
      <div class="sig-label">우리가 발견한 것</div>
      <p>대출이 시급한 사람은 행동이 완전히 다릅니다.<br><br>→ 대출 비교앱 <strong>3개 이상</strong> 동시 설치 (7일 내)<br>→ 설치 후 <strong>매일 반복 접속</strong><br>→ "대출 갈아타기" "금리 인하 요구권" 콘텐츠 소비<br>→ 기존 은행앱 접속 빈도 <strong>감소</strong> (떠나려는 시그널)<br>→ 새벽, 출퇴근 시간대 집중 탐색</p>
    </div>

    <div class="note-body">
      <p>핵심은 <strong>앱 설치 개수와 접속 빈도</strong>입니다.</p>

      <p>앱을 1개 깔고 가끔 보는 사람은 "언젠가" 갈아탈 사람입니다. 급하지 않아요. 광고를 봐도 "나중에"라고 생각합니다.</p>

      <p>앱을 <strong>3개 깔고 매일 여는 사람</strong>은 다릅니다. 이 사람은 지금 금리를 비교하고 있고, 조건이 맞으면 <strong>이번 달 안에 움직입니다.</strong></p>

      <p>K씨에게 이 이야기를 했더니 이렇게 말했어요.</p>

      <div class="quote">"그러니까, 우리가 지금까지 광고비의 90%를<br>'언젠가' 사람한테 쓰고 있었다는 거네요."</div>

      <p>맞습니다. 그게 대출 광고 효율이 안 나오는 이유입니다.</p>
    </div>

    <div class="cmp-grid">
      <div class="cmp-card cmp-left">
        <h4>대출 구경꾼</h4>
        <p>앱 1개 설치<br>가끔 접속<br>"나중에 해야지"<br>광고 클릭 후 이탈<br>전환율 극히 낮음</p>
      </div>
      <div class="cmp-card cmp-right">
        <h4>대출 시급한 사람</h4>
        <p>앱 3개+ 동시 설치<br>매일 반복 접속<br>"이번 달 안에"<br>금리 숫자에 즉시 반응<br>전환율 극상</p>
      </div>
    </div>

    <div class="note-body">
      <p>더 흥미로운 건 <strong>시간대</strong>입니다.</p>

      <p>대출 구경꾼은 점심시간에 잠깐 봅니다. 심심해서요.<br>대출 시급한 사람은 <strong>새벽 1시</strong>에 봅니다. 잠이 안 와서요.</p>

      <p>같은 "대출 비교앱 사용자"인데, 접속 시간대 하나로 긴급도를 추정할 수 있습니다.</p>
    </div>

    <div class="sig-box">
      <div class="sig-label">DMP에서 잡는 법</div>
      <p><strong>[대출 시급 유저]</strong><br>대출 비교앱 3개+ (7일 내 동시 설치)<br>+ 설치 후 일 1회 이상 반복 접속<br>+ 기존 은행앱 접속 빈도 감소<br>+ 야간/새벽 시간대 활성<br>+ "갈아타기" "금리 비교" 콘텐츠 소비</p>
    </div>

    <div class="note-body">
      <p>이 세그먼트로 광고를 집행하면 어떻게 될까요?</p>

      <p>K씨의 저축은행이 기존 "대출 관심자" 대신 "대출 시급 유저"로 타겟을 바꿨다고 가정하면:</p>

      <p>→ 도달 수는 줄어듭니다 (전체의 10~15%)<br>→ 하지만 전환율은 <strong>3~5배</strong> 올라갑니다<br>→ 광고비 대비 실제 대환 건수가 늘어납니다<br>→ "지금 갈아타면 월 OO만 원 절약" 메시지가 <strong>진짜로 먹힙니다</strong></p>

      <p>왜? 이 사람은 이미 갈아타려고 마음먹은 사람이니까요. 광고가 설득하는 게 아니라, <strong>마지막 한 발을 밀어주는 것</strong>입니다.</p>
    </div>

    <div class="ind-grid">
      <div class="ind-card"><div class="ind-title">🏦 은행/저축은행</div><div class="ind-desc">대환대출 "지금 갈아타면 월 OO만 원 절약" 소구</div></div>
      <div class="ind-card"><div class="ind-title">📱 핀테크</div><div class="ind-desc">대출 비교 서비스 "3초 만에 내 금리 확인" 유도</div></div>
      <div class="ind-card"><div class="ind-title">🛡️ 보험</div><div class="ind-desc">대출 연계 보험 상품 타겟팅</div></div>
      <div class="ind-card"><div class="ind-title">💳 카드사</div><div class="ind-desc">대출 이자 캐시백 카드 전환</div></div>
    </div>

    <div class="insight">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"대출 관심자"는 오디언스가 아닙니다.<br><br>앱 <strong>1개</strong> 깔고 가끔 보는 사람과<br>앱 <strong>3개</strong> 깔고 매일 여는 사람은<br>완전히 다른 사람입니다.<br><br><strong>시급함의 크기</strong>가 오디언스를 만듭니다.<br><br>광고비의 90%를 "언젠가" 사람에게 쓰지 마세요.<br>"이번 달" 사람에게 쓰세요.</p>
    </div>

    <div class="note-body">
      <p class="lead" style="font-size:1.05rem">이 오디언스에게 보내는 광고</p>
      <p>❌ 기존 "대출 관심자" 타겟:<br><span style="color:#999">"금리 비교해보세요! 최저 연 3.5%~"</span></p>
      <p>✅ 대출 시급한 사람 타겟:<br><strong>"지금 갈아타면 월 32만 원 절약됩니다. 3분 만에 확인"</strong></p>
      <p>같은 대출 광고인데, 메시지 하나로 전환율이 달라집니다.</p>
    </div>

    <div style="background:#111;border-radius:20px;padding:32px;margin:36px 0">
      <p style="font-size:0.7rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:24px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.2rem;font-weight:800;margin-bottom:20px">대출 시급한 사람</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px">
        <div>
          <p style="color:#666;font-size:0.72rem;margin-bottom:4px">시그널</p>
          <p style="color:#fff;font-size:0.95rem;font-weight:600;line-height:1.6">대출앱 3개+<br>동시 설치 + 매일 접속</p>
        </div>
        <div>
          <p style="color:#666;font-size:0.72rem;margin-bottom:4px">추천 업종</p>
          <p style="color:#fff;font-size:0.95rem;font-weight:600;line-height:1.6">은행 · 저축은행<br>핀테크 · 보험</p>
        </div>
      </div>
      <div style="border-top:1px solid #222;padding-top:16px;display:flex;flex-direction:column;gap:10px">
        <div style="display:flex;justify-content:space-between"><span style="color:#666;font-size:0.8rem">핵심 구분</span><span style="color:#ccc;font-size:0.8rem">앱 1개 가끔 vs 3개 매일 + 야간</span></div>
        <div style="display:flex;justify-content:space-between"><span style="color:#666;font-size:0.8rem">메시지</span><span style="color:#fff;font-size:0.8rem;font-weight:600">"지금 갈아타면 월 32만 원 절약"</span></div>
      </div>
      <p style="color:#333;font-size:0.68rem;margin-top:16px">대출 비교앱 사용자 중 시급 유저 추정 10~15%</p>
    </div>

    <div class="note-end">오늘의 오디언스 #2 · 다음 달 이자가 올라가는 사람 · by IGAWorks</div>
    """
    st.markdown(finance_html, unsafe_allow_html=True)

elif st.session_state.view == "detail_gold":
    if st.button("← 돌아가기", key="back_gold"):
        st.session_state.view = "feed"
        st.rerun()

    jeonse_html = """
    <style>.block-container { max-width:620px!important; padding:0 20px 80px!important; }</style>
    <div class="nav"><div>
      <div class="nav-logo"><span>오늘의</span> 오디언스</div>
      <div class="nav-sub">by IGAWorks</div>
    </div></div>

    <div class="author">
      <div class="author-avatar">IG</div>
      <div>
        <div class="author-name">IGAWorks 오디언스 랩</div>
        <div class="author-date">2026.04.12 · 오늘의 오디언스 #3</div>
      </div>
    </div>

    <div class="note-body">
      <p class="lead">'전세대출 관심자' 타겟팅 금지!<br>4월 17일 전에 움직여야 하는 사람</p>

      <div class="quote">"불이 났는데<br>소화기 할인 쿠폰을 보내고 있는 격이죠."</div>

      <p>시중은행 전세대출 담당 마케터 L씨의 말입니다.</p>

      <p>4월 1일, 금융위원회가 가계대출 종합 대책을 발표했습니다. 핵심은 세 가지:</p>

      <p>→ 가계대출 연간 성장률 상한 <strong>1.5%</strong>로 하향<br>→ 다주택자 주담대 만기 연장 <strong>4월 17일부터 금지</strong><br>→ 비거주 1주택자 전세대출 보증 <strong>제한 검토 중</strong></p>

      <p>특히 비거주 1주택자 — 집은 있지만 전세 놓고 다른 곳에 사는 사람 — 의 전세대출 보증이 막힐 수 있습니다. 2025년 한 해 동안 1주택자에게 나간 전세대출 보증이 <strong>13조 9400억 원</strong>. 이 중 상당수가 영향권입니다.</p>

      <p>L씨에게 물었습니다. "지금 전세대출 광고 어떻게 하고 계세요?"</p>

      <div class="quote">"'전세대출 관심자'로 타겟하면 두 부류가 섞여요.<br>그냥 금리 비교하는 사람과,<br>규제 전에 대환하지 않으면 대출이 막히는 사람.<br><br>이 두 사람한테 같은 광고를 보내고 있어요.<br>한쪽은 '좋은 조건 있으면 갈아탈까' 수준이고,<br>다른 한쪽은 '이번 달 안에 안 하면 끝'인데."</div>

      <p>맞습니다. 규제가 만든 건 <strong>데드라인</strong>입니다. 4월 17일이 지나면 다주택자는 만기 연장이 안 됩니다. 비거주 1주택자 규제가 확정되면 전세대출 보증 자체가 막힙니다.</p>

      <p><strong>이 사람들은 "관심"이 아니라 "생존"으로 움직이고 있습니다.</strong></p>
    </div>

    <div class="sig-box">
      <div class="sig-label">BEHAVIOR SIGNALS</div>
      <p>→ 대출 비교앱 <strong>2개 이상 동시 설치</strong> (14일 내)<br>→ 부동산앱 활성 사용 <strong>급증</strong><br>→ 뉴스앱 접속 빈도 <strong>50% 이상 증가</strong><br>→ 규제 발표(4/1) 전후 <strong>설치 타이밍 집중</strong><br>→ 야간/새벽 시간대 활성</p>
    </div>

    <div class="note-body">
      <p>핵심은 <strong>"동시에 여러 앱을 까는 속도"</strong>입니다.</p>

      <p>금리 비교하는 사람은 앱을 하나 깔고 천천히 봅니다.<br>규제 전에 움직이는 사람은 <strong>대출앱 + 부동산앱 + 뉴스앱을 동시에 깝니다.</strong></p>
    </div>

    <div class="cmp-grid">
      <div class="cmp-card cmp-left">
        <h4>전세대출 구경꾼</h4>
        <p>부동산앱만 활성 증가<br>대출앱 미설치<br>뉴스 소비 평소와 비슷<br>30일+ 관찰 기간<br>전환 가능성 낮음</p>
      </div>
      <div class="cmp-card cmp-right">
        <h4>규제 전 급히 움직이는 사람</h4>
        <p>대출앱 2개+ 동시 설치<br>부동산앱 활성 급증<br>뉴스앱 접속 50%+ 증가<br>14일 내 집중 행동<br>전환 가능성 극상</p>
      </div>
    </div>

    <div class="note-body">
      <p>L씨가 이 구분법을 보고 말했어요.</p>

      <div class="quote">"규제 전에 움직이는 사람한테는<br>'금리 비교해보세요'가 아니라<br>'4월 17일 전에 대환 신청하세요'가 맞는 거네요.<br><br>지금 우리는 불 난 사람한테<br>소화기 할인 쿠폰을 보내고 있었던 거예요."</div>
    </div>

    <div class="sig-box">
      <div class="sig-label">DMP에서 잡는 법 (앱 데이터만으로)</div>
      <p><strong>[규제 전 급히 움직이는 사람]</strong><br>대출 비교앱 2개+ (14일 내 동시 설치)<br>+ 부동산앱 활성 사용 급증<br>+ 뉴스앱 접속 빈도 50%+ 증가<br>+ 규제 발표(4/1) 이후 설치<br><br><strong>[확인 중인 사람 — 교육 콘텐츠 타겟]</strong><br>부동산앱/뉴스앱 활성 증가 (+30%)<br>+ 대출앱 미설치<br>+ 30일 관찰 기간<br><br><em>* 실제 대출 보유 여부, 주택 소유 여부는 DMP로 확인 불가.<br>앱 설치 속도 + 동시성 + 타이밍으로 긴급도를 추정합니다.</em></p>
    </div>

    <div class="note-body">
      <p>이 오디언스를 누가 사나?</p>

      <p>전세대출 전환 1건당 은행 수수료는 수십만 원입니다. 규제 전 대환 수요가 몰리는 지금, <strong>이 유저 1명의 가치는 평소의 3~5배</strong>입니다.</p>
    </div>

    <div class="ind-grid">
      <div class="ind-card"><div class="ind-title">🏦 은행/저축은행</div><div class="ind-desc">"4/17 전 대환 신청" 긴급 캠페인</div></div>
      <div class="ind-card"><div class="ind-title">📱 핀테크</div><div class="ind-desc">대출 비교 "내 전세대출 규제 영향 확인" 유도</div></div>
      <div class="ind-card"><div class="ind-title">🏠 부동산 플랫폼</div><div class="ind-desc">전세→매매 전환 매물 추천</div></div>
      <div class="ind-card"><div class="ind-title">🛡️ 보험</div><div class="ind-desc">전세보증보험 긴급 가입 타겟팅</div></div>
    </div>

    <div class="insight">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"전세대출 관심자"는 오디언스가 아닙니다.<br><br>규제가 만든 건 <strong>데드라인</strong>입니다.<br>4월 17일 전에 움직이는 사람과<br>그냥 뉴스 보는 사람은 완전히 다릅니다.<br><br><strong>대출앱 2개를 동시에 까는 속도</strong>가<br>오디언스를 만듭니다.<br><br>불 난 사람한테 소화기 할인 쿠폰을 보내지 마세요.<br>소화기를 들고 달려가세요.</p>
    </div>

    <div class="note-body">
      <p class="lead" style="font-size:1.05rem">이 오디언스에게 보내는 광고</p>
      <p>❌ 기존 "전세대출 관심자" 타겟:<br><span style="color:#999">"전세대출 금리 비교, 최저 연 3.2%~"</span></p>
      <p>✅ 규제 전 급히 움직이는 사람 타겟:<br><strong>"4월 17일 전에 대환 신청하세요. 이후엔 만기 연장이 안 됩니다"</strong></p>
      <p>같은 전세대출 광고인데, 메시지 하나로 전환율이 달라집니다.</p>
    </div>

    <div style="background:#111;border-radius:20px;padding:32px;margin:36px 0">
      <p style="font-size:0.7rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:24px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.2rem;font-weight:800;margin-bottom:20px">전세대출 규제 영향권 유저</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px">
        <div>
          <p style="color:#666;font-size:0.72rem;margin-bottom:4px">시그널</p>
          <p style="color:#fff;font-size:0.95rem;font-weight:600;line-height:1.6">대출앱 2개+ 동시<br>부동산앱 급증 + 뉴스 50%+</p>
        </div>
        <div>
          <p style="color:#666;font-size:0.72rem;margin-bottom:4px">추천 업종</p>
          <p style="color:#fff;font-size:0.95rem;font-weight:600;line-height:1.6">은행 · 핀테크<br>부동산 · 보험</p>
        </div>
      </div>
      <div style="border-top:1px solid #222;padding-top:16px;display:flex;flex-direction:column;gap:10px">
        <div style="display:flex;justify-content:space-between"><span style="color:#666;font-size:0.8rem">데드라인</span><span style="color:#ef4444;font-size:0.8rem;font-weight:700">4월 17일 만기연장 금지</span></div>
        <div style="display:flex;justify-content:space-between"><span style="color:#666;font-size:0.8rem">영향 규모</span><span style="color:#ccc;font-size:0.8rem">1주택자 전세대출 보증 13.9조</span></div>
        <div style="display:flex;justify-content:space-between"><span style="color:#666;font-size:0.8rem">메시지</span><span style="color:#fff;font-size:0.8rem;font-weight:600">"4/17 전에 대환 신청하세요"</span></div>
      </div>
      <p style="color:#333;font-size:0.68rem;margin-top:16px">출처: 금융위 4/1 발표 · 서울경제 4/12 보도</p>
    </div>

    <div class="note-end">오늘의 오디언스 #3 · 4월 17일 전에 움직여야 하는 사람 · by IGAWorks</div>
    """
    st.markdown(jeonse_html, unsafe_allow_html=True)

elif st.session_state.view == "detail_pet":
    if st.button("← 돌아가기", key="back_pet"):
        st.session_state.view = "feed"
        st.rerun()

    pet_html = """
    <style>.block-container { max-width:620px!important; padding:0 20px 80px!important; }</style>
    <div class="nav"><div>
      <div class="nav-logo"><span>오늘의</span> 오디언스</div>
      <div class="nav-sub">by IGAWorks</div>
    </div></div>

    <div class="author">
      <div class="author-avatar">IG</div>
      <div>
        <div class="author-name">IGAWorks 오디언스 랩</div>
        <div class="author-date">2026.04.13 · 오늘의 오디언스 #4</div>
      </div>
    </div>

    <div class="note-body">
      <p class="lead">'반려동물 관심자' 타겟팅 금지!<br>첫 입양 후 2주,<br>앱이 폭발하는 사람</p>

      <div class="quote">"첫 사료는 선택이 아니라 습관이에요.<br>처음 먹인 사료를 3년을 먹입니다.<br>그 2주를 놓치면, 3년을 놓치는 겁니다."</div>

      <p>프리미엄 사료 브랜드 마케터 J씨의 말입니다.</p>

      <p>한국 반려동물 인구 1,546만 명. 591만 가구. 월 평균 지출 19만 4천 원. 시장 규모 4.5조 원, 2032년 21조 원 전망.</p>

      <p>모든 펫 브랜드가 이 시장을 잡으려고 합니다. 문제는 <strong>"반려동물 관심자"로 타겟하면 대부분이 귀여운 동물 영상만 보는 사람</strong>이라는 것.</p>

      <p>J씨에게 물었습니다. "진짜 반려동물을 키우는 사람은 어떻게 찾나요?"</p>

      <div class="quote">"반려동물 관심자 타겟으로 광고하면<br>클릭의 80%가 고양이 영상 보는 사람이에요.<br>실제로 사료를 살 사람은 20%도 안 됩니다.<br><br>진짜 문제는, 첫 입양자가 모든 걸 결정하는<br>골든타임이 딱 2주라는 거예요.<br>사료, 용품, 병원, 보험 — 전부 2주 안에 정합니다."</div>

      <p>우리는 앱 데이터에서 그 2주를 찾았습니다.</p>
    </div>

    <div class="sig-box">
      <div class="sig-label">BEHAVIOR SIGNALS</div>
      <p>→ 입양 앱(포인핸드) <strong>첫 설치</strong><br>→ 2주 내 펫 관련 앱 <strong>3개 이상 동시 설치</strong><br>→ 펫 건강앱(펫닥/핏펫) + 쇼핑앱(펫프렌즈/쿠팡) 동시<br>→ 설치 후 <strong>하루 2회 이상</strong> 실행<br>→ 기존 90일간 펫앱 <strong>사용 이력 없음</strong> (신규 확인)</p>
    </div>

    <div class="note-body">
      <p>핵심은 <strong>"2주 안에 3개 이상 펫앱을 동시에 까는 속도"</strong>입니다.</p>

      <p>기존 반려인은 이미 쓰는 앱이 있어요. 새 앱을 잘 안 깝니다.<br>첫 입양자는 <strong>모든 게 처음</strong>이라 한꺼번에 깝니다.</p>
    </div>

    <div class="cmp-grid">
      <div class="cmp-card cmp-left">
        <h4>반려동물 콘텐츠 소비자</h4>
        <p>펫앱 미설치<br>귀여운 영상만 소비<br>구매 의도 없음<br>광고 클릭 후 이탈<br>전환 가능성 낮음</p>
      </div>
      <div class="cmp-card cmp-right">
        <h4>첫 입양 폭발기 유저</h4>
        <p>2주 내 펫앱 3개+ 설치<br>입양앱+건강앱+쇼핑앱 동시<br>하루 2회+ 실행<br>모든 카테고리 첫 구매<br>전환 가능성 극상</p>
      </div>
    </div>

    <div class="note-body">
      <p>J씨에게 이 구분법을 보여줬더니 이렇게 말했어요.</p>

      <div class="quote">"포인핸드 깔고 2주 안에 펫닥이랑 쿠팡 펫 카테고리를<br>동시에 쓰기 시작한 사람이면,<br>그건 거의 확실히 첫 입양자예요.<br><br>이 사람한테 '첫 달 사료 무료 체험'을 보내면<br>3년 고객이 됩니다."</div>

      <p>반려동물 보험도 마찬가지입니다. 펫보험 인지도 91.7%인데 가입률은 12.8%. 대부분 "나중에 해야지" 하다가 안 합니다. 하지만 <strong>첫 입양 2주 안에 보험앱을 같이 깐 사람</strong>은 가입 확률이 완전히 다릅니다.</p>
    </div>

    <div class="sig-box">
      <div class="sig-label">DMP에서 잡는 법 (앱 데이터만으로)</div>
      <p><strong>[첫 입양 폭발기]</strong><br>입양앱(포인핸드) 첫 설치<br>+ 14일 내 펫앱 3개+ 동시 설치 (건강+쇼핑 필수)<br>+ 설치 후 7일간 하루 2회+ 실행<br>+ 최근 90일 펫앱 사용 이력 없음<br><br><em>* 실제 입양 여부는 DMP로 확인 불가.<br>앱 설치 폭발 패턴 + 신규 여부로 추정합니다.<br>추정 규모: 연간 36~124만 명 (P020501 기반 3~8%)</em></p>
    </div>

    <div class="note-body">
      <p class="lead" style="font-size:1.05rem">이 오디언스에게 보내는 광고</p>
      <p>❌ 기존 "반려동물 관심자" 타겟:<br><span style="color:#999">"우리 아이에게 좋은 사료, 지금 할인 중!"</span></p>
      <p>✅ 첫 입양 폭발기 타겟:<br><strong>"첫 달 사료 무료 체험. 우리 아이 첫 끼를 함께하세요"</strong></p>
    </div>

    <div class="ind-grid">
      <div class="ind-card"><div class="ind-title">🍖 사료/간식</div><div class="ind-desc">"첫 달 무료 체험" 첫 사료 선점</div></div>
      <div class="ind-card"><div class="ind-title">🛡️ 펫보험</div><div class="ind-desc">"입양 첫 달 가입 시 30% 할인"</div></div>
      <div class="ind-card"><div class="ind-title">🏥 동물병원</div><div class="ind-desc">"첫 건강검진 무료" 신규 등록 유도</div></div>
      <div class="ind-card"><div class="ind-title">🧸 용품/장난감</div><div class="ind-desc">"첫 입양 스타터 키트" 번들 판매</div></div>
    </div>

    <div class="insight">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"반려동물 관심자"는 오디언스가 아닙니다.<br><br>귀여운 영상을 보는 사람과<br>2주 안에 앱 3개를 동시에 까는 사람은<br>완전히 다른 사람입니다.<br><br><strong>첫 입양 후 2주</strong>가 오디언스를 만듭니다.<br>그 2주를 놓치면, 3년을 놓칩니다.</p>
    </div>

    <div style="background:#111;border-radius:20px;padding:32px;margin:36px 0">
      <p style="font-size:0.7rem;color:#a5b4fc;font-weight:700;letter-spacing:1.5px;margin-bottom:24px">📋 AUDIENCE CARD</p>
      <h3 style="color:#fff;font-size:1.2rem;font-weight:800;margin-bottom:20px">첫 입양 폭발기 유저</h3>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px">
        <div>
          <p style="color:#666;font-size:0.72rem;margin-bottom:4px">추정 모수</p>
          <p style="color:#6366f1;font-size:1.6rem;font-weight:900">36~124만</p>
          <p style="color:#555;font-size:0.72rem">연간 (1,546만 중 3~8%)</p>
        </div>
        <div>
          <p style="color:#666;font-size:0.72rem;margin-bottom:4px">추천 업종</p>
          <p style="color:#fff;font-size:0.95rem;font-weight:600;line-height:1.6">사료 · 펫보험<br>동물병원 · 용품</p>
        </div>
      </div>
      <div style="border-top:1px solid #222;padding-top:16px;display:flex;flex-direction:column;gap:10px">
        <div style="display:flex;justify-content:space-between"><span style="color:#666;font-size:0.8rem">시그널</span><span style="color:#ccc;font-size:0.8rem">펫앱 3개+ 동시 (14일 내) + 신규</span></div>
        <div style="display:flex;justify-content:space-between"><span style="color:#666;font-size:0.8rem">골든타임</span><span style="color:#f97316;font-size:0.8rem;font-weight:700">입양 후 2주</span></div>
        <div style="display:flex;justify-content:space-between"><span style="color:#666;font-size:0.8rem">메시지</span><span style="color:#fff;font-size:0.8rem;font-weight:600">"첫 달 무료 체험"</span></div>
      </div>
      <p style="color:#333;font-size:0.68rem;margin-top:16px">출처: KB금융 2025 반려동물 보고서 · IGAWorks DMP P020501</p>
    </div>

    <div class="note-end">오늘의 오디언스 #4 · 첫 입양 후 2주, 앱이 폭발하는 사람 · by IGAWorks</div>
    """
    st.markdown(pet_html, unsafe_allow_html=True)

elif st.session_state.view == "detail_new5":
    if st.button("← 돌아가기", key="back_5"):
        st.session_state.view = "feed"
        st.rerun()

    st.markdown("""
    <style>.block-container { max-width:620px!important; padding:0 20px 80px!important; }</style>
    <div class="nav"><div>
      <div class="nav-logo"><span>오늘의</span> 오디언스</div>
      <div class="nav-sub">by IGAWorks</div>
    </div></div>
    <div class="author">
      <div class="author-avatar">IG</div>
      <div>
        <div class="author-name">IGAWorks 오디언스 랩</div>
        <div class="author-date">2026.04.14 · 오늘의 오디언스 #5</div>
      </div>
    </div>
    <div class="note-body">

<p class="lead">
'부동산 관심자' 타겟팅 금지!<br>
전세 만료 D-60 행동 패턴으로 잡는 진짜 이사 예정자
</p>

<div class="quote">
"직방 앱 설치자에게 이사 관련 광고를 돌렸는데, 전환율이 1%도 안 나와요. 알고 보니 대부분이 그냥 호기심으로 시세 확인하는 사람들이더라고요. 정말 이사할 사람만 골라낼 방법이 없을까요?"<br>
— K씨, 이삿짐업체 마케터
</div>

부동산 시장이 요동치고 있다.

2024년 2월 경인지역 아파트 거래량이 전월 대비 13.2% 감소하며, 매매시장이 얼어붙고 있다는 소식이 연일 이어진다. 하지만 전세시장은 다른 이야기다. 전세 만료 물량이 몰리면서, 수많은 세입자들이 이사를 앞두고 있다.

문제는 이들을 어떻게 찾느냐다.

기존 부동산 앱 타겟팅은 너무 넓다. 직방 앱 설치자 1000만 명 중에 실제로 3개월 내 이사할 사람은 몇 명일까? 대부분은 호기심 많은 구경꾼이다. 동네 시세 확인하고, 내 집값 올랐나 체크하고, 그냥 심심해서 둘러보는 사람들.

진짜 이사 직전인 사람들은 행동 패턴이 완전히 다르다.

<div class="sig-box">
<div class="sig-label">BEHAVIOR SIGNALS</div>

**1. 부동산 앱 3개 이상 7일 내 동시 설치**<br>
직방, 다방, 호갱노노를 일주일 안에 다 깐다. 한두 개로는 부족하다고 느끼는 시점.

**2. 매일 접속 → 하루 3회 이상 접속으로 급증**<br>
기존엔 가끔 확인하던 앱을, 출근길-점심-퇴근 후 하루에 여러 번 확인하기 시작.

**3. 사용 시간대 변화: 심야(23시-02시) 접속 빈도 증가**<br>
낮에 못 본 매물들을 밤에 꼼꼼히 체크. 이사 스트레스로 잠도 잘 안 올 때.

**4. 기존 은행앱 사용 빈도 급증 (30일 내 3배 이상)**<br>
보증금 마련하려고 적금 해지하고, 대출 한도 확인하고, 계좌 정리하느라 분주.

**5. 지도앱에서 특정 지역 반복 검색 패턴**<br>
같은 동네를 며칠간 계속 확대/축소하며 보는 행동. 교통편, 주변 시설 체크 중.

**6. 90일 미사용 후 부동산 앱 재설치**<br>
예전에 쓰다가 삭제했던 앱을 다시 깔기 시작. 뭔가 계기(전세 만료 통보 등)가 생긴 시점.

</div>

핵심은 **행동의 급격한 변화**다.

평소에 부동산에 관심 없던 사람이 갑자기 모든 앱을 깔기 시작하거나, 가끔 보던 사람이 매일 여러 번씩 확인하기 시작할 때. 이런 '변곡점'이야말로 진짜 니즈가 발생한 순간이다.

단순히 "부동산 앱 쓰는 사람"이 아니라, "최근 30일간 부동산 관련 행동이 급변한 사람"을 찾아야 한다.

<div class="cmp-grid">
<div class="cmp-card cmp-left">
<h4>🏠 일반적인 부동산 앱 사용자</h4>
주말에 가끔 동네 시세 확인<br>
앱 1-2개만 사용<br>
하루 1회 미만 접속<br>
특정 지역 고정 없이 여기저기 구경<br>
은행앱 사용 패턴 변화 없음<br>
몇 달째 동일한 사용 패턴 유지<br>
푸시 알림 대부분 무시<br>
앱 내 체류 시간 5분 미만<br>
</div>
<div class="cmp-card cmp-right">
<h4>🚚 진짜 이사 예정자</h4>
매일 여러 번 강박적으로 확인<br>
부동산 앱 3개 이상 병행 사용<br>
하루 3회 이상, 심야시간까지 접속<br>
특정 2-3개 지역에만 집중 탐색<br>
은행앱 사용 빈도 3배 이상 증가<br>
최근 30일간 모든 행동 패턴 급변<br>
매물 알림에 즉시 반응<br>
앱 내에서 20분 이상 머무르며 비교<br>
</div>
</div>

<div class="sig-box">
<div class="sig-label">DMP에서 잡는 법</div>

**핵심 조건 조합:**<br>
(직방 OR 다방 OR 호갑노노) 3개 이상 설치 AND<br>
최근 30일간 사용빈도 200% 이상 증가 AND<br>
은행/금융 앱 사용빈도 동시 증가 AND<br>
심야시간(23-02시) 접속 횟수 증가

**기간 설정:** 최근 30일간 행동 변화<br>
**제외 조건:** 부동산 앱 6개월 이상 꾸준히 사용자 (업무용 추정)<br>
**가중치:** 90일 미사용 후 재설치 시 우선순위 상향

</div>

<div class="ind-grid">
<div class="ind-card">
<div class="ind-title">🚛 이삿짐 / 포장이사</div>
<div class="ind-desc">"3월 이사철 D-30, 견적 미리 받고 마음 편히"<br>"새벽까지 집 보느라 고생 많으셨죠?"</div>
</div>
<div class="ind-card">
<div class="ind-title">🏠 부동산 중개 / 컨설팅</div>
<div class="ind-desc">"여러 앱 돌아다니지 마세요, 한 번에 해결"<br>"전세 만료 임박? 전문가와 상담하세요"</div>
</div>
<div class="ind-card">
<div class="ind-title">🏦 대출 / 금융상품</div>
<div class="ind-desc">"이사 자금 부족할 땐 전세자금대출"<br>"보증금 마련, 지금 시작해야 간에 맞아요"</div>
</div>
<div class="ind-card">
<div class="ind-title">🛋️ 인테리어 / 가전</div>
<div class="ind-desc">"새 집 준비는 이사 전부터"<br>"이사 스트레스는 줄이고, 새 집 설렘은 두 배로"</div>
</div>
</div>

<div class="insight">
<div class="ins-label">KEY INSIGHT</div>
부동산은 '관심사'가 아니라 '상황'이다. 평생에 몇 번 없는 이사라는 이벤트가 발생했을 때만 진짜 고객이 된다. 중요한 건 이 '상황 발생 시점'을 정확히 포착하는 것이다.
</div>

**광고 카피 비교**

❌ 기존: "부동산 앱 사용자 대상"<br>
"새로운 우리 동네를 찾아보세요"<br>
"더 좋은 집이 기다리고 있어요"

✅ 새 오디언스: "이사 임박자 대상"<br>
"벌써 3개 앱 깔아서 보고 계시죠?"<br>
"새벽까지 집 보느라 고생 많으셨어요"<br>
"이사 D-60, 지금 준비해야 할 것들"

<div style="background: #111; color: #fff; padding: 20px; border-radius: 8px; margin: 20px 0;">
<h3 style="color: #00ff88; margin-bottom: 15px;">🎯 AUDIENCE CARD</h3>
<strong>전세 만료 D-60 이사 예정자</strong><br><br>
<strong>추정 모수:</strong> 15~25만 명 (월간)<br><br>
<strong>핵심 시그널:</strong><br>
• 부동산 앱 3개+ 동시 사용 + 사용빈도 급증<br>
• 은행앱 접속 패턴 동시 변화<br>
• 심야시간 매물 탐색 행동<br><br>
<strong>추천 업종:</strong> 이삿짐, 부동산 서비스, 대출, 인테리어<br><br>
<strong>메시지 방향:</strong> 이사 준비 과정의 스트레스 공감 + 실용적 솔루션
</div>

<div class="note-end">
구경꾼과 진짜 고객을 구분하는 건 앱 설치 여부가 아니라, 행동의 변화 속도다. 부동산 시장에서 성공하려면 '언제부터 이렇게 열심히 집을 찾기 시작했는가'를 봐야 한다. 급하게 움직이는 사람이 진짜 고객이다.
</div>

</div>
    """, unsafe_allow_html=True)

else:
    # ===== MAIN PAGE =====
    st.markdown("""
    <div class="nav"><div>
      <div class="nav-logo"><span>오늘의</span> 오디언스</div>
      <div class="nav-sub">by IGAWorks</div>
    </div></div>

    <div style="padding:48px 0 40px;text-align:center">
      <p style="font-size:0.75rem;color:#6366f1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px">AUDIENCE IDEA BANK</p>
      <h1 style="font-size:2.2rem;font-weight:900;color:#111;line-height:1.25;letter-spacing:-1px;margin-bottom:16px">다음 캠페인,<br>누구한테 해야 하지?</h1>
      <p style="color:#888;font-size:0.92rem;line-height:1.7">광고주가 미처 생각하지 못한 타겟을 매일 발견하는 곳.<br>트렌드를 자동으로 읽고, 행동 시그널을 조합해<br>아직 아무도 안 쓰는 오디언스를 제안합니다.</p>
    </div>
    <div style="border-top:1px solid #f0f0f0;margin:8px 0 32px"></div>

    <p style="font-size:0.7rem;color:#6366f1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:20px">🎯 오늘의 오디언스</p>

    <div style="border-radius:20px;overflow:hidden;border:1px solid #e8e8e8;margin-bottom:40px;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 8px 30px rgba(0,0,0,0.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="background:linear-gradient(135deg,#4a1942 0%,#6b3fa0 100%);padding:48px 36px;position:relative;overflow:hidden">
        <div style="position:absolute;top:20px;right:24px;font-size:4rem;opacity:0.15">🏠</div>
        <span style="background:rgba(255,255,255,0.2);color:#fff;font-size:0.68rem;font-weight:600;padding:4px 12px;border-radius:100px;letter-spacing:1px">TODAY</span>
        <h2 style="color:#fff;font-size:1.5rem;font-weight:900;line-height:1.3;margin-top:16px">'부동산 관심자' 타겟팅 금지!</h2>
        <p style="color:rgba(255,255,255,0.7);font-size:0.92rem;line-height:1.6;margin-top:8px">전세 만료 D-60 행동 패턴으로 잡는 진짜 이사 예정자</p>
      </div>
      <div style="padding:20px 24px;display:flex;align-items:center;justify-content:space-between">
        <span style="font-size:0.78rem;color:#888">추정 오디언스 <strong style="color:#6366f1">15~25만</strong></span>
        <span style="color:#6366f1;font-size:0.82rem;font-weight:600">읽기 →</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 전세 만료 D-60 행동 패턴으로 잡는 진짜 이사 예정자", key="go_new5"):
        st.session_state.view = "detail_new5"
        st.rerun()

        st.markdown("""
    <p style="font-size:0.7rem;color:#6366f1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin:8px 0 20px">📚 지난 노트</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:14px;margin-bottom:40px">
      <div style="border-radius:16px;overflow:hidden;border:1px solid #f0f0f0;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
        <div style="background:linear-gradient(135deg,#1a472a,#1a472acc);padding:28px 20px;position:relative"><div style="position:absolute;top:10px;right:14px;font-size:2.4rem;opacity:0.15">⛳</div><span style="background:rgba(255,255,255,0.2);color:#fff;font-size:0.6rem;font-weight:600;padding:2px 8px;border-radius:100px">#4</span><h3 style="color:#fff;font-size:0.92rem;font-weight:800;line-height:1.3;margin-top:10px">반려동물 관심자</h3></div>
        <div style="padding:12px 14px"><span style="font-size:0.68rem;color:#999">반려동물 인구 1,546만 명 중 첫 입양자</span></div>
      </div>
      <div style="border-radius:16px;overflow:hidden;border:1px solid #f0f0f0;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
        <div style="background:linear-gradient(135deg,#1a472a,#3a7d5c);padding:28px 20px;position:relative"><div style="position:absolute;top:10px;right:14px;font-size:2.4rem;opacity:0.15">⛳</div><span style="background:rgba(255,255,255,0.2);color:#fff;font-size:0.6rem;font-weight:600;padding:2px 8px;border-radius:100px">#1</span><h3 style="color:#fff;font-size:0.92rem;font-weight:800;line-height:1.3;margin-top:10px">접대 골프<br>입문자</h3></div>
        <div style="padding:12px 14px"><span style="font-size:0.68rem;color:#999">골프 용품 · 웨어 · 레슨</span></div>
      </div>
      <div style="border-radius:16px;overflow:hidden;border:1px solid #f0f0f0;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
        <div style="background:linear-gradient(135deg,#1e3a5f,#2a5298);padding:28px 20px;position:relative"><div style="position:absolute;top:10px;right:14px;font-size:2.4rem;opacity:0.15">💰</div><span style="background:rgba(255,255,255,0.2);color:#fff;font-size:0.6rem;font-weight:600;padding:2px 8px;border-radius:100px">#2</span><h3 style="color:#fff;font-size:0.92rem;font-weight:800;line-height:1.3;margin-top:10px">대출 시급한<br>사람</h3></div>
        <div style="padding:12px 14px"><span style="font-size:0.68rem;color:#999">은행 · 핀테크 · 보험</span></div>
      </div>
      <div style="border-radius:16px;overflow:hidden;border:1px solid #f0f0f0;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
        <div style="background:linear-gradient(135deg,#4a1942,#6b3fa0);padding:28px 20px;position:relative"><div style="position:absolute;top:10px;right:14px;font-size:2.4rem;opacity:0.15">🏠</div><span style="background:rgba(255,255,255,0.2);color:#fff;font-size:0.6rem;font-weight:600;padding:2px 8px;border-radius:100px">#3</span><h3 style="color:#fff;font-size:0.92rem;font-weight:800;line-height:1.3;margin-top:10px">전세대출<br>규제 영향권</h3></div>
        <div style="padding:12px 14px"><span style="font-size:0.68rem;color:#999">은행 · 부동산 · 보험</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⛳ 골프", key="go_golf"):
            st.session_state.view = "detail_golf"
            st.rerun()
    with col2:
        if st.button("💰 대출", key="go_finance"):
            st.session_state.view = "detail_finance"
            st.rerun()
    with col3:
        if st.button("🏠 전세", key="go_gold"):
            st.session_state.view = "detail_gold"
            st.rerun()

    with col4:
        if st.button("⛳ '반려동물 관심자' 타겟팅 ", key="go_pet2"):
            st.session_state.view = "detail_pet"
            st.rerun()
    st.markdown('<div class="footer">오늘의 오디언스 · by IGAWorks · © 2026</div>', unsafe_allow_html=True)
