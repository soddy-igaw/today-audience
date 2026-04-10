import streamlit as st

st.set_page_config(page_title="오늘의 오디언스 — IGAWorks", page_icon="🎯", layout="wide")

if "view" not in st.session_state:
    st.session_state.view = "feed"

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
.stApp { background:#fafafa; font-family:'Pretendard',sans-serif; }
header, .stDeployButton, #MainMenu, footer, [data-testid="stToolbar"] { display:none!important; }
.block-container { max-width:960px!important; padding:0 24px 80px!important; }

/* Nav */
.nav { display:flex; align-items:center; justify-content:space-between; padding:20px 0; border-bottom:1px solid #eee; margin-bottom:48px; }
.nav-logo { font-size:1.1rem; font-weight:800; color:#111; letter-spacing:-0.5px; }
.nav-logo span { color:#6366f1; }
.nav-sub { color:#999; font-size:0.78rem; }

/* Hero (brunch) */
.br-hero { padding:48px 0 56px; border-bottom:1px solid #eee; margin-bottom:48px; }
.br-hero h1 { font-size:2.8rem; font-weight:900; color:#111; line-height:1.2; letter-spacing:-1.5px; margin-bottom:16px; }
.br-hero p { color:#666; font-size:1.05rem; line-height:1.7; max-width:520px; }

/* Section label */
.sec-label { font-size:0.72rem; color:#6366f1; letter-spacing:2px; text-transform:uppercase; font-weight:700; margin-bottom:10px; }
.sec-title { font-size:2rem; font-weight:800; color:#111; margin-bottom:8px; line-height:1.3; }

/* Magazine card */
.mag-card {
  display:grid; grid-template-columns:1fr 1fr; gap:40px; align-items:center;
  padding:40px 0; border-bottom:1px solid #eee; transition:background 0.2s;
}
.mag-card:hover { background:rgba(99,102,241,0.02); }
.mag-left .mag-cat { font-size:0.7rem; color:#6366f1; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:8px; }
.mag-left h2 { font-size:1.5rem; font-weight:800; color:#111; line-height:1.3; margin-bottom:10px; }
.mag-left .mag-desc { color:#666; font-size:0.92rem; line-height:1.6; margin-bottom:16px; }
.mag-left .mag-read { color:#6366f1; font-size:0.85rem; font-weight:600; }
.mag-right { display:flex; flex-direction:column; gap:8px; }
.mag-right .tag-row { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:8px; }
.tag { padding:5px 14px; border-radius:100px; font-size:0.75rem; font-weight:500; }
.tag-ind { background:#f0eeff; color:#6366f1; }
.sig-item { display:flex; align-items:center; gap:8px; padding:4px 0; }
.sig-dot { width:5px; height:5px; background:#6366f1; border-radius:50%; flex-shrink:0; }
.sig-text { color:#888; font-size:0.82rem; }

/* Featured (first card bigger) */
.featured { padding:0 0 48px; border-bottom:1px solid #eee; margin-bottom:8px; }
.featured .feat-cat { font-size:0.72rem; color:#6366f1; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:12px; }
.featured h2 { font-size:2.2rem; font-weight:900; color:#111; line-height:1.2; margin-bottom:14px; letter-spacing:-0.5px; }
.featured .feat-desc { color:#555; font-size:1.05rem; line-height:1.7; margin-bottom:20px; max-width:600px; }
.featured .feat-meta { display:flex; align-items:center; gap:24px; }
.featured .tag-row { display:flex; flex-wrap:wrap; gap:6px; }
.featured .feat-read { color:#6366f1; font-size:0.9rem; font-weight:600; }

.footer { text-align:center; color:#bbb; font-size:0.78rem; padding:48px 0 20px; }

@media(max-width:768px) {
  .mag-card { grid-template-columns:1fr; gap:16px; }
  .br-hero h1 { font-size:2rem; }
  .featured h2 { font-size:1.6rem; }
}
</style>
""", unsafe_allow_html=True)

# ===== ROUTING =====
if st.session_state.view == "detail":
    # ===== DETAIL PAGE =====
    if st.button("← 돌아가기", key="back"):
        st.session_state.view = "feed"
        st.rerun()

    st.markdown("""
    <div class="detail-hero" style="text-align:center;padding:32px 0 48px">
      <div style="font-size:4rem;margin-bottom:16px">⛳</div>
      <div class="sec-title" style="font-size:2.2rem">접대 골프를<br>시작한 30대</div>
      <p style="color:#94a3b8;font-size:1.05rem;line-height:1.6;margin-top:16px;max-width:500px;margin-left:auto;margin-right:auto">회사 때문에 골프에 입문한 대기업 직장인.<br>취미가 아니라 업무의 연장.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        # 광고주의 숙제
        st.markdown("""
        <div class="sec-label">광고주의 숙제</div>
        <div style="background:rgba(255,255,255,0.04);border-left:3px solid #6366f1;padding:20px;border-radius:0 12px 12px 0;margin-bottom:24px">
          <p style="color:#cbd5e1;font-size:0.95rem;line-height:1.6;font-style:italic">"골프 관련 광고를 하고 싶은데,<br>기존 골퍼랑 입문자를 어떻게 구분하죠?"</p>
        </div>
        <p style="color:#cbd5e1;font-size:0.95rem;line-height:1.7">골프 시장이 커졌다는 건 다 안다. 문제는 <strong style="color:#fff">"골프 관심자"로 타겟팅하면</strong> 10년 경력 싱글 골퍼부터 유튜브만 보는 구경꾼까지 다 섞인다는 것.</p>
        """, unsafe_allow_html=True)

        # 행동 시그널
        st.markdown("""
        <div style="margin-top:36px">
        <div class="sec-label">진짜 타겟은 따로 있다</div>
        <div class="sec-title" style="font-size:1.15rem">이런 행동을 하는 사람이다</div>
        </div>
        """, unsafe_allow_html=True)

        signals = ["30대 초중반, 대기업 재직 추정", "최근 3개월 내 골프 앱 첫 설치", "골프 용품 비교 검색 시작", "골프 레슨 예약 앱 탐색", "평일 저녁 골프 콘텐츠 소비"]
        for s in signals:
            st.markdown(f'<div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04)"><span style="width:6px;height:6px;background:#6366f1;border-radius:50%;flex-shrink:0"></span><span style="color:#cbd5e1;font-size:0.9rem">{s}</span></div>', unsafe_allow_html=True)

        st.markdown("""
        <p style="color:#cbd5e1;font-size:0.95rem;line-height:1.7;margin-top:20px">
          이 조합이 의미하는 건 하나다.<br><strong style="color:#fff">"회사 때문에 골프를 시작한 사람."</strong>
          <br><br>접대, 임원 라운딩, 거래처 미팅.<br>이 사람들은 기존 골퍼와 <strong style="color:#fff">완전히 다른 니즈</strong>를 가지고 있다.
        </p>
        """, unsafe_allow_html=True)

    with col2:
        # 비교
        st.markdown("""
        <div class="sec-label">뭐가 다른가</div>
        <div class="sec-title" style="font-size:1.15rem">같은 골프인데, 완전히 다른 사람</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0;border-radius:16px;overflow:hidden;margin:16px 0">
          <div style="padding:20px;background:rgba(255,255,255,0.03)">
            <h4 style="font-size:0.75rem;color:#64748b;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;font-weight:600">기존 골프 관심자</h4>
            <ul style="list-style:none;padding:0">
              <li style="font-size:0.85rem;color:#94a3b8;padding:5px 0">장비에 진심</li>
              <li style="font-size:0.85rem;color:#94a3b8;padding:5px 0">스코어에 집착</li>
              <li style="font-size:0.85rem;color:#94a3b8;padding:5px 0">가성비 추구</li>
              <li style="font-size:0.85rem;color:#94a3b8;padding:5px 0">주말 라운딩</li>
              <li style="font-size:0.85rem;color:#94a3b8;padding:5px 0">천천히 구매</li>
            </ul>
          </div>
          <div style="padding:20px;background:rgba(99,102,241,0.08)">
            <h4 style="font-size:0.75rem;color:#a5b4fc;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;font-weight:600">접대 골프 입문자</h4>
            <ul style="list-style:none;padding:0">
              <li style="font-size:0.85rem;color:#e2e8f0;padding:5px 0">창피 안 당할 정도면 됨</li>
              <li style="font-size:0.85rem;color:#e2e8f0;padding:5px 0">매너와 에티켓이 급함</li>
              <li style="font-size:0.85rem;color:#e2e8f0;padding:5px 0">무난하게 좋은 걸 원함</li>
              <li style="font-size:0.85rem;color:#e2e8f0;padding:5px 0">평일 라운딩 비중 높음</li>
              <li style="font-size:0.85rem;color:#e2e8f0;padding:5px 0">빠르게 풀세트 구매</li>
            </ul>
          </div>
        </div>
        <p style="color:#cbd5e1;font-size:0.95rem;line-height:1.7"><strong style="color:#fff">이 사람은 고민하지 않는다. 빠르게 산다.</strong><br>객단가가 높고 전환이 빠르다.</p>
        """, unsafe_allow_html=True)

        # 추천 업종
        st.markdown("""
        <div style="margin-top:36px">
        <div class="sec-label">이 오디언스를 쓸 수 있는 광고주</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px">
          <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:16px">
            <h4 style="color:#fff;font-size:0.9rem;font-weight:600;margin-bottom:4px">⛳ 골프 용품</h4>
            <p style="color:#94a3b8;font-size:0.8rem;line-height:1.4">입문자 풀세트, "처음 사는 드라이버" 소구</p>
          </div>
          <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:16px">
            <h4 style="color:#fff;font-size:0.9rem;font-weight:600;margin-bottom:4px">👔 골프웨어</h4>
            <p style="color:#94a3b8;font-size:0.8rem;line-height:1.4">"접대 라운딩에 입고 갈 옷" 포지셔닝</p>
          </div>
          <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:16px">
            <h4 style="color:#fff;font-size:0.9rem;font-weight:600;margin-bottom:4px">🏌️ 골프 레슨</h4>
            <p style="color:#94a3b8;font-size:0.8rem;line-height:1.4">"4주 만에 필드 나가기" 속성 레슨</p>
          </div>
          <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:16px">
            <h4 style="color:#fff;font-size:0.9rem;font-weight:600;margin-bottom:4px">💳 프리미엄 카드</h4>
            <p style="color:#94a3b8;font-size:0.8rem;line-height:1.4">골프 특화 혜택 소구</p>
          </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    # 인사이트 (full width)
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(99,102,241,0.15),rgba(168,85,247,0.1));border-radius:16px;padding:32px;margin:40px 0;text-align:center">
      <p style="color:#e2e8f0;font-size:1.15rem;line-height:1.6;font-weight:500">💡 "골프 관심자"는 오디언스가 아니다.<br><strong>왜 골프를 시작했는지</strong>가 오디언스를 만든다.</p>
      <p style="color:#94a3b8;font-size:0.92rem;margin-top:12px">같은 골프인데, 접대 입문자 / 취미 입문자 / 은퇴 후 입문자는 완전히 다른 사람이다.<br>행동 시그널의 조합으로 이걸 구분할 수 있다.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="footer">© 2026 IGAWorks — 오늘의 오디언스 · Audience Idea Bank</div>', unsafe_allow_html=True)

else:
    # ===== BRUNCH FEED =====
    st.markdown("""
    <div class="nav">
      <div>
        <div class="nav-logo"><span>오늘의</span> 오디언스</div>
        <div class="nav-sub">by IGAWorks</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== FEATURED ESSAY =====
    st.markdown("""
    <div style="padding:48px 0 40px;border-bottom:1px solid #eee;margin-bottom:48px">
      <h1 style="font-size:2.4rem;font-weight:900;color:#111;line-height:1.2;letter-spacing:-1.5px;margin-bottom:16px">오늘의 오디언스</h1>
      <p style="color:#111;font-size:1.05rem;font-weight:600;line-height:1.7;margin-bottom:12px">
        "다음 캠페인, 누구한테 해야 하지?"를 해결하는 서비스
      </p>
      <p style="color:#888;font-size:0.92rem;line-height:1.8">
        광고주가 미처 생각하지 못한 타겟을 매일 발견하는 곳.<br>
        트렌드를 자동으로 읽고, 행동 시그널을 조합해<br>
        아직 아무도 안 쓰는 오디언스를 제안합니다.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:48px 0 20px">
      <div class="feat-cat" style="font-size:0.72rem;color:#6366f1;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:24px">⛳ 오늘의 오디언스 #1</div>

      <h1 style="font-size:2.6rem;font-weight:900;color:#111;line-height:1.25;letter-spacing:-1.5px;margin-bottom:32px">
        '골프 관심자' 타겟팅 금지!<br>
        접대 골프 입문자의<br>
        숨겨진 구매 시그널
      </h1>

      <p style="color:#555;font-size:1.15rem;line-height:2;margin-bottom:28px">
        "드라이버를 사는 게 아니라,<br>
        &nbsp;&nbsp;창피를 안 당할 보험을 사는 겁니다."
      </p>

      <p style="color:#888;font-size:0.92rem;line-height:1.8;margin-bottom:20px">
        광고 기획자의 말이 아닙니다.<br>
        IGAWorks DMP에서 발견한<br>
        실제 행동 데이터의 해석이죠.
      </p>

      <p style="color:#888;font-size:0.92rem;line-height:1.8;margin-bottom:20px">
        골프 시장이 커졌다는 건 다 압니다.<br>
        문제는 "골프 관심자"로 타겟팅하면<br>
        10년 경력 싱글 골퍼부터<br>
        유튜브만 보는 구경꾼까지<br>
        전부 섞인다는 것.
      </p>

      <p style="color:#888;font-size:0.92rem;line-height:1.8;margin-bottom:28px">
        우리가 주목한 건<br>
        <strong style="color:#111">완전히 다른 종류의 골퍼</strong>였습니다.
      </p>

      <div style="background:#f5f3ff;border-radius:12px;padding:28px 32px;margin:32px 0">
        <p style="color:#6366f1;font-size:0.75rem;font-weight:700;letter-spacing:1.5px;margin-bottom:16px">BEHAVIOR SIGNALS</p>
        <p style="color:#333;font-size:0.95rem;line-height:1.9">
          → 30대 초중반, 대기업 재직 추정<br>
          → 최근 3개월 내 골프 앱 <strong>첫</strong> 설치<br>
          → 골프 용품 비교 검색 시작<br>
          → 골프 레슨 예약 앱 탐색<br>
          → <strong>평일 저녁</strong> 골프 콘텐츠 소비
        </p>
      </div>

      <p style="color:#888;font-size:0.92rem;line-height:1.8;margin-bottom:20px">
        이 조합이 의미하는 건 하나입니다.
      </p>

      <p style="color:#111;font-size:1.3rem;font-weight:800;line-height:1.5;margin-bottom:28px">
        "회사 때문에 골프를 시작한 사람."
      </p>

      <p style="color:#888;font-size:0.92rem;line-height:1.8;margin-bottom:20px">
        접대, 임원 라운딩, 거래처 미팅.<br>
        이 사람들은 기존 골퍼와<br>
        완전히 다른 니즈를 가지고 있습니다.
      </p>

      <p style="color:#888;font-size:0.92rem;line-height:1.8;margin-bottom:8px">
        장비에 진심인 골퍼와 달리<br>
        <strong style="color:#111">창피 안 당할 정도면 됩니다.</strong><br>
        스코어에 집착하는 골퍼와 달리<br>
        <strong style="color:#111">매너와 에티켓이 급합니다.</strong><br>
        가성비를 따지는 골퍼와 달리<br>
        <strong style="color:#111">무난하게 좋은 걸 원합니다.</strong>
      </p>

      <p style="color:#888;font-size:0.92rem;line-height:1.8;margin:28px 0">
        그래서 이 사람은<br>
        고민하지 않습니다.<br>
        <strong style="color:#111;font-size:1.05rem">빠르게 삽니다.</strong><br>
        객단가가 높고, 전환이 빠릅니다.
      </p>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:32px 0">
        <div style="background:#f8f8f8;border-radius:10px;padding:20px">
          <p style="font-size:0.82rem;font-weight:700;color:#111;margin-bottom:6px">⛳ 골프 용품</p>
          <p style="font-size:0.8rem;color:#888;line-height:1.4">입문자 풀세트, "처음 사는 드라이버" 소구</p>
        </div>
        <div style="background:#f8f8f8;border-radius:10px;padding:20px">
          <p style="font-size:0.82rem;font-weight:700;color:#111;margin-bottom:6px">👔 골프웨어</p>
          <p style="font-size:0.8rem;color:#888;line-height:1.4">"접대 라운딩에 입고 갈 옷" 포지셔닝</p>
        </div>
        <div style="background:#f8f8f8;border-radius:10px;padding:20px">
          <p style="font-size:0.82rem;font-weight:700;color:#111;margin-bottom:6px">🏌️ 골프 레슨</p>
          <p style="font-size:0.8rem;color:#888;line-height:1.4">"4주 만에 필드 나가기" 속성 레슨</p>
        </div>
        <div style="background:#f8f8f8;border-radius:10px;padding:20px">
          <p style="font-size:0.82rem;font-weight:700;color:#111;margin-bottom:6px">💳 프리미엄 카드</p>
          <p style="font-size:0.8rem;color:#888;line-height:1.4">골프 특화 혜택 소구</p>
        </div>
      </div>

      <div style="background:#111;border-radius:12px;padding:28px 32px;margin:32px 0">
        <p style="color:#a5b4fc;font-size:0.75rem;font-weight:700;letter-spacing:1.5px;margin-bottom:12px">💡 KEY INSIGHT</p>
        <p style="color:#fff;font-size:1.05rem;line-height:1.7;font-weight:500">
          "골프 관심자"는 오디언스가 아닙니다.<br>
          <strong>왜 골프를 시작했는지</strong>가 오디언스를 만듭니다.
        </p>
      </div>

      <p style="color:#888;font-size:0.92rem;line-height:1.8">
        같은 골프인데,<br>
        접대 입문자 / 취미 입문자 / 은퇴 후 입문자는<br>
        완전히 다른 사람입니다.<br><br>
        행동 시그널의 조합으로<br>
        이걸 구분할 수 있습니다.
      </p>

      <p style="color:#bbb;font-size:0.8rem;margin-top:40px;padding-top:20px;border-top:1px solid #eee">
        오늘의 오디언스 #1 · 접대 골프를 시작한 30대 · by IGAWorks
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ===== COMING SOON =====
    st.markdown("""
    <div style="padding:48px 0 20px;border-top:1px solid #eee;margin-top:48px">
      <p style="font-size:0.72rem;color:#6366f1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:24px">COMING SOON</p>
      <h2 style="font-size:1.6rem;font-weight:800;color:#111;margin-bottom:8px">다음 오디언스를 준비하고 있어요</h2>
      <p style="color:#999;font-size:0.92rem;margin-bottom:36px">매주 새로운 오디언스 아이디어가 공개됩니다.</p>
    </div>
    """, unsafe_allow_html=True)

    UPCOMING = [
        ("#2", "💰", "첫 주식을 산 2030 사회초년생", "금융", '"월급만으로는 안 된다"를 깨달은 사람'),
        ("#3", "🏦", "대출 갈아타기 골든타임 유저", "금융", "지금 움직이면 수백만 원 아끼는 사람"),
        ("#4", "⛳", "스크린에서 필드로 넘어가는 여성 골퍼", "골프", "취미에서 라이프스타일로 전환 중"),
        ("#5", "📚", "AI 시대 불안한 학부모", "교육", "아이 미래가 걱정되기 시작한 부모"),
        ("#6", "🎓", "이직 준비하는 3~5년차 직장인", "교육", "리스킬링을 시작한 유저"),
        ("#7", "👗", "콰이어트 럭셔리에 눈뜬 30대", "패션", '"비싸 보이지 않게 비싼 옷"을 찾는 유저'),
        ("#8", "👟", "러닝에 빠진 패션 피플", "패션", "라이프스타일로 러닝을 시작한 유저"),
    ]

    for num, emoji, title, cat, desc in UPCOMING:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:20px;padding:20px 0;border-bottom:1px solid #f0f0f0;opacity:0.55">
          <div style="font-size:1.8rem">{emoji}</div>
          <div style="flex:1">
            <p style="font-size:0.7rem;color:#6366f1;font-weight:600;letter-spacing:1px;margin-bottom:2px">{cat} · 오늘의 오디언스 {num}</p>
            <p style="font-size:1.05rem;font-weight:700;color:#111;margin-bottom:2px">{title}</p>
            <p style="font-size:0.82rem;color:#999">{desc}</p>
          </div>
          <div style="color:#ccc;font-size:0.78rem;font-weight:500;white-space:nowrap">오픈 예정</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="footer">오늘의 오디언스 · by IGAWorks · © 2026</div>', unsafe_allow_html=True)
