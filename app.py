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
    <div style="padding:20px 0">
      <div class="nav"><div>
        <div class="nav-logo"><span>오늘의</span> 오디언스</div>
        <div class="nav-sub">by IGAWorks</div>
      </div></div>

      <div style="padding:48px 0 20px">
        <div style="font-size:0.72rem;color:#6366f1;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:24px">💰 오늘의 오디언스 #2</div>
        <h1 style="font-size:2.6rem;font-weight:900;color:#111;line-height:1.25;letter-spacing:-1.5px;margin-bottom:32px">'대출 관심자' 타겟팅 금지!<br>다음 달 이자가<br>올라가는 사람</h1>
        <p style="color:#555;font-size:1.15rem;line-height:2;margin-bottom:28px">"금리가 내려갔다는데,<br>&nbsp;&nbsp;나는 왜 아직 4%대를 내고 있지?"</p>
        <p style="color:#888;font-size:0.92rem;line-height:1.8;margin-bottom:20px">부동산 커뮤니티 글이 아닙니다.<br>대출 만기 3개월 전,<br>새벽 1시에 금리 비교앱을 깐 사람의<br>실제 행동 패턴이죠.</p>
        <p style="color:#888;font-size:0.92rem;line-height:1.8;margin-bottom:20px">모든 은행이<br>"대출 관심자"를 타겟합니다.<br><br>문제는 이 안에<br>"언젠가 갈아타야지" 하는 사람과<br><strong style="color:#111">"이번 달 안에 안 바꾸면 매달 30만 원을 더 내는 사람"</strong>이<br>같이 섞여 있다는 것.</p>
        <p style="color:#111;font-size:1.3rem;font-weight:800;line-height:1.5;margin:32px 0">시급한 사람은<br>행동이 완전히 다릅니다.</p>

        <div style="background:#f5f3ff;border-radius:12px;padding:28px 32px;margin:32px 0">
          <p style="color:#6366f1;font-size:0.75rem;font-weight:700;letter-spacing:1.5px;margin-bottom:16px">BEHAVIOR SIGNALS</p>
          <p style="color:#333;font-size:0.95rem;line-height:1.9">→ 대출 비교앱 <strong>3개 이상</strong> 동시 설치 (7일 내)<br>→ 설치 후 <strong>매일 반복 접속</strong><br>→ "대출 갈아타기" "금리 인하 요구권" 콘텐츠 소비<br>→ 기존 은행앱 접속 빈도 <strong>감소</strong> (떠나려는 시그널)<br>→ 새벽/출퇴근 시간대 집중 탐색</p>
        </div>

        <p style="color:#888;font-size:0.92rem;line-height:1.8;margin-bottom:20px">앱을 1개 깔고 가끔 보는 사람은<br>"언젠가" 갈아탈 사람입니다.<br><br>앱을 <strong style="color:#111">3개 깔고 매일 여는 사람</strong>은<br><strong style="color:#111">지금 당장</strong> 갈아탈 사람입니다.</p>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:20px 0">
        <div style="background:#f8f8f8;border-radius:12px;padding:20px">
          <h4 style="font-size:0.75rem;color:#999;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px">대출 구경꾼</h4>
          <p style="font-size:0.88rem;color:#888;line-height:1.8">앱 1개 설치<br>가끔 접속<br>"나중에 해야지"<br>광고 무시<br>전환율 극히 낮음</p>
        </div>
        <div style="background:#f5f3ff;border-radius:12px;padding:20px">
          <h4 style="font-size:0.75rem;color:#6366f1;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px">대출 시급한 사람</h4>
          <p style="font-size:0.88rem;color:#333;line-height:1.8">앱 3개+ 동시 설치<br>매일 반복 접속<br>"이번 달 안에"<br>금리 숫자에 즉시 반응<br>전환율 극상</p>
        </div>
      </div>

      <p style="color:#888;font-size:0.92rem;line-height:1.8;margin:28px 0">모든 은행이 "대출 관심자"를 타겟하고 있습니다.<br>그래서 단가가 비싸고 전환이 안 나옵니다.<br><br><strong style="color:#111">"이번 달 안에 갈아타야 하는 사람"은<br>아무도 안 잡고 있습니다.</strong><br><br>왜?<br>이 세그먼트가 존재하는지 몰랐으니까요.</p>

      <div style="background:#f5f3ff;border-radius:12px;padding:28px 32px;margin:32px 0">
        <p style="color:#6366f1;font-size:0.75rem;font-weight:700;letter-spacing:1.5px;margin-bottom:16px">DMP에서 잡는 법</p>
        <p style="color:#333;font-size:0.88rem;line-height:1.9"><strong>[대출 시급 유저]</strong><br>대출 비교앱 3개+ (7일 내 동시 설치)<br>+ 설치 후 일 1회 이상 반복 접속<br>+ 기존 은행앱 접속 빈도 감소<br>+ "갈아타기" "금리 비교" 콘텐츠 소비</p>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:32px 0">
        <div style="background:#f8f8f8;border-radius:10px;padding:20px"><p style="font-size:0.82rem;font-weight:700;color:#111;margin-bottom:6px">🏦 은행/저축은행</p><p style="font-size:0.8rem;color:#888;line-height:1.4">대환대출 "지금 갈아타면 월 OO만 원 절약" 소구</p></div>
        <div style="background:#f8f8f8;border-radius:10px;padding:20px"><p style="font-size:0.82rem;font-weight:700;color:#111;margin-bottom:6px">📱 핀테크</p><p style="font-size:0.8rem;color:#888;line-height:1.4">대출 비교 서비스 신규 유저 확보</p></div>
        <div style="background:#f8f8f8;border-radius:10px;padding:20px"><p style="font-size:0.82rem;font-weight:700;color:#111;margin-bottom:6px">🛡️ 보험</p><p style="font-size:0.8rem;color:#888;line-height:1.4">대출 연계 보험 상품 타겟팅</p></div>
        <div style="background:#f8f8f8;border-radius:10px;padding:20px"><p style="font-size:0.82rem;font-weight:700;color:#111;margin-bottom:6px">💳 카드사</p><p style="font-size:0.8rem;color:#888;line-height:1.4">대출 이자 캐시백 카드 전환</p></div>
      </div>

      <div style="background:#111;border-radius:12px;padding:28px 32px;margin:32px 0">
        <p style="color:#a5b4fc;font-size:0.75rem;font-weight:700;letter-spacing:1.5px;margin-bottom:12px">💡 KEY INSIGHT</p>
        <p style="color:#fff;font-size:1.05rem;line-height:1.7;font-weight:500">"대출 관심자"는 오디언스가 아닙니다.<br><br>앱 <strong>1개</strong> 깔고 가끔 보는 사람과<br>앱 <strong>3개</strong> 깔고 매일 여는 사람은<br>완전히 다른 사람입니다.<br><br><strong>시급함의 크기</strong>가 오디언스를 만듭니다.</p>
      </div>

      <p style="color:#bbb;font-size:0.8rem;margin-top:40px;padding-top:20px;border-top:1px solid #eee">오늘의 오디언스 #2 · 다음 달 이자가 올라가는 사람 · by IGAWorks</p>
    </div>
    """
    st.markdown(finance_html, unsafe_allow_html=True)

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

    <!-- Divider -->
    <div style="border-top:1px solid #f0f0f0;margin:8px 0 32px"></div>

    <!-- Feed label -->
    <p style="font-size:0.7rem;color:#6366f1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:20px">오늘의 노트</p>
    """, unsafe_allow_html=True)

    # ===== NOTE CARD #1 (Golf) =====
    st.markdown("""
    <div style="background:#fff;border:1px solid #f0f0f0;border-radius:16px;padding:28px;margin-bottom:16px;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
        <div style="width:32px;height:32px;border-radius:50%;background:#6366f1;display:flex;align-items:center;justify-content:center;color:#fff;font-size:0.7rem;font-weight:700">IG</div>
        <div>
          <div style="font-size:0.78rem;font-weight:600;color:#111">IGAWorks 오디언스 랩</div>
          <div style="font-size:0.68rem;color:#bbb">2026.04.11</div>
        </div>
        <div style="margin-left:auto;background:#f0eeff;color:#6366f1;font-size:0.68rem;font-weight:700;padding:3px 10px;border-radius:100px">⛳ #1</div>
      </div>
      <h3 style="font-size:1.15rem;font-weight:800;color:#111;line-height:1.35;margin-bottom:10px">'골프 관심자' 타겟팅 금지!<br>접대 골프 입문자의 숨겨진 구매 시그널</h3>
      <p style="color:#888;font-size:0.88rem;line-height:1.6;margin-bottom:14px">"드라이버를 사는 게 아니라, 창피를 안 당할 보험을 사는 겁니다." 회사 때문에 골프에 입문한 30대의 행동 패턴을 분석했습니다.</p>
      <div style="display:flex;gap:6px;flex-wrap:wrap">
        <span style="background:#f8f8f8;color:#888;font-size:0.72rem;padding:4px 10px;border-radius:100px">골프 용품</span>
        <span style="background:#f8f8f8;color:#888;font-size:0.72rem;padding:4px 10px;border-radius:100px">골프웨어</span>
        <span style="background:#f8f8f8;color:#888;font-size:0.72rem;padding:4px 10px;border-radius:100px">프리미엄 카드</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⛳ 접대 골프를 시작한 30대 — 읽기", key="go_golf"):
        st.session_state.view = "detail_golf"
        st.rerun()

    # ===== NOTE CARD #2 (Finance) =====
    st.markdown("""
    <div style="background:#fff;border:1px solid #f0f0f0;border-radius:16px;padding:28px;margin-bottom:16px;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
        <div style="width:32px;height:32px;border-radius:50%;background:#6366f1;display:flex;align-items:center;justify-content:center;color:#fff;font-size:0.7rem;font-weight:700">IG</div>
        <div>
          <div style="font-size:0.78rem;font-weight:600;color:#111">IGAWorks 오디언스 랩</div>
          <div style="font-size:0.68rem;color:#bbb">2026.04.10</div>
        </div>
        <div style="margin-left:auto;background:#f0eeff;color:#6366f1;font-size:0.68rem;font-weight:700;padding:3px 10px;border-radius:100px">💰 #2</div>
      </div>
      <h3 style="font-size:1.15rem;font-weight:800;color:#111;line-height:1.35;margin-bottom:10px">'대출 관심자' 타겟팅 금지!<br>다음 달 이자가 올라가는 사람</h3>
      <p style="color:#888;font-size:0.88rem;line-height:1.6;margin-bottom:14px">앱 1개 깔고 가끔 보는 사람과, 3개 깔고 매일 여는 사람은 완전히 다릅니다. 시급함의 크기가 오디언스를 만듭니다.</p>
      <div style="display:flex;gap:6px;flex-wrap:wrap">
        <span style="background:#f8f8f8;color:#888;font-size:0.72rem;padding:4px 10px;border-radius:100px">은행</span>
        <span style="background:#f8f8f8;color:#888;font-size:0.72rem;padding:4px 10px;border-radius:100px">핀테크</span>
        <span style="background:#f8f8f8;color:#888;font-size:0.72rem;padding:4px 10px;border-radius:100px">보험</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💰 다음 달 이자가 올라가는 사람 — 읽기", key="go_finance"):
        st.session_state.view = "detail_finance"
        st.rerun()

    # ===== COMING SOON CARDS =====
    st.markdown("""<p style="font-size:0.7rem;color:#6366f1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin:40px 0 20px;padding-top:32px;border-top:1px solid #f0f0f0">공개 예정 노트</p>""", unsafe_allow_html=True)

    UPCOMING = [
        ("#3", "⛳", "스크린에서 필드로 넘어가는 여성 골퍼", "스포츠/레저", "D-5"),
        ("#4", "🏦", "전세 만기 D-90, 지금 움직이는 사람", "금융", "D-12"),
        ("#5", "💍", "결혼 준비 커플의 동시다발 소비", "라이프 전환", "D-19"),
        ("#6", "👶", "첫 아이 출산 준비 부부", "라이프 전환", "D-26"),
        ("#7", "👗", "콰이어트 럭셔리에 눈뜬 30대", "패션", "D-33"),
        ("#8", "👟", "러닝에 빠진 패션 피플", "패션", "D-40"),
    ]

    for num, emoji, title, cat, dday in UPCOMING:
        st.markdown(f"""
        <div style="background:#fafafa;border:1px solid #f5f5f5;border-radius:12px;padding:20px 24px;margin-bottom:10px;opacity:0.5;display:flex;align-items:center;gap:14px">
          <div style="font-size:1.4rem">{emoji}</div>
          <div style="flex:1">
            <div style="font-size:0.68rem;color:#6366f1;font-weight:600;letter-spacing:1px;margin-bottom:2px">{cat} · 오늘의 오디언스 {num}</div>
            <div style="font-size:0.92rem;font-weight:700;color:#111">{title}</div>
          </div>
          <div style="background:#f0eeff;color:#6366f1;font-size:0.68rem;font-weight:700;padding:3px 10px;border-radius:100px;white-space:nowrap">{dday}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="footer">오늘의 오디언스 · by IGAWorks · © 2026</div>', unsafe_allow_html=True)
