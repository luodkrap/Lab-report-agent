# 기계공학실험 레포트 에이전트

> Pre-lab / Post-lab 레포트 초안을 자동 생성하는 멀티 에이전트 AI 시스템

---

## 개요

실험 매뉴얼, 강의안, 레포트 양식, 실험 결과 데이터를 넣으면 문항별 고품질 한국어 공학 보고서 답변을 자동으로 생성합니다.  
Claude Agent SDK 기반으로 동작하며, 외부 서버 없이 로컬에서 Claude Code CLI만으로 실행됩니다.

---

## 주요 기능

- **Pre-lab / Post-lab 모두 지원** — 이론 정리부터 결과 분석까지
- **멀티 에이전트 파이프라인** — 9개의 전문 에이전트가 역할 분담
- **자연스러운 문체** — 4학년 학부생 스타일로 자동 변환 (GPTZero / Turnitin 통과 목표)
- **족보 문체만 참조** — 선배 레포트의 내용(수치·결론)은 절대 사용하지 않음
- **Word(.docx) 출력** — 수식은 Word 수식 편집기 호환 LaTeX 형식
- **사진 추천 + 참고문헌** — 삽입 위치·출처 추천 및 한국기계학회 인용 형식 지원
- **xlsx 자동 파싱** — 실험 결과 엑셀 파일을 텍스트로 자동 추출

---

## 지원 실험 분야

| 분야 | 실험 수 |
|------|---------|
| 열전달 | 2개 |
| 기계진동 | 2개 |
| 유체역학 | 2개 |
| 동역학 | 2개 |

---

## 에이전트 구조

```
[사용자 입력]
      ↓
  Orchestrator
      ├── Input Analyzer      — 매뉴얼·강의안·양식 파싱, 문항 추출
      ├── Style Analyzer      — 족보 문체 분석 (내용 참조 금지)
      ├── Theory Researcher   — 이론 정리 및 LaTeX 수식 작성
      ├── Report Writer       — 문항별 초안 작성
      ├── Humanizer           — 학부생 문체로 자연스럽게 변환
      ├── Reviewer            — 사실 정확성·논리 검토 및 재작업 요청
      ├── Image Recommender   — 삽입할 사진/그림 위치와 출처 추천
      └── Reference Manager   — 참고문헌 목록 생성
```

---

## 디렉터리 구조

```
report_agent/
├── .claude/agents/         # 에이전트 정의 파일 (마크다운)
├── input/
│   ├── manual/             # 실험 매뉴얼 (PDF, Word)
│   ├── lecture/            # 강의안 (PDF로 변환된 pptx)
│   ├── form/               # 레포트 양식 (PDF, Word)
│   ├── data/               # 실험 결과 데이터 (xlsx, CSV, 이미지)
│   └── jokbo/              # 족보 — 문체 분석 전용
├── output/                 # 최종 결과물 (.docx, .md)
├── tmp/                    # 에이전트 간 중간 파일
│   ├── extracted_data.txt  # xlsx 추출 결과
│   ├── style_guide.md      # 문체 가이드
│   ├── theory_notes.md     # 이론 정리
│   └── draft_answers.md    # 초안
├── scripts/
│   └── extract_xlsx.py     # xlsx → 텍스트 추출 스크립트
└── docs/
    ├── requirements.md
    ├── design.md
    └── tasks.md
```

---

## 사용법

### 1. 입력 파일 준비

| 파일 유형 | 폴더 | 비고 |
|-----------|------|------|
| 실험 매뉴얼 (PDF / Word) | `input/manual/` | |
| 강의안 (PDF) | `input/lecture/` | pptx → PDF 변환 필요 |
| 레포트 양식 (PDF / Word) | `input/form/` | |
| 실험 결과 데이터 (xlsx / 이미지) | `input/data/` | |
| 족보 (PDF / Word / 이미지) | `input/jokbo/` | 선택 사항 |

> pptx 강의안은 PowerPoint 또는 LibreOffice로 PDF 변환 후 넣어주세요.

### 2. Claude Code에서 실행

Claude Code CLI를 열고 아래처럼 입력하면 됩니다:

```
열전달 실험 1 post-lab 레포트 작성해줘.
입력 파일은 input/ 폴더에 넣어뒀어.
```

"레포트 작성", "pre-lab", "post-lab" 키워드가 감지되면 **Orchestrator** 에이전트가 자동으로 전체 파이프라인을 실행합니다.

### 3. 결과 확인

- `output/` 폴더에 Word(.docx) 또는 Markdown 파일로 저장됩니다.
- 수식은 Word 수식 편집기에 바로 붙여넣기 가능한 LaTeX 형식입니다.
- 사진 삽입 추천 목록과 참고문헌이 함께 생성됩니다.

---

## 핵심 제약사항

- **족보는 문체 분석 전용** — Style Analyzer만 접근하며, 수치·결론·분석 내용은 절대 참조하지 않습니다.
- **수식 형식** — Word 수식 편집기 호환 LaTeX (`$$Q = \dot{m} c_p \Delta T$$`)
- **응답 언어** — 한국어 전용
- **AI 탐지 회피** — GPTZero, Turnitin 기준 통과를 목표로 Humanizer가 문체를 조정합니다.
- **표절률** — 20% 미만 유지 목표

---

## 기술 스택

- **에이전트 프레임워크**: Claude Agent SDK (`.claude/agents/` 마크다운 정의)
- **실행 환경**: Claude Code CLI (로컬, 외부 서버 없음)
- **보조 스크립트**: Python 3.11+ / openpyxl (xlsx 파싱), python-docx (Word 출력)
- **파일 파싱**: Claude 기본 파일 읽기 기능 (PDF, Word, 이미지 지원)

---

## 워크플로우 상세

Reviewer가 품질 미달로 판단할 경우, Report Writer → Humanizer 재작업이 자동으로 실행됩니다 (최대 2회).  
2회 후에도 미흡하면 Reviewer 코멘트를 결과물에 포함하여 수동 수정을 안내합니다.

```
Report Writer → Humanizer → Reviewer
                               ↓ 미흡
               Report Writer → Humanizer (최대 2회 반복)
                               ↓ 최종 승인
               Image Recommender + Reference Manager → output/
```
