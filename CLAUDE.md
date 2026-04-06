# 기계공학실험(2) 레포트 에이전트

## 목적

pre-lab / post-lab 레포트 초안을 자동 생성하는 멀티 에이전트 시스템.

## 사용법

"레포트 작성", "pre-lab", "post-lab" 등을 언급하면 **orchestrator** 에이전트가 자동 실행된다.
실험명·종류(pre/post)·입력 파일 위치를 알려주면 된다.

## 디렉터리

```
input/manual/   — 실험 매뉴얼
input/lecture/  — 강의안
input/form/     — 레포트 양식
input/gpt/      — 족보(선배 레포트) — 문체 분석에만 사용, 내용 참조 금지
output/         — 최종 결과물
tmp/            — 에이전트 간 중간 파일
```

## 핵심 규칙

- 족보는 **문체 분석 전용** (Style Analyzer만 접근). 수치·결론 절대 참조 금지.
- LaTeX 수식은 Word 수식 편집기 호환 형식으로 작성.
- 응답 언어: 한국어.
