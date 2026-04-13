import streamlit as st
import json
import os

st.set_page_config(page_title="오늘의 오디언스 — IGAWorks", page_icon="🎯", layout="wide")

if "view" not in st.session_state:
    st.session_state.view = "feed"

# ===== 에세이 로딩 =====
ESSAYS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "essays")

def load_meta():
    p = os.path.join(ESSAYS_DIR, "meta.json")
    if not os.path.exists(p):
        return []
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def load_essay_html(essay_id):
    p = os.path.join(ESSAYS_DIR, f"{essay_id}.html")
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

essays = sorted(load_meta(), key=lambda e: e["number"], reverse=True)

# ===== CSS (기존 그대로) =====
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
.stApp { background:#fff; font-family:'Pretendard',sans-serif; }
header, .stDeployButton, #MainMenu, footer, [data-testid="stToolbar"] { display:none!important; }
.block-container { max-width:960px!important; padding:0 32px 80px!important; }

.nav { display:flex; align-items:center; justify-content:space-between; padding:16px 0; border-bottom:1px solid #f0f0f0; margin-bottom:40px; }
.nav-logo { font-size:1rem; font-weight:800; color:#111; letter-spacing:-0.5px; }
.nav-logo span { color:#6366f1; }
.nav-sub { color:#bbb; font-size:0.72rem; }

.author { display:flex; align-items:center; gap:12px; margin-bottom:32px; }
.author-avatar { width:40px; height:40px; border-radius:50%; background:#6366f1; display:flex; align-items:center; justify-content:center; color:#fff; font-size:0.85rem; font-weight:700; }
.author-name { font-size:0.85rem; font-weight:600; color:#111; }
.author-date { font-size:0.75rem; color:#bbb; }

.note-body p { color:#333; font-size:0.95rem; line-height:2; margin-bottom:24px; }
.note-body strong { color:#111; }
.note-body .lead { color:#111; font-size:1.2rem; font-weight:700; line-height:1.6; margin-bottom:28px; }
.note-body .quote { color:#555; font-size:1.1rem; line-height:1.8; font-style:italic; margin:32px 0; padding-left:20px; border-left:3px solid #6366f1; }

.sig-box { background:#f8f7ff; border-radius:12px; padding:24px 28px; margin:32px 0; }
.sig-box .sig-label { font-size:0.7rem; color:#6366f1; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:14px; }
.sig-box p { color:#333; font-size:0.9rem; line-height:2; margin:0; }

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

.ind-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:32px 0; }
.ind-card { background:#f8f8f8; border-radius:10px; padding:18px; }
.ind-card .ind-title { font-size:0.82rem; font-weight:700; color:#111; margin-bottom:4px; }
.ind-card .ind-desc { font-size:0.78rem; color:#888; line-height:1.4; }

.insight { background:#111; border-radius:12px; padding:28px; margin:36px 0; }
.insight .ins-label { font-size:0.7rem; color:#a5b4fc; font-weight:700; letter-spacing:1.5px; margin-bottom:10px; }
.insight p { color:#fff; font-size:0.98rem; line-height:1.8; font-weight:500; }

.footer { text-align:center; color:#ccc; font-size:0.75rem; padding:48px 0 20px; }

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
div[data-testid="stButton"] > button[kind="secondary"] {
  width:auto!important; padding:8px 16px!important; border-radius:8px!important;
  font-size:0.85rem!important; font-weight:500!important;
}
.note-end { color:#bbb; font-size:0.78rem; margin-top:48px; padding-top:20px; border-top:1px solid #f0f0f0; }

@media(max-width:768px) {
  .block-container { max-width:100%!important; }
}
</style>
""", unsafe_allow_html=True)

# ===== DETAIL VIEW =====
if st.session_state.view.startswith("detail_"):
    essay_id = st.session_state.view[len("detail_"):]
    meta = next((e for e in essays if e["id"] == essay_id), None)
    html = load_essay_html(essay_id) if meta else None

    if meta and html:
        if st.button("← 돌아가기", key="back"):
            st.session_state.view = "feed"
            st.rerun()

        date_fmt = meta["date"].replace("-", ".")
        detail_html = f"""
        <style>.block-container {{ max-width:620px!important; padding:0 20px 80px!important; }}</style>
        <div class="nav"><div>
          <div class="nav-logo"><span>오늘의</span> 오디언스</div>
          <div class="nav-sub">by IGAWorks</div>
        </div></div>
        <div class="author">
          <div class="author-avatar">IG</div>
          <div>
            <div class="author-name">IGAWorks 오디언스 랩</div>
            <div class="author-date">{date_fmt} · 오늘의 오디언스 #{meta['number']}</div>
          </div>
        </div>
        {html}
        """
        st.markdown(detail_html, unsafe_allow_html=True)
    else:
        st.session_state.view = "feed"
        st.rerun()

# ===== FEED VIEW =====
else:
    # Hero
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
    """, unsafe_allow_html=True)

    if essays:
        # TODAY — 최신 에세이
        today_essay = essays[0]
        st.markdown(f"""
        <p style="font-size:0.7rem;color:#6366f1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:20px">🎯 오늘의 오디언스</p>
        <div style="border-radius:20px;overflow:hidden;border:1px solid #e8e8e8;margin-bottom:40px;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 8px 30px rgba(0,0,0,0.08)'" onmouseout="this.style.boxShadow='none'">
          <div style="background:linear-gradient(135deg,{today_essay['color_from']} 0%,{today_essay['color_to']} 100%);padding:48px 36px;position:relative;overflow:hidden">
            <div style="position:absolute;top:20px;right:24px;font-size:4rem;opacity:0.15">{today_essay['emoji']}</div>
            <span style="background:rgba(255,255,255,0.2);color:#fff;font-size:0.68rem;font-weight:600;padding:4px 12px;border-radius:100px;letter-spacing:1px">TODAY</span>
            <h2 style="color:#fff;font-size:1.5rem;font-weight:900;line-height:1.3;margin-top:16px">{today_essay['title']}</h2>
            <p style="color:rgba(255,255,255,0.7);font-size:0.92rem;line-height:1.6;margin-top:8px">{today_essay['subtitle']}</p>
          </div>
          <div style="padding:20px 24px;display:flex;align-items:center;justify-content:space-between">
            <span style="font-size:0.78rem;color:#888">{today_essay['summary_label']}</span>
            <span style="color:#6366f1;font-size:0.82rem;font-weight:600">읽기 →</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"{today_essay['emoji']} {today_essay['subtitle']}", key="go_today"):
            st.session_state.view = f"detail_{today_essay['id']}"
            st.rerun()

        # 지난 노트
        past = essays[1:]
        if past:
            cols_count = min(len(past), 3)
            grid_items = ""
            for e in past:
                short_title = e.get("card_title", e["title"].replace("'", "").replace(" 타겟팅 금지!", ""))
                grid_items += f"""
                <div style="border-radius:16px;overflow:hidden;border:1px solid #f0f0f0;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
                  <div style="background:linear-gradient(135deg,{e['color_from']},{e['color_to']});padding:28px 20px;position:relative">
                    <div style="position:absolute;top:10px;right:14px;font-size:2.4rem;opacity:0.15">{e['emoji']}</div>
                    <span style="background:rgba(255,255,255,0.2);color:#fff;font-size:0.6rem;font-weight:600;padding:2px 8px;border-radius:100px">#{e['number']}</span>
                    <h3 style="color:#fff;font-size:0.92rem;font-weight:800;line-height:1.3;margin-top:10px">{short_title}</h3>
                  </div>
                  <div style="padding:12px 14px"><span style="font-size:0.68rem;color:#999">{e['industries']}</span></div>
                </div>"""

            st.markdown(f"""
            <p style="font-size:0.7rem;color:#6366f1;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin:8px 0 20px">📚 지난 노트</p>
            <div style="display:grid;grid-template-columns:repeat({cols_count},1fr);gap:14px;margin-bottom:40px">
              {grid_items}
            </div>
            """, unsafe_allow_html=True)

            btn_cols = st.columns(cols_count)
            for i, e in enumerate(past):
                with btn_cols[i % cols_count]:
                    if st.button(f"{e['emoji']} #{e['number']}", key=f"go_{e['id']}"):
                        st.session_state.view = f"detail_{e['id']}"
                        st.rerun()

    st.markdown('<div class="footer">오늘의 오디언스 · by IGAWorks · © 2026</div>', unsafe_allow_html=True)
