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
        "패션": "P030201",
        "쇼핑": "P030101",
        "교육": "P010104",
    }
    code = persona_map.get(category)
    if not code or not os.path.exists(PERSONA_FILE):
        return None
    with open(PERSONA_FILE, "r") as f:
        data = json.load(f)
    return data.get(code)


def build_prompt(category, trends, persona):
    """에세이 생성 프롬프트 구성"""
    today = datetime.now().strftime("%Y.%m.%d")
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
롱블랙 스타일로 한 편의 에세이를 작성하세요.

## 규칙
1. 제목은 "'OO 관심자' 타겟팅 금지! [구체적 오디언스]" 형식
2. 가상의 광고주 마케터 인터뷰 포함 (이름은 알파벳 1글자+씨)
3. DMP 앱 데이터로 실제 잡을 수 있는 시그널만 사용
   - 가능: 앱 설치, 사용 빈도, 동시 설치, 타이밍
   - 불가: 앱 내부 행동, 검색어, 구매 금액
4. 비교표 포함 (구경꾼 vs 진짜 타겟)
5. 광고 카피 비교 (❌ 기존 vs ✅ 새 오디언스)
6. 추적 가능한 앱: {apps}
7. 짧은 문장, 많은 줄바꿈, 롱블랙 톤

## 오늘의 카테고리: {category}
## 날짜: {today}

## 최신 트렌드 (3일 이내 뉴스):
{trend_text}

{persona_text}

## 출력 형식
HTML로 출력하세요. class는 다음을 사용:
- note-body, lead, quote (본문)
- sig-box, sig-label (시그널 박스)
- cmp-grid, cmp-card, cmp-left, cmp-right (비교표)
- ind-grid, ind-card, ind-title, ind-desc (추천 업종)
- insight, ins-label (인사이트)

마지막에 AUDIENCE CARD (다크 배경 #111) 포함.
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
            modelId="us.anthropic.claude-3-5-haiku-20241022-v1:0",
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


def update_meta(category, today, essay_html):
    """essays/meta.json에 새 에세이 추가, HTML 파일 저장"""
    meta_path = os.path.join(ESSAY_DIR, "essays", "meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
    else:
        meta = []

    next_num = max((e["number"] for e in meta), default=0) + 1
    date_str = today.strftime("%Y-%m-%d")
    colors = CATEGORY_COLORS.get(category, ("#333", "#666", "📝"))

    # Extract title/subtitle from HTML
    import re
    title_m = re.search(r'class="lead"[^>]*>(.*?)</[^>]+>', essay_html, re.DOTALL)
    raw_title = re.sub(r'<[^>]+>', ' ', title_m.group(1)).strip() if title_m else category
    lines = [l.strip() for l in raw_title.split('\n') if l.strip()]
    title = lines[0] if lines else category
    subtitle = lines[1] if len(lines) > 1 else title

    essay_id = f"{category}_{next_num:02d}"

    entry = {
        "id": essay_id,
        "number": next_num,
        "date": date_str,
        "category": category,
        "emoji": colors[2],
        "color_from": colors[0],
        "color_to": colors[1],
        "title": title[:40],
        "subtitle": subtitle[:40],
        "summary_label": f"{category} 오디언스 인사이트",
        "industries": category,
    }
    meta.append(entry)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # Save essay HTML
    html_path = os.path.join(ESSAY_DIR, "essays", f"{essay_id}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(essay_html)
    print(f"📋 meta.json 업데이트: #{next_num} {essay_id}")


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

    # 5. 결과 저장
    output_file = os.path.join(ESSAY_DIR, f"essay_{today.strftime('%Y%m%d')}.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(essay_html)
    print(f"📄 에세이 저장: {output_file}")

    if dry_run:
        print("🔍 dry-run 모드: 코드 반영 안 함")
        return

    # 6. meta.json 업데이트 — app.py가 자동으로 읽음
    update_meta(category, today, essay_html)
    print("✅ 에세이 발행 완료! (meta.json 업데이트됨)")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    run(dry_run=dry_run)
