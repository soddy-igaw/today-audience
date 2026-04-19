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
자사 페르소나 데이터:
- 페르소나명: {persona['name']}
- 추정 모수: {persona.get('estimate_min', '?'):,}~{persona.get('estimate_max', '?'):,}명
"""

    # 기존 에세이 참고용
    ref_file = os.path.join(ESSAY_DIR, "essays_html", "realestate.html")
    ref_html = ""
    if os.path.exists(ref_file):
        with open(ref_file, "r") as f:
            ref_html = f.read()[:3000]

    return f"""당신은 IGAWorks의 "오늘의 오디언스" 에세이 작가입니다.

## 에세이 컨셉
시장 트렌드를 읽고, 행동 시그널을 조합해 아직 아무도 안 쓰는 오디언스를 제안합니다.
타겟: 광고 마케터, AE, 광고주. "이 사람한테 광고하면 됩니다"를 전달.

## 필수 구조 (이 순서 그대로)
1. detail-hero: 제목(타겟 직관형 — "OO하는 사람"), 서브타이틀, 날짜
2. quote-box: 가상 페르소나 인터뷰 (감정 있게, 구체적 상황)
3. section "무슨 일이 벌어지고 있나": 시장 배경 2~3문단
4. quote-box: 페르소나 두 번째 인터뷰 (더 깊은 디테일)
5. section "이 사람의 행동 패턴": 타임라인 (DAY 0 → DAY 14)
6. section "이 사람을 찾는 법": 시그널 카드 4개 (앱 이름 + 행동)
7. insight-box: KEY INSIGHT 한 문단
8. audience-card: 오디언스 이름, 추정 모수, 핵심 시그널
9. CTA box
10. footer

## DMP로 추적 가능한 시그널만 사용
- 앱 설치/삭제, 사용 빈도 변화, 사용 시간대
- 동시 설치 속도, 앱 조합 패턴
- 커머스 구매 이력, 위치 데이터
- ❌ 앱 내부 탭/검색어/장바구니는 추적 불가 — 절대 사용 금지

## 제목 규칙
- 타겟 직관형: "OO하는 사람" — 광고주가 바로 "이 타겟!" 인지
- 예: "대출 만기 전 대환을 준비하는 사람", "접대 때문에 골프 시작한 입문자"

## CSS 클래스 (반드시 이 클래스만 사용)
detail-wrap, hero-img, detail-hero, detail-emoji, detail-tag, detail-title, detail-sub, detail-meta,
quote-box, section, section-label, tl, tl-item, tl-dot, tl-day, tl-title, tl-desc,
tl-flow, tl-flow-down, tl-flow-up, tl-bar-wrap, tl-bar-bg, tl-bar-fill, tl-alert,
ind-grid, ind-card, ind-title, ind-desc, insight-box, ins-label, audience-card, footer

## 색상: 흑백 기조 + 포인트 #e8530e
- "이 사람을 찾는 법" section-label: style="color:#e8530e"
- ind-card: style="border-left:3px solid #e8530e"
- insight-box 핵심 문장: style="color:#e8530e"
- audience-card 모수 숫자: style="color:#e8530e"
- 타임라인 핵심 시그널 dot: style="background:#e8530e;box-shadow:0 0 0 2px #e8530e"

## 규칙
- HTML 조각만 출력. <div class="detail-wrap">로 시작, </div>로 끝
- <!DOCTYPE>, <html>, <head>, <body> 태그 절대 금지
- 빈 줄 없이 태그 연속 배치
- 추적 가능한 앱: {apps}
- 히어로 이미지는 넣지 마세요 (빌드 시 자동 추가)

## 참고: 기존 에세이 HTML 구조
{ref_html}

## 오늘의 카테고리: {category}
## 날짜: {today_str}

## 최신 트렌드:
{trend_text}

