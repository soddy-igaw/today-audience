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

<p class="lead">'인테리어 관심자' 타겟팅 금지!<br>
[3개월 내 실제 이사 준비 유저]</p>

<div class="quote">
"인테리어 앱 설치자들에게 광고했는데 클릭률은 높아요. 근데 전환은 왜 이렇게 낮죠? 다들 구경만 하는 것 같아요."
<span>— K씨, 홈퍼니싱 브랜드 마케팅 매니저</span>
</div>

**"인테리어에 관심 있는 사람"**

이보다 뭉뚱그린 타겟이 또 있을까.

인테리어 관심자라는 건 누구인가?
오늘 오후에 심심해서 집꾸미기 앱 훑어본 직장인?
3년 후 결혼 준비하며 레퍼런스 모으는 대학생?
아니면 다음 달 이사 앞두고 절박하게 업체 알아보는 실수요자?

전부 다 "인테리어 관심자"다.
하지만 광고비를 쓸 가치가 있는 건 마지막 한 명뿐.

나머지는 그냥 구경꾼이다.
예쁜 사진 보며 "나중에 내 집 꾸밀 때..." 라고 상상하는.

<div class="sig-box">
<div class="sig-label">BEHAVIOR SIGNALS</div>
직방 + 다방 + 호갱노노<br>
3개 앱 동시 설치율 78%<br><br>
최근 30일 내 부동산 앱<br>
주 3회 이상 접속<br><br>
부동산 앱 첫 설치 후<br>
3개월 내 인테리어 앱 추가 설치<br><br>
주말 오전 10-12시<br>
부동산 앱 집중 사용<br><br>
인테리어 앱보다<br>
부동산 앱 사용 빈도 2배 이상
</div>

**진짜 이사 준비하는 사람들은 패턴이 다르다.**

먼저 부동산 앱부터 깐다.
직방, 다방, 호갱노노를 동시에.
하나로는 안 되니까. 놓치는 매물이 있을까 봐.

그다음에야 인테리어 앱을 깐다.
집을 구한 다음 꾸미는 거니까.
순서가 명확하다.

**반대로 구경꾼들은 인테리어 앱만 있다.**

집도 없으면서 꾸밀 생각부터 한다.
현실적이지 않다는 뜻.
당장 지갑을 열 확률이 낮다.

<div class="cmp-grid">
<div class="cmp-card cmp-left">
<h4>🏠 구경꾼</h4>
인테리어 앱만 설치<br>
부동산 앱 사용 경험 無<br>
주로 평일 저녁 시간대 접속<br>
앱 내에서 '저장'만 반복<br>
설치 후 3개월 넘게 앱만 유지<br>
소셜 공유 기능 자주 사용<br>
트렌드성 콘텐츠 위주 소비<br>
실제 구매 전환율 2% 미만
</div>
<div class="cmp-card cmp-right">
<h4>🔧 실제 이사 준비자</h4>
부동산 앱 → 인테리어 앱 순차 설치<br>
3개 이상 부동산 앱 동시 보유<br>
주말 오전 부동산 앱 집중 사용<br>
검색보다 '실제 매물' 위주 탐색<br>
앱 설치 후 3개월 내 활동 집중<br>
가격 정보에 민감한 반응<br>
실용성 위주 콘텐츠 선호<br>
실제 구매 전환율 15% 이상
</div>
</div>

<div class="sig-box">
<div class="sig-label">DMP에서 잡는 법</div>
1단계: 직방+다방+호갱노노 동시 설치<br>
2단계: 최근 30일 부동산 앱 사용 빈도 주 3회↑<br>
3단계: 부동산 앱 설치 이후 인테리어 앱 추가<br>
4단계: 주말 오전 부동산 앱 활성 패턴<br>
5단계: 전체 기간 3개월 이내 압축
</div>

<div class="ind-grid">
<div class="ind-card">
<div class="ind-title">🏡 인테리어 시공</div>
<div class="ind-desc">실제 이사 앞둔 사람들만 타겟. 견적 문의율 300% 향상 기대. 시공 일정 맞춰 광고 집행.</div>
</div>
<div class="ind-card">
<div class="ind-title">🛋️ 가구 브랜드</div>
<div class="ind-desc">새 집 가구 구매 적기 포착. 기존 관심자 대비 구매 전환 5배 높음. 배송 일정까지 고려한 타이밍.</div>
</div>
<div class="ind-card">
<div class="ind-title">🏠 부동산 중개</div>
<div class="ind-desc">이미 적극적으로 집 알아보는 층. 경쟁업체 이용자도 함께 공략. 계약 성사율 대폭 상승.</div>
</div>
<div class="ind-card">
<div class="ind-title">🚛 이사 서비스</div>
<div class="ind-desc">이사 확정 전 미리 접근. 예약률 최대 400% 증가. 성수기 대비한 선제적 마케팅 가능.</div>
</div>
</div>

