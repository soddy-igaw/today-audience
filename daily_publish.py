"""
오늘의 오디언스 — 자동 발행 파이프라인
매일 10시 실행: 트렌드 수집 → 주제 선정 → 에세이 생성 → 코드 반영 → git push

설정:
  export ANTHROPIC_API_KEY="sk-..."  또는
  export OPENAI_API_KEY="sk-..."     또는
  AWS Bedrock 사용 (기본)

사용법:
  python3 daily_publish.py              # 전체 파이프라인
  python3 daily_publish.py --dry-run    # 에세이만 생성 (코드 반영 안 함)
"""

import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime

# === 설정 ===
ESSAY_DIR = os.path.dirname(os.path.abspath(__file__))
APP_FILE = os.path.join(ESSAY_DIR, "app.py")
PERSONA_FILE = "/home/soddy/projects/persona-model/config/market_size_reference.json"

CATEGORY_ROTATION = {
    0: "금융",    # 월
    1: "부동산",  # 화
    2: "쇼핑",    # 수
    3: "헬스",    # 목
    4: "골프",    # 금
    5: "교육",    # 토
    6: "반려동물", # 일
}

CATEGORY_KEYWORDS = {
    "금융": ["대출 갈아타기", "금리 비교", "ETF 투자", "증권 계좌"],
    "부동산": ["전세 만기", "아파트 매매", "부동산 규제", "이사"],
    "쇼핑": ["알리익스프레스 테무", "쿠팡", "중고거래", "새벽배송"],
    "배달": ["배달앱 배달비", "쿠팡이츠", "배달의민족"],
    "골프": ["골프 입문", "스크린골프", "골프웨어", "여성 골퍼"],
    "교육": ["코딩 교육 AI", "이직 준비", "자격증", "온라인 강의"],
    "반려동물": ["반려동물 펫코노미", "펫보험", "동물병원", "반려동물 입양"],
    "패션": ["러닝크루", "콰이어트럭셔리", "중고명품"],
    "헬스": ["헬스장 PT", "러닝크루", "홈트레이닝", "크로스핏", "필라테스"],
}

CATEGORY_APPS = {
    "금융": ["뱅크샐러드", "핀다", "토스"],
    "부동산": ["직방", "다방", "호갱노노"],
    "쇼핑": ["쿠팡", "알리익스프레스", "테무"],
    "배달": ["배달의민족", "쿠팡이츠", "요기요"],
    "골프": ["카카오VX", "골프존", "스마트스코어"],
    "교육": ["클래스101", "패스트캠퍼스", "인프런"],
    "반려동물": ["포인핸드", "펫닥", "핏펫"],
    "패션": ["크림", "번개장터", "무신사"],
    "헬스": ["캐치핏", "나이키런클럽", "킵", "애플피트니스", "눔"],
}

CATEGORY_COLORS = {
    "금융": ("#1e3a5f", "#2a5298", "💰"),
    "부동산": ("#4a1942", "#6b3fa0", "🏠"),
    "쇼핑": ("#7c2d12", "#ea580c", "🛒"),
    "배달": ("#14532d", "#16a34a", "🛵"),
    "골프": ("#1a472a", "#3a7d5c", "⛳"),
    "교육": ("#1e1b4b", "#4338ca", "📚"),
    "반려동물": ("#9a3412", "#f97316", "🐾"),
    "패션": ("#831843", "#db2777", "👗"),
    "헬스": ("#0f766e", "#14b8a6", "💪"),
}


def collect_trends(category):
    """카테고리별 최신 뉴스 수집 (3일 이내)"""
    keywords = CATEGORY_KEYWORDS.get(category, [])
    results = []
    for kw in keywords:
        encoded = urllib.parse.quote(kw)
        url = f"https://news.google.com/rss/search?q={encoded}+when:3d&hl=ko&gl=KR&ceid=KR:ko"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = resp.read().decode("utf-8", errors="ignore")
                for item in data.split("<title>")[2:4]:
                    t = item.split("</title>")[0].strip()
                    if t and t != "Google 뉴스":
                        results.append({"keyword": kw, "title": t})
        except:
            pass
    return results


def get_persona_data(category):
    """자사 페르소나 데이터 로드"""
    persona_map = {
        "골프": "P030902",
        "반려동물": "P020501",
        "패션": "P030203",
        "쇼핑": "P030101",
        "교육": "P010104",
        "헬스": "P031003",
        "부동산": "P031101",
    }
    code = persona_map.get(category)
    if not code or not os.path.exists(PERSONA_FILE):
        return None
    with open(PERSONA_FILE, "r") as f:
        data = json.load(f)
    return data.get(code)


