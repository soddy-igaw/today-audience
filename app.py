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

    <div class="note-end">오늘의 오디언스 #2 · 다음 달 이자가 올라가는 사람 · by IGAWorks</div>
    """
    st.markdown(finance_html, unsafe_allow_html=True)

elif st.session_state.view == "detail_gold":
    if st.button("← 돌아가기", key="back_gold"):
        st.session_state.view = "feed"
        st.rerun()

    gold_html = """
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
      <p class="lead">'금 투자자' 타겟팅 금지!<br>금괴 품절 이후,<br>금 앱을 처음 깐 사람</p>

      <div class="quote">"금에 관심 있는 사람과<br>금에 돈을 넣을 사람은<br>완전히 다른 사람이에요."</div>

      <p>대형 증권사 마케터 P씨의 말입니다.</p>

      <p>금값이 역대 최고를 찍고 있습니다. 1돈에 84만 원. 2025년 한 해 동안 금값은 70% 올랐어요. 1979년 이후 최고 상승률입니다.</p>

      <p>은행 금괴는 품절입니다. 한국조폐공사는 2025년 2월 금괴 제조를 중단했고, 10월에는 아예 전 제품 판매를 멈췄어요. 신한은행은 1kg 금괴 판매를 중지했습니다.</p>

      <p>그런데 금을 못 사게 된 사람들이 <strong>다른 곳으로 몰리고 있습니다.</strong></p>

      <p>2026년 1월, 국내 금 ETF 유입액 7900억 원. 5대 은행 금통장 잔액 2조 1700억 원. KRX 금 거래 개인 계좌 145만 개.</p>

      <p>모든 증권사가 이 사람들을 잡으려고 합니다. 문제는 <strong>"금 투자자"로 타겟하면 전환이 안 나온다</strong>는 것.</p>
    </div>

    <div class="sig-box">
      <div class="sig-label">P씨의 고민</div>
      <p>"금 ETF 광고 CTR은 다른 상품의 2배예요. 클릭은 엄청 나요. 그런데 실제 계좌 개설은 1%도 안 됩니다. 다른 ETF는 3~4%인데."<br><br>"트래픽을 뜯어보니까, 대부분 '금 1돈 얼마', '오늘 금값' 검색하다 들어온 사람이에요. 금값이 궁금한 거지, 금을 사려는 게 아닌 거죠."<br><br>"그물을 바다에 던지는데, 잡히는 건 해파리뿐인 겁니다."</p>
    </div>

    <div class="note-body">
      <p>P씨에게 물었습니다. "그러면 진짜 금을 살 사람은 어떻게 구분하나요?"</p>

      <p>P씨는 모른다고 했어요. <strong>"금 관심자" 안에서 진짜 투자할 사람을 걸러낼 방법이 없다</strong>는 게 문제였습니다.</p>

      <p>우리는 앱 데이터에서 힌트를 찾았습니다.</p>
    </div>

    <div class="sig-box">
      <div class="sig-label">우리가 발견한 것</div>
      <p>금 거래 앱을 처음 설치한 사람은 세 부류로 나뉩니다.<br>그리고 <strong>설치 후 3일간의 행동</strong>으로 구분할 수 있습니다.<br><br>→ 금 거래앱(금방/한국금거래소/KRX금시장) <strong>첫 설치</strong><br>→ 설치 후 3일 내 <strong>매일 실행</strong> vs <strong>1회 실행 후 방치</strong><br>→ 증권앱 <strong>기존 사용자</strong> 여부<br>→ 금값 급등 시점과 설치 타이밍의 <strong>상관관계</strong></p>
    </div>

    <div class="note-body">
      <p>같은 "금 앱 설치자"인데, 전부 다른 사람입니다.</p>
    </div>

    <div style="overflow-x:auto;margin:32px 0">
      <table style="width:100%;border-collapse:collapse;font-size:0.82rem">
        <tr style="border-bottom:2px solid #e0e0e0">
          <th style="text-align:left;padding:12px 8px;color:#999;font-weight:600"></th>
          <th style="text-align:left;padding:12px 8px;color:#999;font-weight:600">기존 금 투자자</th>
          <th style="text-align:left;padding:12px 8px;color:#6366f1;font-weight:600">FOMO 진입자</th>
          <th style="text-align:left;padding:12px 8px;color:#999;font-weight:600">관망형</th>
        </tr>
        <tr style="border-bottom:1px solid #f0f0f0">
          <td style="padding:10px 8px;color:#888">금 앱</td>
          <td style="padding:10px 8px;color:#888">6개월+ 전 설치</td>
          <td style="padding:10px 8px;color:#333;font-weight:500">최근 30일 내 첫 설치</td>
          <td style="padding:10px 8px;color:#888">최근 30일 내 첫 설치</td>
        </tr>
        <tr style="border-bottom:1px solid #f0f0f0">
          <td style="padding:10px 8px;color:#888">설치 후 3일</td>
          <td style="padding:10px 8px;color:#888">꾸준히 사용</td>
          <td style="padding:10px 8px;color:#333;font-weight:500">매일 실행</td>
          <td style="padding:10px 8px;color:#888">1회 실행 후 방치</td>
        </tr>
        <tr style="border-bottom:1px solid #f0f0f0">
          <td style="padding:10px 8px;color:#888">증권앱</td>
          <td style="padding:10px 8px;color:#888">있거나 없거나</td>
          <td style="padding:10px 8px;color:#333;font-weight:500">기존 사용자 (주식→금 이동)</td>
          <td style="padding:10px 8px;color:#888">없는 경우 많음</td>
        </tr>
        <tr style="border-bottom:1px solid #f0f0f0">
          <td style="padding:10px 8px;color:#888">설치 타이밍</td>
          <td style="padding:10px 8px;color:#888">금값과 무관</td>
          <td style="padding:10px 8px;color:#333;font-weight:500">금값 급등 직후</td>
          <td style="padding:10px 8px;color:#888">금값 급등 직후</td>
        </tr>
        <tr>
          <td style="padding:10px 8px;color:#888">전환 가능성</td>
          <td style="padding:10px 8px;color:#888">이미 투자 중</td>
          <td style="padding:10px 8px;color:#6366f1;font-weight:700">극상</td>
          <td style="padding:10px 8px;color:#888">낮음 (교육 필요)</td>
        </tr>
      </table>
    </div>

    <div class="note-body">
      <p>P씨에게 이 구분법을 보여줬더니 이렇게 말했어요.</p>

      <div class="quote">"우리가 지금까지 설치자를 전부 '관심자' 한 덩어리로 봤는데,<br>설치 후 3일 데이터만 봐도 나뉘는 거네요.<br><br>FOMO 진입자한테는 '지금 안 사면 더 오릅니다'가 먹히고,<br>관망형한테는 '소액부터 시작해보세요'가 먹히겠네요."</div>

      <p>맞습니다. 같은 금 앱 설치자인데, <strong>메시지가 완전히 달라져야 합니다.</strong></p>
    </div>

    <div class="sig-box">
      <div class="sig-label">DMP에서 잡는 법 (앱 데이터만으로)</div>
      <p><strong>[FOMO 진입자 — 전환 가능성 극상]</strong><br>금 거래앱 첫 설치 (30일 내)<br>+ 설치 후 3일 내 매일 실행<br>+ 증권앱 기존 사용자<br>+ 금값 급등 시점 전후 설치<br><br><strong>[관망형 — 교육 콘텐츠 타겟]</strong><br>금 거래앱 첫 설치 (30일 내)<br>+ 설치 후 1회 실행, 이후 미실행<br>+ 증권앱 미보유<br><br><em>* 앱 내부 거래 데이터(매수/매도)는 DMP로 볼 수 없습니다.<br>설치 + 실행 빈도 + 타이밍으로 의도를 추정합니다.</em></p>
    </div>

    <div class="ind-grid">
      <div class="ind-card"><div class="ind-title">📈 증권사</div><div class="ind-desc">FOMO 진입자 → "금 ETF, 1000원부터" 즉시 전환 유도</div></div>
      <div class="ind-card"><div class="ind-title">🏦 은행</div><div class="ind-desc">관망형 → "금통장 소액 시작" 교육형 콘텐츠</div></div>
      <div class="ind-card"><div class="ind-title">🤖 로보어드바이저</div><div class="ind-desc">"금+채권+달러 자동 분산" 안전자산 포트폴리오</div></div>
      <div class="ind-card"><div class="ind-title">📚 재테크 교육</div><div class="ind-desc">"금값 역대 최고, 지금 사도 될까?" 콘텐츠 마케팅</div></div>
    </div>

    <div class="insight">
      <div class="ins-label">💡 KEY INSIGHT</div>
      <p>"금 투자자"는 오디언스가 아닙니다.<br><br>금 앱을 <strong>깔고 매일 여는 사람</strong>과<br>금 앱을 <strong>깔고 한 번 보고 닫은 사람</strong>은<br>완전히 다른 사람입니다.<br><br><strong>설치 후 3일</strong>이 오디언스를 만듭니다.<br><br>금괴는 품절이지만, 금에 관심 있는 사람은 넘칩니다.<br>그 안에서 진짜 투자할 사람을 찾는 게 광고주의 숙제입니다.</p>
    </div>

    <div class="note-end">오늘의 오디언스 #3 · 금괴 품절 이후, 금 앱을 처음 깐 사람 · by IGAWorks</div>
    """
    st.markdown(gold_html, unsafe_allow_html=True)

else:
    # ===== MAIN PAGE =====
    st.markdown("""
    <div class="nav"><div>
      <div class="nav-logo"><span>오늘의</span> 오디언스</div>
      <div class="nav-sub">by IGAWorks</div>
    </div></div>

    <!-- Hero -->
    <div style="padding:48px 0 40px;text-align:center">
      <p style="font-size:0.75rem;color:#6366f1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px">AUDIENCE IDEA BANK</p>
      <h1 style="font-size:2.2rem;font-weight:900;color:#111;line-height:1.25;letter-spacing:-1px;margin-bottom:16px">다음 캠페인,<br>누구한테 해야 하지?</h1>
      <p style="color:#888;font-size:0.92rem;line-height:1.7">광고주가 미처 생각하지 못한 타겟을 매일 발견하는 곳.<br>트렌드를 자동으로 읽고, 행동 시그널을 조합해<br>아직 아무도 안 쓰는 오디언스를 제안합니다.</p>
    </div>

    <div style="border-top:1px solid #f0f0f0;margin:8px 0 32px"></div>

    <!-- TODAY'S AUDIENCE (Golf) -->
    <p style="font-size:0.7rem;color:#6366f1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:20px">🎯 오늘의 오디언스</p>

    <div style="background:#fff;border:1px solid #e8e8e8;border-radius:20px;padding:36px;margin-bottom:40px;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 8px 30px rgba(0,0,0,0.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px">
        <div style="width:36px;height:36px;border-radius:50%;background:#6366f1;display:flex;align-items:center;justify-content:center;color:#fff;font-size:0.75rem;font-weight:700">IG</div>
        <div>
          <div style="font-size:0.82rem;font-weight:600;color:#111">IGAWorks 오디언스 랩</div>
          <div style="font-size:0.7rem;color:#bbb">2026.04.12</div>
        </div>
        <div style="margin-left:auto;background:#6366f1;color:#fff;font-size:0.7rem;font-weight:700;padding:4px 14px;border-radius:100px">⛳ TODAY</div>
      </div>
      <h2 style="font-size:1.4rem;font-weight:900;color:#111;line-height:1.3;margin-bottom:12px">'골프 관심자' 타겟팅 금지!<br>접대 골프 입문자의 숨겨진 구매 시그널</h2>
      <p style="color:#666;font-size:0.92rem;line-height:1.7;margin-bottom:16px">"드라이버를 사는 게 아니라, 창피를 안 당할 보험을 사는 겁니다." 한국 골프 인구 564만 명 중, 회사 때문에 입문한 30대의 행동 패턴은 완전히 다릅니다.</p>
      <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:16px">
        <span style="background:#f0eeff;color:#6366f1;font-size:0.72rem;font-weight:500;padding:4px 12px;border-radius:100px">골프 용품</span>
        <span style="background:#f0eeff;color:#6366f1;font-size:0.72rem;font-weight:500;padding:4px 12px;border-radius:100px">골프웨어</span>
        <span style="background:#f0eeff;color:#6366f1;font-size:0.72rem;font-weight:500;padding:4px 12px;border-radius:100px">골프 레슨</span>
        <span style="background:#f0eeff;color:#6366f1;font-size:0.72rem;font-weight:500;padding:4px 12px;border-radius:100px">프리미엄 카드</span>
      </div>
      <div style="display:flex;align-items:center;gap:16px;padding-top:16px;border-top:1px solid #f0f0f0">
        <span style="font-size:0.78rem;color:#888">추정 모수 <strong style="color:#6366f1">564만 명</strong> 중 접대 입문자</span>
        <span style="margin-left:auto;color:#6366f1;font-size:0.85rem;font-weight:600">읽기 →</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⛳ 접대 골프를 시작한 30대 — 읽기", key="go_golf"):
        st.session_state.view = "detail_golf"
        st.rerun()

    # Gallery
    st.markdown("""
    <p style="font-size:0.7rem;color:#6366f1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin:8px 0 20px">📚 오디언스 갤러리</p>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:40px">

      <!-- Card: 대출 -->
      <div style="background:#fff;border:1px solid #f0f0f0;border-radius:16px;padding:24px;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
          <span style="background:#f0eeff;color:#6366f1;font-size:0.65rem;font-weight:700;padding:3px 10px;border-radius:100px">💰 #2</span>
          <span style="font-size:0.68rem;color:#bbb">2026.04.10</span>
        </div>
        <h3 style="font-size:1.05rem;font-weight:800;color:#111;line-height:1.3;margin-bottom:8px">'대출 관심자' 타겟팅 금지!<br>다음 달 이자가 올라가는 사람</h3>
        <p style="color:#999;font-size:0.82rem;line-height:1.5;margin-bottom:12px">앱 1개 vs 3개. 시급함의 크기가 오디언스를 만든다.</p>
        <div style="display:flex;gap:4px;flex-wrap:wrap">
          <span style="background:#f8f8f8;color:#999;font-size:0.68rem;padding:3px 8px;border-radius:100px">은행</span>
          <span style="background:#f8f8f8;color:#999;font-size:0.68rem;padding:3px 8px;border-radius:100px">핀테크</span>
          <span style="background:#f8f8f8;color:#999;font-size:0.68rem;padding:3px 8px;border-radius:100px">보험</span>
        </div>
      </div>

      <!-- Card: 금 -->
      <div style="background:#fff;border:1px solid #f0f0f0;border-radius:16px;padding:24px;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
          <span style="background:#f0eeff;color:#6366f1;font-size:0.65rem;font-weight:700;padding:3px 10px;border-radius:100px">🥇 #3</span>
          <span style="font-size:0.68rem;color:#bbb">2026.04.12</span>
        </div>
        <h3 style="font-size:1.05rem;font-weight:800;color:#111;line-height:1.3;margin-bottom:8px">'금 투자자' 타겟팅 금지!<br>금괴 품절 이후 앱을 처음 깐 사람</h3>
        <p style="color:#999;font-size:0.82rem;line-height:1.5;margin-bottom:12px">설치 후 3일이 오디언스를 만든다. FOMO vs 관망.</p>
        <div style="display:flex;gap:4px;flex-wrap:wrap">
          <span style="background:#f8f8f8;color:#999;font-size:0.68rem;padding:3px 8px;border-radius:100px">증권사</span>
          <span style="background:#f8f8f8;color:#999;font-size:0.68rem;padding:3px 8px;border-radius:100px">은행</span>
          <span style="background:#f8f8f8;color:#999;font-size:0.68rem;padding:3px 8px;border-radius:100px">로보어드바이저</span>
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💰 대출 — 읽기", key="go_finance"):
            st.session_state.view = "detail_finance"
            st.rerun()
    with col2:
        if st.button("🥇 금 — 읽기", key="go_gold"):
            st.session_state.view = "detail_gold"
            st.rerun()

    st.markdown('<div class="footer">오늘의 오디언스 · by IGAWorks · © 2026</div>', unsafe_allow_html=True)
