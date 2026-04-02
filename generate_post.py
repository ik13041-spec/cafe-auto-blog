import anthropic
import os
from datetime import datetime, timedelta
import hashlib

# 카페 관련 주제 목록 (매일 다르게 순환)
TOPICS = [
    ("커피 상식", "아메리카노 vs 롱블랙, 뭐가 다를까? 카페에서 알고 마시면 더 맛있는 커피 상식"),
    ("디저트 트렌드", "2025년 카페 디저트 트렌드 총정리 — 요즘 뜨는 메뉴는?"),
    ("커피 원두", "원두 로스팅 단계별 차이 — 라이트, 미디엄, 다크 어떻게 고를까?"),
    ("카페 분위기", "혼자 가기 좋은 카페 고르는 법 — 이런 카페가 진짜 좋은 카페"),
    ("음료 추천", "계절별 카페 음료 추천 — 지금 이 계절엔 이걸 마셔요"),
    ("카페 에티켓", "카페에서 지켜야 할 에티켓 — 알면 더 편한 카페 문화"),
    ("홈카페", "집에서 카페 느낌 내는 법 — 홈카페 입문자를 위한 가이드"),
    ("라떼 종류", "라떼의 세계 — 카페라떼, 바닐라라떼, 말차라떼 차이 총정리"),
    ("카페 창업", "카페 창업 전 알아야 할 것들 — 현실적인 이야기"),
    ("시럽/첨가물", "카페 시럽 종류와 활용법 — 내 취향에 맞는 음료 커스텀하기"),
    ("디카페인", "디카페인 커피, 정말 괜찮을까? 카페인에 민감한 분들을 위한 정보"),
    ("우유 종류", "오트밀크, 두유, 아몬드밀크 — 식물성 우유 완전 정복"),
    ("케이크 종류", "카페 케이크 종류 총정리 — 생크림, 무스, 치즈케이크 차이는?"),
    ("아이스크림", "카페 아이스크림 메뉴 활용법 — 이렇게 먹으면 더 맛있어요"),
    ("카페 인테리어", "손님을 끌어당기는 카페 인테리어의 비밀"),
    ("브런치 메뉴", "카페 브런치 메뉴 트렌드 — 요즘 카페에서 꼭 먹어봐야 할 것들"),
    ("커피와 건강", "커피, 하루 몇 잔까지 괜찮을까? 커피와 건강 이야기"),
    ("SNS 카페", "SNS에서 뜨는 카페 — 인스타 감성 카페의 특징은?"),
    ("쿠키/마들렌", "카페 쿠키와 마들렌 — 어떻게 만들길래 이렇게 맛있을까?"),
    ("카페 음악", "카페 BGM의 비밀 — 음악이 커피 맛에 영향을 준다고?"),
    ("콜드브루", "콜드브루 커피란? 일반 아이스 커피와 다른 점 총정리"),
    ("플랫화이트", "플랫화이트가 뭐예요? 카페 메뉴판의 낯선 이름들 해설"),
    ("당도 조절", "카페 음료 당도 조절하는 법 — 덜 달게, 더 건강하게"),
    ("카페 포장", "테이크아웃 커피 더 맛있게 마시는 법"),
    ("에스프레소", "에스프레소 기초 — 싱글, 더블, 리스트레토가 뭔지 알고 주문하자"),
    ("플레이팅", "카페 디저트 플레이팅 — 눈으로 먼저 먹는 예쁜 디저트의 세계"),
    ("카페 창가", "창가 자리가 인기 있는 이유 — 카페 공간 심리학"),
    ("티 메뉴", "카페에서 차 주문하기 — 얼그레이, 캐모마일, 루이보스 차이"),
    ("스무디/에이드", "카페 에이드와 스무디 — 종류별 특징과 추천"),
    ("카페 쿠폰", "카페 쿠폰 & 멤버십 200% 활용하는 법"),
]

def get_today_topic():
    """날짜 기반으로 매일 다른 주제 선택"""
    today = datetime.now()
    # 날짜를 숫자로 변환해서 주제 순환
    day_index = (today.year * 365 + today.month * 30 + today.day) % len(TOPICS)
    return TOPICS[day_index]

def generate_post(topic_title, topic_desc):
    """Claude API로 블로그 글 생성"""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""당신은 감성 있는 카페 블로그 작가입니다.
아래 주제로 네이버 블로그에 올릴 정보성 글을 작성해주세요.

주제: {topic_title}
방향: {topic_desc}

작성 조건:
- 분량: 600~800자 내외
- 말투: 친근하고 따뜻한 ~해요 체
- 구성: 도입 → 본문 (소제목 2~3개) → 마무리
- 실용적인 정보 위주로, 카페를 좋아하는 일반인이 읽기 쉽게
- 과도한 마케팅 느낌 없이 자연스럽게
- 마지막에 해시태그 5개 추가 (예: #카페추천 #커피상식 등)

마크다운 형식으로 작성해주세요."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text

def save_post(content, topic_title):
    """posts 폴더에 날짜별로 저장"""
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("posts", exist_ok=True)

    filename = f"posts/{today}.md"

    full_content = f"""---
date: {today}
topic: {topic_title}
---

{content}
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"✅ 저장 완료: {filename}")
    return filename

def main():
    print(f"🕘 실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    topic_title, topic_desc = get_today_topic()
    print(f"📌 오늘의 주제: {topic_title}")

    print("✍️ 글 생성 중...")
    content = generate_post(topic_title, topic_desc)

    filename = save_post(content, topic_title)
    print(f"🎉 완료! {filename}")

if __name__ == "__main__":
    main()