<div class="insight">
<div class="ins-label">KEY INSIGHT</div>
진짜 고객은 꿈꾸지 않는다. 준비한다.<br>
인테리어 관심보다 이사 준비 신호가 100배 정확하다.
</div>

**광고 카피도 달라져야 한다.**

❌ **기존**: "꿈꾸던 인테리어를 현실로"
✅ **새 타겟**: "이사 한 달 전 미리 준비하세요"

❌ **기존**: "트렌디한 홈스타일링"  
✅ **새 타겟**: "새 집 입주 일정에 맞춰 시공"

❌ **기존**: "인테리어 영감을 찾아보세요"
✅ **새 타겟**: "계약금 낸 분들을 위한 특가"

구경꾼에게는 꿈을 팔았다.
실수요자에게는 솔루션을 판다.

**K씨와의 두 번째 대화.**

"정말 부동산 앱 쓰는 사람들이 더 잘 살까요?"

**당연하다.**

집 구하는 사람이 인테리어에 돈 쓸 확률이 높다.
이미 목적이 명확하니까.
예산도 책정해둔 상태고.

"그럼 타겟 사이즈가 많이 줄어들지 않나요?"

**줄어든다.**

400만 명에서 50만 명으로.
하지만 50만 명이 400만 명보다 값지다.
구매 확률이 8배 높으니까.

"언제부터 이 타겟으로 잡아야 할까요?"

**지금 당장.**

이사철은 따로 없다. 연중 계속이다.
다만 3-4월, 8-9월에 더 집중될 뿐.
미리 준비하는 게 좋다.

<div style="background:#111; color:#fff; padding:24px; border-radius:8px; margin:24px 0;">
<h3 style="color:#00ff88; margin:0 0 16px 0;">AUDIENCE CARD</h3>
<h4 style="margin:0 0 8px 0;">3개월 내 실제 이사 준비 유저</h4>
<p style="margin:0 0 16px 0; opacity:0.8;">추정 모수: 45만~65만 명</p>

<div style="margin:16px 0;">
<strong style="color:#00ff88;">추천 업종</strong><br>
인테리어 시공, 가구 브랜드, 부동산 중개, 이사 서비스
</div>

<div style="margin:16px 0;">
<strong style="color:#00ff88;">핵심 시그널</strong><br>
부동산 3개 앱 동시 설치 + 인테리어 앱 후순위 추가 + 주말 오전 집중 사용
</div>

<div style="margin:16px 0;">
<strong style="color:#00ff88;">메시지</strong><br>
"이사 일정 맞춰 미리 준비" / "새 집 입주 전 완벽 세팅" / "계약 완료자 특별 혜택"
</div>
</div>

<div class="note-end">
**마지막 조언.**

인테리어 관심자 타겟팅은 이제 그만.
너무 넓다. 너무 뭉뚱그려져 있다.

실제로 이사 준비하는 사람들을 찾아라.
부동산 앱 사용 패턴이 가장 정확한 신호다.

그들은 이미 예산을 정해뒀다.
시기도 정해뒀다.
당신의 서비스만 기다리고 있다.

**2026년 4월 14일**<br>
**IGAWorks 오늘의 오디언스**
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
        <h2 style="color:#fff;font-size:1.5rem;font-weight:900;line-height:1.3;margin-top:16px">'인테리어 관심자' 타겟팅 금지!</h2>
        <p style="color:rgba(255,255,255,0.7);font-size:0.92rem;line-height:1.6;margin-top:8px">[3개월 내 실제 이사 준비 유저]</p>
      </div>
      <div style="padding:20px 24px;display:flex;align-items:center;justify-content:space-between">
        <span style="font-size:0.78rem;color:#888">부동산 오디언스 인사이트</span>
        <span style="color:#6366f1;font-size:0.82rem;font-weight:600">읽기 →</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 [3개월 내 실제 이사 준비 유저]", key="go_new5"):
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
        if st.button("🐾 반려동물", key="go_pet2"):
            st.session_state.view = "detail_pet"
            st.rerun()

    st.markdown('<div class="footer">오늘의 오디언스 · by IGAWorks · © 2026</div>', unsafe_allow_html=True)
