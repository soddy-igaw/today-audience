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
    4: "자동차",  # 금
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
    "여행": ["해외여행 취소", "국내여행 전환", "항공편 결항", "호르무즈 여행", "제주 숙소"],
    "증권": ["주식 폭락", "안전자산 금", "달러 환전", "ETF 투자"],
    "게임": ["스위치2", "GTA6", "게이밍 노트북", "신작 게임"],
    "자동차": ["전기차 보조금", "하이브리드 전환", "중고차 시세", "자동차 보험"],
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
    "여행": ["야놀자", "여기어때", "스카이스캐너", "트립닷컴", "네이버지도"],
    "증권": ["토스증권", "키움증권", "금방", "한국금거래소"],
    "게임": ["스팀", "닌텐도", "쿠팡", "네이버쇼핑"],
    "자동차": ["KB차차차", "엔카", "카이즈유", "마이클"],
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
    "여행": ("#0c4a6e", "#0ea5e9", "✈️"),
    "증권": ("#713f12", "#eab308", "📈"),
    "게임": ("#3b0764", "#7c3aed", "🎮"),
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


def query_audience_size(category):
    """Athena에서 카테고리별 교차 시그널 ADID 수 실측"""
    CROSS_QUERIES = {
        "금융": ("대출앱+은행앱", "%대출%", "%은행%"),
        "부동산": ("부동산앱+대출/은행앱", "%부동산%", "%대출%"),
        "쇼핑": ("쇼핑앱+가격비교앱", "%종합쇼핑%", "%가격비교%"),
        "골프": ("골프앱+비즈니스앱", "%골프%", "%비즈니스%"),
        "반려동물": ("반려동물앱+쇼핑앱", "%반려%", "%쇼핑%"),
        "헬스": ("운동앱 2개+쇼핑앱", "%운동%", "%쇼핑%"),
        "여행": ("여행/숙박앱 2개 이상", "%여행%", "%숙박%"),
        "증권": ("증권앱+은행앱", "%증권%", "%은행%"),
        "게임": ("게임앱+가전앱", "%게임%", "%가전%"),
        "패션": ("패션앱+쇼핑앱", "%패션%", "%쇼핑%"),
        "교육": ("교육앱+취업앱", "%교육%", "%취업%"),
    }
    entry = CROSS_QUERIES.get(category)
    if not entry:
        return None
    label, cate_a, cate_b = entry
    try:
        import boto3
        from datetime import timedelta
        end = datetime.now()
        start = end - timedelta(days=30)
        s_key = int(start.strftime("%Y%m%d"))
        e_key = int(end.strftime("%Y%m%d"))
        client = boto3.Session(region_name="ap-northeast-1").client("athena")
        sql = f"""
WITH a AS (SELECT DISTINCT adid FROM DMP_ONESTORE.PACKAGE_USAGE_ALL_V2
  WHERE PACKAGE_NAME IN (SELECT PACKAGE_NAME FROM DMP.ST_CATEGORY WHERE TOTAL_CATE LIKE '{cate_a}')
  AND SEARCH_KEY BETWEEN {s_key} AND {e_key}),
b AS (SELECT DISTINCT adid FROM DMP_ONESTORE.PACKAGE_USAGE_ALL_V2
  WHERE PACKAGE_NAME IN (SELECT PACKAGE_NAME FROM DMP.ST_CATEGORY WHERE TOTAL_CATE LIKE '{cate_b}')
  AND SEARCH_KEY BETWEEN {s_key} AND {e_key})
SELECT COUNT(DISTINCT a.adid) FROM a JOIN b ON a.adid = b.adid"""
        import time
        qid = client.start_query_execution(
            QueryString=sql,
            ResultConfiguration={"OutputLocation": "s3://ai-profiling-tokyo/soddy/today_audience_query/"},
            WorkGroup="mi.ai"
        )["QueryExecutionId"]
        for _ in range(60):
            time.sleep(5)
            r = client.get_query_execution(QueryExecutionId=qid)
            state = r["QueryExecution"]["Status"]["State"]
            if state == "SUCCEEDED":
                rows = client.get_query_results(QueryExecutionId=qid)["ResultSet"]["Rows"]
                count = int(rows[1]["Data"][0]["VarCharValue"]) if len(rows) > 1 else 0
                man = count // 10000
                return {"count": count, "label": f"~{man}만 명", "signal": f"{label} · DMP 실측"}
            elif state in ("FAILED", "CANCELLED"):
                return None
    except Exception as e:
        print(f"⚠️ Athena 쿼리 실패: {e}")
    return None


