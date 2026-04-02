# ☕ cafe-auto-blog

매일 오전 9시(KST), 카페 관련 정보성 블로그 글을 자동 생성해서 저장하는 파이프라인이에요.

## 구조

```
cafe-auto-blog/
├── .github/
│   └── workflows/
│       └── generate.yml   # GitHub Actions 스케줄러
├── posts/
│   ├── 2025-04-02.md      # 날짜별 자동 생성 글
│   ├── 2025-04-03.md
│   └── ...
├── generate_post.py       # 글 생성 스크립트
└── README.md
```

## 설정 방법

1. 이 레포를 GitHub에 생성 (`cafe-auto-blog`)
2. Settings → Secrets → Actions에서 시크릿 추가:
   - `ANTHROPIC_API_KEY` : Anthropic API 키
3. Actions 탭에서 워크플로우 활성화
4. 매일 오전 9시에 자동으로 `posts/` 폴더에 글이 쌓여요!

## 주제 목록

커피 상식, 디저트 트렌드, 원두 로스팅, 카페 에티켓, 홈카페,
콜드브루, 플랫화이트, 에스프레소, 브런치 메뉴 등 30가지 주제가
날짜 기반으로 순환돼요.

## 수동 실행

Actions 탭 → Daily Cafe Blog Post Generator → Run workflow
