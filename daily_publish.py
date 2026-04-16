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
자사 DMP 페르소나 데이터:
- 페르소나명: {persona['name']}
- 추정 모수: {persona.get('estimate_min', '?'):,}~{persona.get('estimate_max', '?'):,}명
- 산출 근거: {persona.get('basis', '')}
- 출처: {persona.get('source', '')}
"""

    return f"""당신은 IGAWorks의 "오늘의 오디언스" 에세이 작가입니다.
롱블랙 스타일로 한 편의 에세이를 작성하세요. 최소 3000자 이상.

## 에세이 컨셉
1. 최근 시장 트렌드가 이렇다 (뉴스/데이터 기반)
2. 해당 업종 인하우스 광고주(마케터)는 아직 명확한 오디언스를 못 찾고 있다
3. 시장 트렌드와 유저들의 행동 패턴을 보면 이런 시그널이 보인다
4. 자사 DMP로는 이 패턴을 이렇게 찾을 수 있다!

## IGAWorks DMP에서 추적 가능한 유저 행동 시그널
단순 "앱 설치 여부"가 아니라, 유저의 행동 맥락을 조합해서 의도를 읽어야 합니다.

### 추적 가능한 행동 데이터:
- **앱 설치/삭제 타이밍**: 언제 깔았는지, 며칠 만에 삭제했는지
- **앱 사용 빈도 변화**: 주 1회 → 매일, 또는 매일 → 안 씀 (이탈 시그널)
- **앱 사용 시간대**: 출퇴근(7-9시/18-20시), 점심(12-13시), 심야(23-02시)
- **앱 카테고리 이동 패턴**: 뉴스앱 → 금융앱 → 부동산앱 순서로 이동
- **동시 설치 속도**: 같은 카테고리 앱 N개를 며칠 내에 설치 (비교쇼핑 시그널)
- **앱 조합 패턴**: A앱+B앱+C앱을 동시에 쓰는 사람 (의도 추정)
- **사용 기기 정보**: OS, 기기 가격대 (구매력 추정)
- **위치 기반 패턴**: 특정 지역 체류 시간 변화 (이사/출퇴근 변화)
- **푸시 알림 반응률**: 알림 클릭 vs 무시 (관여도)
- **앱 내 체류 시간 변화**: 짧게 확인 vs 오래 탐색 (탐색 깊이)
- **신규 vs 복귀 유저**: 90일 미사용 후 재설치 (계기 발생)
- **크로스 카테고리 행동**: 골프앱 쓰다가 명품앱 설치 (라이프스타일 변화)

### 추적 불가능한 것:
- 앱 내부 검색어, 장바구니, 결제 금액
- 웹 브라우징 기록
- 개인 신용정보, 소득, 자산

## 행동 시그널 설계 원칙
1. **단일 시그널이 아니라 시그널 조합**으로 의도를 추정
   - 나쁜 예: "대출앱 설치자" → 너무 넓음
   - 좋은 예: "대출 비교앱 3개를 7일 내 설치 + 매일 접속 + 기존 은행앱 사용 감소" → 갈아타기 직전
2. **시간축 변화**가 핵심 — "지금 이 행동을 하고 있다"가 아니라 "최근 N일간 행동이 이렇게 변했다"
3. **행동의 속도와 강도**로 긴급도를 구분
   - 천천히 1개씩 = 관심 단계
   - 빠르게 여러 개 동시 = 실행 직전
4. **이탈 시그널도 중요** — 기존에 쓰던 앱을 안 쓰기 시작하면 전환 시그널

## 규칙
1. 제목: "'OO 관심자' 타겟팅 금지! [구체적 오디언스]" 형식
2. 가상의 인하우스 마케터 인터뷰 (이름은 알파벳 1글자+씨). 실제 업무 고민을 구체적으로.
3. 위의 DMP 행동 시그널만 사용. 단순 앱 설치가 아니라 행동 패턴 조합으로 설계.
4. 비교표: 구경꾼 vs 진짜 타겟 — 행동 패턴의 차이를 구체적으로 (각 5줄+)
5. 광고 카피 비교 (❌ 기존 vs ✅ 새 오디언스)
6. 추적 가능한 앱: {apps}
7. 짧은 문장, 많은 줄바꿈, 롱블랙 톤
8. 추천 업종 4개+ (구체적 캠페인 아이디어 포함)
9. AUDIENCE CARD (다크 배경 #111) — 추정 모수("N~N만" 형식), 핵심 시그널 조합, 추천 업종, 메시지

## 필수 구조:
1. <p class="lead"> 제목/부제
2. <div class="quote"> 마케터 첫 인용 (실제 업무 고민)
3. 시장 현황 + 기존 타겟팅의 한계 (3~4 문단, 트렌드 뉴스 인용)
4. <div class="sig-box"> BEHAVIOR SIGNALS — 행동 시그널 조합 5개+ (각각 왜 이 행동이 의미있는지 설명)
5. 핵심 해석 — 이 시그널 조합이 왜 기존 타겟팅보다 나은지 (2~3 문단)
6. <div class="cmp-grid"> 비교표 (행동 패턴 기준)
7. <div class="sig-box"> DMP에서 잡는 법 — 구체적 조건 조합 (AND/OR, 기간, 빈도)
8. <div class="ind-grid"> 추천 업종 4개 (구체적 캠페인 메시지)
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
HTML 조각만 출력. <!DOCTYPE>, <html>, <head>, <body>, <article> 태그 절대 금지.
<div class="note-body">로 시작.
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