def build_prompt(category, trends, persona, page_type=None):
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

    # 페이지 타입 결정
    if not page_type:
        types = ["감정형", "인사이트형", "데이터형"]
        page_type = types[datetime.now().timetuple().tm_yday % 3]

    # 타입별 템플릿 로드
    type_file_map = {"감정형": "emotion.html", "인사이트형": "insight.html", "데이터형": "data.html"}
    tmpl_file = os.path.join(ESSAY_DIR, "templates", type_file_map.get(page_type, "emotion.html"))
    ref_html = ""
    if os.path.exists(tmpl_file):
        with open(tmpl_file, "r") as f:
            ref_html = f.read()
    else:
        # fallback: 기존 에세이
        ref_file = os.path.join(ESSAY_DIR, "essays_html", "coupang_exit.html")
        if os.path.exists(ref_file):
            with open(ref_file, "r") as f:
                ref_html = f.read()

    return f"""당신은 IGAWorks의 "오늘의 오디언스" 에세이 작가입니다.

## 에세이 컨셉
시장 트렌드를 읽고, 행동 시그널을 조합해 아직 아무도 안 쓰는 오디언스를 제안합니다.
타겟: 광고 마케터, AE, 광고주. "지금 이 시그널을 잡아야 합니다"를 전달.

## 톤 & 스타일
- 토스 피드 + 브런치형: 읽히면서도 타겟이 보이게
- 문장은 짧게. 불필요한 수식어 제거. 한 문장 끝나면 <br> 넣기
- 확신 있는 문체: "~로 보입니다" 대신 "~입니다"
- em dash(—) 뒤에 반드시 공백
- 근거/출처는 "출처: OO" 형태로 명시

## 오늘의 페이지 타입: {page_type}

3가지 타입 중 오늘은 **{page_type}**으로 작성하세요:

### 감정형 — "이 사람의 하루"
- 페르소나의 감정과 상황을 깊게 묘사하며 시작
- 독자가 "나도 이런 사람 봤다"고 공감하게
- 스토리 중심, 시그널은 자연스럽게 녹여서
- 마무리: 이 감정이 어떤 소비 행동으로 이어지는지

### 인사이트형 — "광고주가 몰랐던 시그널"
- 의외의 데이터 조합이나 반직관적 발견으로 시작
- "A앱 사용자가 왜 B앱을 깔까?" 같은 질문 던지기
- 시그널 해석 중심, 페르소나는 보조적으로
- 마무리: 이 인사이트를 광고에 어떻게 쓰는지

### 데이터형 — "숫자가 말하는 타겟"
- 수치와 비교 데이터로 시작 (전주 대비, 전월 대비)
- 구경꾼 vs 진짜 타겟을 데이터로 분리
- 차트/비교표 중심, 감정은 최소화
- 마무리: 이 숫자가 광고주에게 의미하는 것

## 필수 규칙: 행동 정의 문장
모든 글에 반드시 아래 형식의 문장을 1개 이상 포함하세요:
- ❌ 추상적: "이탈자", "관심자", "잠재 고객"
- ✅ 행동 기반: "결제 직전 앱을 닫은 사람", "3일 연속 가격비교앱을 연 사람", "대출앱 3개를 동시에 깐 사람"
- 이 문장은 highlight-line 또는 punchline에 배치

## 에세이 3막 구조

### 1막: 상황 — 왜 지금인가
### 2막: 타겟 정의 — 이 사람은 누구인가 (행동 기반으로 정의)
### 3막: 전환 — 어떤 소비/행동으로 이어지고, 광고주가 어디에 쓸 수 있는가

## 제목 규칙
- 직관적이고 짧게. 광고주가 한눈에 타겟을 알 수 있게
- "~하는 사람"으로만 끝내지 마세요. 다양한 형식:
  - 타이밍형: "쿠팡 삭제 후 72시간", "금리 만기 D-30"
  - 현상형: "운동 2주차의 벽", "전세 만기 카운트다운"
  - 질문형: "PT 끊은 사람이 다음에 깔은 앱은?"
- **중요: hero의 h1 제목과 audience-box의 h3 오디언스 이름은 반드시 동일하게 사용하세요**
- **중요: 제목/타겟명에 숫자, 퍼센트(%), 통계 수치를 넣지 마세요. 숫자는 본문에서 사용하세요**
- **중요: 제목만 보고 "어떤 사람인지" 바로 알 수 있어야 합니다. 감성적/추상적 제목 금지**
  - ❌ "내연기관 마지막 사랑", "전세 만기의 불안감", "필드 첫 날의 배신"
  - ❌ "홈트 앱 3개 동시 설치자 +47%", "대출앱 삭제 후 ETF 검색량 3배 증가"
  - ✅ "전기차 포기하고 하이브리드 찾는 사람", "쿠팡 삭제 후 알리 깐 사람", "PT 끊고 홈트앱으로 갈아탄 사람"
  - 핵심: 행동이 보이는 제목. "~한 사람"으로만 끝내지 말되, 타겟이 직관적으로 보여야 함
- 서브타이틀에서 타겟을 구체적으로 설명

## 필수 HTML 구조 — 토스 카드 스타일

반드시 아래 참고 HTML의 클래스명과 구조를 그대로 사용하세요:
- hero (tag, h1, sub, meta)
- punchline (핵심 한 문장 — 행동 정의 문장 배치)
- quote (가상 인터뷰)
- card + s-label (왜 지금인가)
- card + steps > step/step.active (행동 시그널 3단계)
- highlight-line (매력 포인트 — 행동 정의 문장 배치)
- card + compare (비교 그리드)
- audience-box (오디언스 규모)
- card + biz-item 아코디언 (광고주 활용 3개 — "어디에 쓸 수 있는지" 명확히)
- cta-bar
- footer

## DMP로 추적 가능한 시그널만 사용
- 앱 설치/삭제, 사용 빈도 변화, 사용 시간대
- 동시 설치 속도, 앱 조합 패턴
- ❌ 앱 내부 탭/검색어/장바구니는 추적 불가 — 절대 사용 금지

## 색상: 흑백 기조 + 포인트 #e8530e

## 규칙
- <style> 태그 없이 HTML 본문만 출력 (CSS는 빌드 시 자동 주입)
- <div class="back"> 으로 시작
- <!DOCTYPE>, <html>, <head>, <body> 태그 절대 금지
- 추적 가능한 앱: {apps}

## 참고: {page_type} 템플릿 HTML (이 구조를 그대로 따라하세요)
{ref_html}

## 오늘의 카테고리: {category}
## 날짜: {today_str}

## 최신 트렌드:
{trend_text}

{persona_text}

## 푸터 문구 (반드시 이것 사용):
<div class="footer"><div style="margin-bottom:6px">본 리포트는 IGAWorks의 DMP 행동 데이터를 시장 트렌드에 맞춰 자동 생성한 오디언스 분석입니다.</div><div style="margin-bottom:6px">데이터 기준: 모바일인덱스 실측 · © 2026 IGAWorks</div><div>made by soddy</div></div>
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
    import time
    data = json.dumps({
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 8192,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            print(f"   OpenAI 에러 {e.code} (시도 {attempt+1}/3): {body[:200]}")
            if e.code == 429 and attempt < 2:
                wait = 30 * (attempt + 1)
                print(f"   {wait}초 후 재시도...")
                time.sleep(wait)
            else:
                return None
    return None


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

    # 1. Save essay HTML — 토스 스타일 CSS 주입 + 정리
    essay_file = os.path.join(ESSAY_DIR, "essays_html", f"{essay_id}.html")
    cleaned = '\n'.join(line for line in essay_html.split('\n') if line.strip())
    # 토스 스타일 CSS가 없으면 주입
    if 'body{background:#f7f7fa' not in cleaned:
        toss_css_file = os.path.join(ESSAY_DIR, "essays_html", "coupang_exit.html")
        if os.path.exists(toss_css_file):
            with open(toss_css_file, "r") as tcf:
                toss_content = tcf.read()
            # <style>...</style> 블록 추출
            style_match = _re.search(r'(<style>.*?</style>)', toss_content, _re.DOTALL)
            if style_match:
                cleaned = style_match.group(1) + '\n\n' + cleaned
    with open(essay_file, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print(f"📄 에세이 저장: {essay_file}")

    # 2. Get next essay number
    with open(APP_FILE, "r", encoding="utf-8") as f:
        code = f.read()
    existing = _re.findall(r'"number":\s*(\d+)', code)
    next_num = max(int(n) for n in existing) + 1 if existing else 1

    # 3. Determine chapter
    chapter_map = {
        "금융": "금융", "부동산": "금융", "증권": "금융",
        "골프": "스포츠", "헬스": "스포츠", "러닝": "스포츠",
        "쇼핑": "라이프", "반려동물": "라이프", "자동차": "라이프",
        "게임": "게임", "여행": "여행", "교육": "라이프",
    }
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

    # 6. Update build_static.py ESSAYS too
    build_script = os.path.join(ESSAY_DIR, "build_static.py")
    if os.path.exists(build_script):
        with open(build_script, "r", encoding="utf-8") as f:
            bcode = f.read()
        new_build_entry = (
            f'    {{"id":"{essay_id}","tag":"{category}","title":"{title}",'
            f'"sub":"{sub[:80]}","stat":"{stat}","stat_label":"{stat_label}",'
            f'"date":"{date_fmt}"}},\n'
        )
        bcode = bcode.replace('ESSAYS = [\n', f'ESSAYS = [\n{new_build_entry}')
        with open(build_script, "w", encoding="utf-8") as f:
            f.write(bcode)

    # 7. Rebuild static site
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

    # 2.5 Athena 실측 모수
    print("📊 DMP 실측 모수 조회 중...")
    audience = query_audience_size(category)
    if audience:
        print(f"   → {audience['label']} ({audience['signal']})")
    else:
        print("   ⚠️ 실측 조회 실패 — 추정치 사용")

    # 3. 프롬프트 생성
    prompt = build_prompt(category, trends, persona)
    if audience:
        prompt += f"\n\n[DMP 실측 데이터]\n추정 규모: {audience['label']}\n시그널: {audience['signal']}\n※ 이 숫자를 data-box에 반드시 사용하세요."

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