def build_prompt(category, trends, persona):
    """에세이 생성 프롬프트 구성"""
    today_str = datetime.now().strftime("%Y.%m.%d")
    apps = ", ".join(CATEGORY_APPS.get(category, []))
    trend_text = "\n".join([f"- [{t['keyword']}] {t['title']}" for t in trends[:5]])
    persona_text = ""
    if persona:
        persona_text = f"""
자사 DMP 데이터:
- 페르소나: {persona['name']}
- 추정 모수: {persona.get('estimate_min', '?'):,}~{persona.get('estimate_max', '?'):,}명
- 근거: {persona.get('basis', '')}
- 출처: {persona.get('source', '')}
"""

    return f"""당신은 IGAWorks의 "오늘의 오디언스" 에세이 작가입니다.
롱블랙 스타일로 한 편의 에세이를 작성하세요. 최소 3000자 이상, 깊이 있게 작성하세요.

## 규칙
1. 제목은 "'OO 관심자' 타겟팅 금지! [구체적 오디언스]" 형식
2. 가상의 광고주 마케터 인터뷰 포함 (이름은 알파벳 1글자+씨). 대화를 여러 번 주고받으세요.
3. DMP 앱 데이터로 실제 잡을 수 있는 시그널만 사용
   - 가능: 앱 설치, 사용 빈도, 동시 설치, 타이밍
   - 불가: 앱 내부 행동, 검색어, 구매 금액
4. 비교표 포함 (구경꾼 vs 진짜 타겟) — 각 5줄 이상
5. 광고 카피 비교 (❌ 기존 vs ✅ 새 오디언스)
6. 추적 가능한 앱: {apps}
7. 짧은 문장, 많은 줄바꿈, 롱블랙 톤
8. 추천 업종 4개 이상 (ind-grid)
9. AUDIENCE CARD (다크 배경 style="background:#111") 포함 — 추정 모수(반드시 "N~N만" 형식), 추천 업종, 시그널, 메시지

## 필수 구조 (이 순서대로 작성):
1. <p class="lead"> 제목/부제
2. <div class="quote"> 마케터 첫 인용
3. 문제 제기 (기존 타겟팅의 한계) — 3~4 문단
4. <div class="sig-box"> BEHAVIOR SIGNALS (5개 이상)
5. 핵심 해석 — 2~3 문단
6. <div class="cmp-grid"> 비교표
7. <div class="sig-box"> DMP에서 잡는 법
8. <div class="ind-grid"> 추천 업종 4개
9. <div class="insight"> KEY INSIGHT
10. 광고 카피 비교 (❌ vs ✅)
11. AUDIENCE CARD (다크 배경 div)
12. <div class="note-end"> 마무리

## 오늘의 카테고리: {category}
## 날짜: {today_str}

## 최신 트렌드:
{trend_text}

{persona_text}

## 출력 형식
HTML 조각(fragment)만 출력. <!DOCTYPE>, <html>, <head>, <body>, <article> 태그 절대 금지.
<div class="note-body">로 시작하세요.
class: note-body, lead, quote, sig-box, sig-label, cmp-grid, cmp-card, cmp-left, cmp-right, ind-grid, ind-card, ind-title, ind-desc, insight, ins-label, note-end
"""


def call_llm(prompt):
    """LLM API 호출 (Bedrock > Anthropic > OpenAI)"""
    # 1. AWS Bedrock (기본)
    result = _call_bedrock(prompt)
    if result:
        return result

    # 2. Anthropic 직접
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        return _call_anthropic(prompt, api_key)

    # 3. OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return _call_openai(prompt, api_key)

    print("⚠️  LLM API 사용 불가. AWS 크레덴셜 또는 API 키를 설정하세요.")
    return None


def _call_bedrock(prompt):
    """AWS Bedrock Claude"""
    try:
        import boto3
        region = os.environ.get("AWS_REGION", "us-east-1")
        # GitHub Actions에서는 환경변수, 로컬에서는 SSO → default fallback
        if os.environ.get("AWS_ACCESS_KEY_ID"):
            session = boto3.Session()
        else:
            try:
                session = boto3.Session(profile_name="audmaker_soddy")
                session.client("sts").get_caller_identity()
            except Exception:
                session = boto3.Session()  # default 프로필 (IAM 키)
        client = session.client("bedrock-runtime", region_name=region)
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        })
        resp = client.invoke_model(
            modelId="us.anthropic.claude-sonnet-4-20250514-v1:0",
            body=body,
            contentType="application/json",
        )
        result = json.loads(resp["body"].read())
        return result["content"][0]["text"]
    except ImportError:
        print("   boto3 미설치, Bedrock 스킵")
        return None
    except Exception as e:
        print(f"   Bedrock 실패: {e}")
        return None


