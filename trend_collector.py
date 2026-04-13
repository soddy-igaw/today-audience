"""
오늘의 오디언스 — 트렌드 수집기
매일 아침 실행하여 최신 트렌드 데이터를 수집합니다.

소스:
1. 네이버 뉴스 API — 업종별 최신 기사
2. 구글 트렌드 — 검색량 급상승 키워드
3. 앱스토어 순위 — 카테고리별 급상승 앱

사용법:
  python trend_collector.py --category 금융
  python trend_collector.py --all
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

# === 설정 ===
CATEGORIES = {
    "금융": ["대출 갈아타기", "금 투자", "ETF", "증권 계좌", "금리 비교"],
    "증권": ["금 ETF", "해외주식", "미국주식", "배당주", "로보어드바이저"],
    "부동산": ["전세 만기", "아파트 매매", "이사", "부동산 앱", "전세대출"],
    "골프": ["골프 입문", "스크린골프", "골프웨어", "골프 레슨", "여성 골퍼"],
    "교육": ["코딩 교육", "AI 교육", "이직 준비", "자격증", "온라인 강의"],
    "쇼핑": ["알리익스프레스", "테무", "쿠팡", "새벽배송", "중고거래"],
    "배달": ["배달앱", "배달비", "쿠팡이츠", "배달의민족", "요기요"],
    "패션": ["러닝크루", "콰이어트럭셔리", "중고명품", "러닝화", "골프웨어"],
    "헬스": ["헬스장 PT", "러닝크루", "홈트레이닝", "크로스핏", "필라테스"],
}

# 앱 카테고리별 추적 대상
APP_WATCHLIST = {
    "금융": ["뱅크샐러드", "핀다", "토스", "카카오뱅크", "금방", "한국금거래소"],
    "증권": ["토스증권", "키움증권", "미래에셋", "삼성증권", "카카오페이증권"],
    "부동산": ["직방", "다방", "호갱노노", "네이버부동산", "KB부동산"],
    "골프": ["카카오VX", "골프존", "스마트스코어", "티스캐너", "김캐디"],
    "배달": ["배달의민족", "쿠팡이츠", "요기요"],
    "쇼핑": ["쿠팡", "알리익스프레스", "테무", "번개장터", "크림"],
    "교육": ["클래스101", "패스트캠퍼스", "인프런", "스파르타코딩", "듀오링고"],
    "헬스": ["캐치핏", "나이키런클럽", "킵", "애플피트니스", "눔"],
}


def search_naver_news(query, display=5):
    """구글 뉴스 RSS로 한국어 최신 뉴스 검색"""
    encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded}+when:7d&hl=ko&gl=KR&ceid=KR:ko"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode("utf-8", errors="ignore")
            titles = []
            for item in data.split("<title>")[2:display+2]:
                t = item.split("</title>")[0].strip()
                if t and t != "Google 뉴스":
                    titles.append(t)
            return titles
    except Exception as e:
        return [f"(검색 실패: {e})"]


def get_trending_keywords(category):
    """카테고리별 트렌드 키워드 뉴스 수집"""
    keywords = CATEGORIES.get(category, [])
    results = {}
    for kw in keywords:
        news = search_naver_news(kw, display=3)
        results[kw] = news
    return results


def generate_audience_ideas(category, trends):
    """트렌드 → 오디언스 아이디어 변환"""
    ideas = []
    apps = APP_WATCHLIST.get(category, [])

    for keyword, news_titles in trends.items():
        if not news_titles or "(검색 실패" in str(news_titles):
            continue

        idea = {
            "keyword": keyword,
            "news_sample": news_titles[0] if news_titles else "",
            "audience_idea": f"'{keyword}' 관련 앱을 최근 처음 설치한 사람",
            "dmp_signal": f"{', '.join(apps[:3])} 등 앱 첫 설치 + 설치 후 3일 내 활성 사용",
            "advertiser": f"{category} 업종 광고주",
        }
        ideas.append(idea)

    return ideas


def collect_all(category=None):
    """전체 수집 실행"""
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    cats = [category] if category else list(CATEGORIES.keys())

    report = {
        "collected_at": today,
        "categories": {}
    }

    for cat in cats:
        print(f"\n📡 [{cat}] 트렌드 수집 중...")
        trends = get_trending_keywords(cat)
        ideas = generate_audience_ideas(cat, trends)

        report["categories"][cat] = {
            "trends": trends,
            "audience_ideas": ideas,
            "watchlist_apps": APP_WATCHLIST.get(cat, []),
        }

        # 요약 출력
        print(f"  키워드 {len(trends)}개 검색 완료")
        for idea in ideas:
            print(f"  💡 {idea['audience_idea']}")
            print(f"     뉴스: {idea['news_sample'][:60]}...")
            print(f"     시그널: {idea['dmp_signal']}")

    # 결과 저장
    output_file = f"trend_report_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 리포트 저장: {output_file}")

    return report


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "--category":
        collect_all(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "--all":
        collect_all()
    else:
        print("사용법:")
        print("  python trend_collector.py --category 금융")
        print("  python trend_collector.py --all")
        print(f"\n지원 카테고리: {', '.join(CATEGORIES.keys())}")