{persona_text}
"""


def call_llm(prompt):
    """LLM API 호출 (Anthropic > OpenAI > Bedrock)"""
    # 1. Anthropic 직접
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        return _call_anthropic(prompt, api_key)

    # 2. OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return _call_openai(prompt, api_key)

    # 3. AWS Bedrock (fallback)
    result = _call_bedrock(prompt)
    if result:
        return result

    print("⚠️  LLM API 사용 불가. ANTHROPIC_API_KEY를 설정하세요.")
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
        "max_tokens": 8192,
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
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print(f"   Anthropic 에러 {e.code}: {body[:200]}")
        return None


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
    """새 에세이를 essays_html/에 저장하고 app.py + 정적 사이트 업데이트"""
    import re as _re
    import subprocess

    colors = CATEGORY_COLORS.get(category, ("#333", "#666", "📝"))
    _, _, emoji = colors
    date_fmt = today.strftime("%Y.%m.%d")
    essay_id = f"{category}_{today.strftime('%m%d')}"

    # Extract title/subtitle from essay HTML
    title_m = _re.search(r'detail-title[^>]*>(.*?)</div>', essay_html, _re.DOTALL)
    title = _re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else category
    sub_m = _re.search(r'detail-sub[^>]*>(.*?)</div>', essay_html, _re.DOTALL)
    sub = _re.sub(r'<[^>]+>', '', sub_m.group(1)).strip() if sub_m else ""
    audience_m = _re.search(r'font-weight:900">([\d~,만억천명\s]+)</p>', essay_html)
    stat = audience_m.group(1).strip() if audience_m else ""

    # 1. Save essay HTML (remove blank lines for Streamlit compat)
    essay_file = os.path.join(ESSAY_DIR, "essays_html", f"{essay_id}.html")
    cleaned = '\n'.join(line for line in essay_html.split('\n') if line.strip())
    with open(essay_file, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print(f"📄 에세이 저장: {essay_file}")

    # 2. Get next essay number
    with open(APP_FILE, "r", encoding="utf-8") as f:
        code = f.read()
    existing = _re.findall(r'"number":\s*(\d+)', code)
    next_num = max(int(n) for n in existing) + 1 if existing else 1

    # 3. Determine chapter and hero image
    chapter_map = {
        "금융": "금융", "부동산": "금융", "증권": "금융",
        "골프": "스포츠", "헬스": "스포츠", "러닝": "스포츠",
        "쇼핑": "라이프", "반려동물": "라이프", "자동차": "라이프",
        "게임": "게임", "여행": "여행", "교육": "라이프",
    }
    hero_images = {
        "금융": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=400&fit=crop&q=80",
        "부동산": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=400&fit=crop&q=80",
        "스포츠": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=400&fit=crop&q=80",
        "게임": "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=800&h=400&fit=crop&q=80",
        "여행": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&h=400&fit=crop&q=80",
        "라이프": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800&h=400&fit=crop&q=80",
    }
    img = hero_images.get(category, hero_images.get(chapter_map.get(category, ""), ""))
    stat_label = f"{category} 오디언스 (DMP)"

    # 4. Insert new card as first ESSAYS entry
    new_card = (
        f'    {{\n'
        f'        "id": "{essay_id}", "emoji": "{emoji}", "tag": "{category}", "number": {next_num},\n'
        f'        "title": "{title}",\n'
        f'        "sub": "{sub[:80]}",\n'
        f'        "stat": "{stat}",\n'
        f'        "stat_label": "{stat_label}",\n'
        f'        "date": "{date_fmt}",\n'
        f'        "color": "#000",\n'
        f'        "img": "{img}",\n'
        f'    }},\n'
    )
    code = code.replace('ESSAYS = [\n', f'ESSAYS = [\n{new_card}')

    # 5. Add routing
    route_block = (
        f'if st.session_state.view == "detail_{essay_id}":\n'
        f'    if st.button("← 뒤로", key="back_{essay_id}"):\n'
        f'        go_feed()\n'
        f'    st.markdown(load_essay("{essay_id}"), unsafe_allow_html=True)\n\n'
        f'elif st.session_state.view == "detail_realestate":'
    )
    code = code.replace(
        'if st.session_state.view == "detail_realestate":',
        route_block,
        1
    )

    with open(APP_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"📝 app.py 업데이트: #{next_num} {essay_id}")

    # 6. Rebuild static site
    build_script = os.path.join(ESSAY_DIR, "build_static.py")
    if os.path.exists(build_script):
        subprocess.run([sys.executable, build_script], cwd=ESSAY_DIR)
        print("🏗️  정적 사이트 재빌드 완료")


def run(dry_run=False, category_override=None):
    """전체 파이프라인 실행"""
    today = datetime.now()

    if category_override:
        category = category_override
    else:
        # 트렌드 기반 자동 선택: 모든 카테고리에서 뉴스 수집, 가장 많은 곳 선택
        print("📡 트렌드 기반 카테고리 자동 선택 중...")
        best_cat, best_count = "금융", 0
        for cat in CATEGORY_KEYWORDS:
            count = len(collect_trends(cat))
            print(f"   {cat}: {count}개 뉴스")
            if count > best_count:
                best_count = count
                best_cat = cat
        category = best_cat

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
    # --category 금융 으로 카테고리 강제 지정 가능
    override = None
    if "--category" in sys.argv:
        idx = sys.argv.index("--category")
        if idx + 1 < len(sys.argv):
            override = sys.argv[idx + 1]
    run(dry_run=dry_run, category_override=override)