def _call_anthropic(prompt, api_key):
    """Anthropic Claude API"""
    data = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result["content"][0]["text"]


def _call_openai(prompt, api_key):
    """OpenAI API"""
    data = json.dumps({
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result["choices"][0]["message"]["content"]


def inject_to_app(category, today, essay_html):
    """app.py에 새 에세이를 직접 삽입"""
    import re as _re

    colors = CATEGORY_COLORS.get(category, ("#333", "#666", "📝"))
    color_from, color_to, emoji = colors
    date_fmt = today.strftime("%Y.%m.%d")

    # Extract title/subtitle from essay HTML
    m = _re.search(r'class="lead"[^>]*>(.*?)</[^>]+>', essay_html, _re.DOTALL)
    raw = _re.sub(r'<[^>]+>', '\n', m.group(1)).strip() if m else category
    lines = [l.strip() for l in raw.split('\n') if l.strip()]
    title = lines[0] if lines else category
    subtitle = lines[1] if len(lines) > 1 else title

    # Extract audience size from AUDIENCE CARD or 추정 모수
    audience_m = _re.search(r'추정 모수.*?<p[^>]*>([\d~,만억천명\s]+)</p>', essay_html, _re.DOTALL)
    if not audience_m:
        audience_m = _re.search(r'([\d,]+~[\d,]+만)', essay_html)
    audience_size = audience_m.group(1).strip() if audience_m else ""

    with open(APP_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Count existing essays to get next number
    existing = _re.findall(r'오늘의 오디언스 #(\d+)', code)
    next_num = max(int(n) for n in existing) + 1 if existing else 1

    # 2. Find current TODAY info (from the go_ button before 지난 노트)
    today_btn = _re.search(
        r'if st\.button\("(.+?)",\s*key="go_(\w+)"\):\s*\n\s*st\.session_state\.view = "detail_(\w+)"',
        code[code.find('🎯 오늘의 오디언스'):]
    )
    old_view_key = today_btn.group(2) if today_btn else None
    old_detail = today_btn.group(3) if today_btn else None

    # 3. Extract current TODAY card colors/emoji/title for moving to 지난 노트
    today_card_m = _re.search(
        r'<span[^>]*>TODAY</span>\s*<h2[^>]*>(.*?)</h2>\s*<p[^>]*>(.*?)</p>',
        code, _re.DOTALL
    )
    old_title_short = _re.sub(r'<[^>]+>', '', today_card_m.group(1)).strip() if today_card_m else ""
    old_gradient_m = _re.search(r'background:linear-gradient\(135deg,(#\w+)[^)]*\)', code[code.find('TODAY'):])
    old_color_from = old_gradient_m.group(1) if old_gradient_m else "#333"
    old_emoji_m = _re.search(r'opacity:0\.15">(.)(?:</div>)', code[code.find('TODAY'):])
    old_emoji = old_emoji_m.group(1) if old_emoji_m else "📝"

    # Get old summary from card bottom
    old_summary_m = _re.search(r'font-size:0\.78rem;color:#888">(.*?)</span>', code[code.find('TODAY'):], _re.DOTALL)
    old_summary_industries = ""
    if old_summary_m:
        old_summary_industries = _re.sub(r'<[^>]+>', '', old_summary_m.group(1)).strip()[:30]

    new_view = f"detail_new{next_num}"

    # 4. Build new elif route block
    route_block = f'''
elif st.session_state.view == "{new_view}":
    if st.button("← 돌아가기", key="back_{next_num}"):
        st.session_state.view = "feed"
        st.rerun()

    st.markdown("""
    <style>.block-container {{ max-width:620px!important; padding:0 20px 80px!important; }}</style>
    <div class="nav"><div>
      <div class="nav-logo"><span>오늘의</span> 오디언스</div>
      <div class="nav-sub">by IGAWorks</div>
    </div></div>
    <div class="author">
      <div class="author-avatar">IG</div>
      <div>
        <div class="author-name">IGAWorks 오디언스 랩</div>
        <div class="author-date">{date_fmt} · 오늘의 오디언스 #{next_num}</div>
      </div>
    </div>
    {essay_html}
    """, unsafe_allow_html=True)

'''

    # 5. Insert route block before "else:" (main page)
    code = code.replace('\nelse:\n    # ===== MAIN PAGE =====',
                        route_block + 'else:\n    # ===== MAIN PAGE =====')

    # 6. Replace TODAY card with new essay
    today_section_start = code.find('🎯 오늘의 오디언스')
    today_section_end = code.find('""", unsafe_allow_html=True)', today_section_start) + len('""", unsafe_allow_html=True)')

    new_today_card = f'''🎯 오늘의 오디언스</p>

    <div style="border-radius:20px;overflow:hidden;border:1px solid #e8e8e8;margin-bottom:40px;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 8px 30px rgba(0,0,0,0.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="background:linear-gradient(135deg,{color_from} 0%,{color_to} 100%);padding:48px 36px;position:relative;overflow:hidden">
        <div style="position:absolute;top:20px;right:24px;font-size:4rem;opacity:0.15">{emoji}</div>
        <span style="background:rgba(255,255,255,0.2);color:#fff;font-size:0.68rem;font-weight:600;padding:4px 12px;border-radius:100px;letter-spacing:1px">TODAY</span>
        <h2 style="color:#fff;font-size:1.5rem;font-weight:900;line-height:1.3;margin-top:16px">{title}</h2>
        <p style="color:rgba(255,255,255,0.7);font-size:0.92rem;line-height:1.6;margin-top:8px">{subtitle}</p>
      </div>
      <div style="padding:20px 24px;display:flex;align-items:center;justify-content:space-between">
        <span style="font-size:0.78rem;color:#888">{f'추정 오디언스 <strong style="color:#6366f1">{audience_size}</strong>' if audience_size else f'{category} 오디언스 인사이트'}</span>
        <span style="color:#6366f1;font-size:0.82rem;font-weight:600">읽기 →</span>
      </div>
    </div>
    """, unsafe_allow_html=True)'''

    old_today = code[today_section_start:today_section_end]
    code = code.replace(old_today, new_today_card)

    # 7. Replace TODAY button
    old_btn_pattern = _re.compile(
        r'if st\.button\("[^"]+", key="go_\w+"\):\s*\n\s*st\.session_state\.view = "detail_\w+"\s*\n\s*st\.rerun\(\)\s*\n',
        _re.MULTILINE
    )
    # Find the first go_ button after TODAY card (not in 지난 노트)
    today_card_pos = code.find('🎯 오늘의 오디언스')
    past_notes_pos = code.find('지난 노트')
    btn_match = old_btn_pattern.search(code, today_card_pos, past_notes_pos)
    if btn_match:
        new_btn = f'''    if st.button("{emoji} {subtitle}", key="go_new{next_num}"):
        st.session_state.view = "{new_view}"
        st.rerun()

'''
        code = code[:btn_match.start()] + new_btn + code[btn_match.end():]

    # 8. Add old TODAY to 지난 노트 grid (prepend as first card)
    grid_marker = '<div style="display:grid;grid-template-columns:'
    grid_pos = code.find(grid_marker)
    if grid_pos > 0 and old_detail:
        # Find the first card inside the grid
        first_card_pos = code.find('<div style="border-radius:16px', grid_pos)
        # Build card for old TODAY
        old_card_title = old_title_short.replace("'", "").replace(" 타겟팅 금지!", "")
        # Wrap long titles
        words = old_card_title.split()
        if len(words) > 2:
            mid = len(words) // 2
            old_card_title = ' '.join(words[:mid]) + '<br>' + ' '.join(words[mid:])

        old_card = f'''<div style="border-radius:16px;overflow:hidden;border:1px solid #f0f0f0;cursor:pointer;transition:box-shadow 0.2s" onmouseover="this.style.boxShadow='0 4px 20px rgba(0,0,0,0.06)'" onmouseout="this.style.boxShadow='none'">
        <div style="background:linear-gradient(135deg,{old_color_from},{old_color_from}cc);padding:28px 20px;position:relative"><div style="position:absolute;top:10px;right:14px;font-size:2.4rem;opacity:0.15">{old_emoji}</div><span style="background:rgba(255,255,255,0.2);color:#fff;font-size:0.6rem;font-weight:600;padding:2px 8px;border-radius:100px">#{next_num - 1}</span><h3 style="color:#fff;font-size:0.92rem;font-weight:800;line-height:1.3;margin-top:10px">{old_card_title}</h3></div>
        <div style="padding:12px 14px"><span style="font-size:0.68rem;color:#999">{old_summary_industries}</span></div>
      </div>
      '''
        code = code[:first_card_pos] + old_card + code[first_card_pos:]

        # Update grid columns count
        grid_line_start = code.rfind('grid-template-columns:', grid_pos)
        grid_line_end = code.find(';', grid_line_start)
        old_grid = code[grid_line_start:grid_line_end]
        fr_count = old_grid.count('1fr')
        new_grid = 'grid-template-columns:' + ' '.join(['1fr'] * (fr_count + 1))
        code = code[:grid_line_start] + new_grid + code[grid_line_end:]

        # Add button for old TODAY in columns
        # Find the columns section after grid
        col_section = _re.search(r'(col\d+, col\d+, col\d+)\s*=\s*st\.columns\((\d+)\)', code)
        if col_section:
            old_col_count = int(col_section.group(2))
            # Add new column variable and button
            new_col_count = old_col_count + 1
            old_col_names = col_section.group(1)
            new_col_name = f"col{new_col_count}"
            new_col_names = f"{old_col_names}, {new_col_name}"
            code = code.replace(
                f'{old_col_names} = st.columns({old_col_count})',
                f'{new_col_names} = st.columns({new_col_count})'
            )
            # Add button in new column before footer
            footer_pos = code.find("st.markdown('<div class=\"footer\"")
            if footer_pos > 0:
                new_col_btn = f'''    with {new_col_name}:
        if st.button("{old_emoji} {old_title_short[:15]}", key="go_{old_detail}2"):
            st.session_state.view = "detail_{old_detail}"
            st.rerun()
'''
                code = code[:footer_pos] + new_col_btn + code[footer_pos:]

    with open(APP_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"📝 app.py 업데이트: #{next_num} {new_view}")


def run(dry_run=False):
    """전체 파이프라인 실행"""
    today = datetime.now()
    weekday = today.weekday()
    category = CATEGORY_ROTATION.get(weekday, "금융")

    print(f"\n🎯 오늘의 카테고리: {category} ({today.strftime('%Y-%m-%d %A')})")

    # 1. 트렌드 수집
    print("📡 트렌드 수집 중...")
    trends = collect_trends(category)
    print(f"   {len(trends)}개 뉴스 수집")
    for t in trends[:3]:
        print(f"   → [{t['keyword']}] {t['title'][:50]}...")

    # 2. 페르소나 데이터
    persona = get_persona_data(category)
    if persona:
        print(f"📊 페르소나: {persona['name']} ({persona.get('estimate_min', '?'):,}~{persona.get('estimate_max', '?'):,}명)")

    # 3. 프롬프트 생성
    prompt = build_prompt(category, trends, persona)

    # 4. LLM 호출
    print("✍️  에세이 생성 중...")
    essay_html = call_llm(prompt)

    if not essay_html:
        print("❌ 에세이 생성 실패 (API 키 확인)")
        # 프롬프트 저장 (수동 생성용)
        prompt_file = os.path.join(ESSAY_DIR, f"prompt_{today.strftime('%Y%m%d')}.txt")
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"📝 프롬프트 저장: {prompt_file}")
        print("   이 프롬프트를 Claude/ChatGPT에 붙여넣으면 에세이가 생성됩니다.")
        return

    # 4.5 HTML 정리 — 문서 태그 제거
    import re
    essay_html = re.sub(r'```html\s*', '', essay_html)
    essay_html = re.sub(r'```\s*$', '', essay_html)
    for tag in ['<!DOCTYPE[^>]*>', '</?html[^>]*>', '</?head[^>]*>', '</?body[^>]*>', '</?article[^>]*>']:
        essay_html = re.sub(tag, '', essay_html, flags=re.IGNORECASE)
    essay_html = essay_html.strip()

    # 5. 결과 저장
    output_file = os.path.join(ESSAY_DIR, f"essay_{today.strftime('%Y%m%d')}.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(essay_html)
    print(f"📄 에세이 저장: {output_file}")

    if dry_run:
        print("🔍 dry-run 모드: 코드 반영 안 함")
        return

    # 6. app.py에 에세이 삽입
    inject_to_app(category, today, essay_html)
    print("✅ 에세이 발행 완료! (app.py 업데이트됨)")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    run(dry_run=dry_run)
