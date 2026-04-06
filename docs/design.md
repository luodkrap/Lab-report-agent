# 기계공학실험 레포트 에이전트 설계 문서

## 기술 스택

- 에이전트 프레임워크: Claude Agent SDK (`.claude/agents/` 마크다운 정의 방식)
- 실행 환경: Claude Code CLI (로컬, 외부 서버 없음)
- 언어: Python 3.11+ (보조 스크립트용)
- 파일 처리:
  - PDF 파싱: Claude 기본 파일 읽기 기능 (Read 도구)
  - Word(.docx) 파싱: Claude 기본 파일 읽기 기능 (Read 도구)
  - xlsx 추출: openpyxl (Python 스크립트, Bash 도구로 실행)
  - 결과물 생성: python-docx (Word 출력), 또는 Markdown 직접 출력
- 기타: 별도 데이터베이스 없음, 파일 시스템 기반

## 폴더 구조

```
report_agent/
├── .claude/
│   └── agents/
│       ├── orchestrator.md         # Orchestrator 에이전트 정의
│       ├── input-analyzer.md       # Input Analyzer 에이전트 정의
│       ├── style-analyzer.md       # Style Analyzer 에이전트 정의
│       ├── theory-researcher.md    # Theory Researcher 에이전트 정의
│       ├── report-writer.md        # Report Writer 에이전트 정의
│       ├── humanizer.md            # Humanizer 에이전트 정의
│       ├── reviewer.md             # Reviewer 에이전트 정의
│       ├── image-recommender.md    # Image Recommender 에이전트 정의
│       ├── reference-manager.md    # Reference Manager 에이전트 정의
│       └── sdd-spec.md             # (기존) SDD 스펙 에이전트
├── docs/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
├── scripts/
│   └── extract_xlsx.py             # xlsx → 텍스트 추출 스크립트
├── input/                          # 사용자가 입력 파일을 넣는 폴더
│   ├── manual/                     # 실험 매뉴얼 (PDF, Word)
│   ├── lecture/                    # 강의안 (PDF로 변환된 pptx)
│   ├── form/                       # 레포트 양식 (PDF, Word)
│   ├── data/                       # 실험 결과 데이터 (xlsx, CSV, 이미지)
│   └── jokbo/                      # 족보 (PDF, Word, 이미지)
├── output/                         # 생성된 레포트 저장 폴더
│   ├── [실험명]_prelab.docx
│   ├── [실험명]_postlab.docx
│   └── [실험명]_references.md
└── tmp/                            # 중간 처리 결과 임시 저장
    ├── extracted_data.txt          # xlsx 추출 결과
    ├── style_guide.md              # Style Analyzer 결과
    ├── theory_notes.md             # Theory Researcher 결과
    └── draft_answers.md            # Report Writer 초안
```

## 에이전트 워크플로우

### 전체 실행 순서

```
[사용자 입력]
    ↓
Orchestrator
    ├─(xlsx 있을 경우)→ extract_xlsx.py 실행 (Bash) → tmp/extracted_data.txt
    ├─→ Input Analyzer → 파일 파싱, 문항 목록 추출
    ├─→ Style Analyzer → 족보 문체 분석 → tmp/style_guide.md
    ├─→ Theory Researcher → 이론 정리 → tmp/theory_notes.md
    ├─→ Report Writer → 문항별 초안 → tmp/draft_answers.md
    ├─→ Humanizer → 문체 변환 (style_guide.md 적용)
    ├─→ Reviewer → 품질 검토 및 피드백 (필요 시 Writer/Humanizer 재호출)
    ├─→ Image Recommender → 사진 추천 목록 생성
    ├─→ Reference Manager → 참고문헌 목록 생성
    └─→ 최종 결과물 저장 (output/)
```

### 반복(루프) 처리

- Reviewer가 피드백을 반환하면 Orchestrator는 해당 문항을 Report Writer → Humanizer 순으로 재처리한다.
- 최대 재시도 횟수: 2회 (무한 루프 방지)
- 2회 재시도 후에도 미흡하면 Reviewer 코멘트를 결과물에 포함하고 사용자에게 수동 수정을 안내한다.

## 에이전트별 입출력 명세

### Orchestrator
| 항목 | 내용 |
|------|------|
| 입력 | 사용자 명령, input/ 폴더의 파일 목록, 레포트 종류(pre/post), 실험명 |
| 출력 | output/ 폴더의 최종 결과 파일 |
| 도구 | Read, Write, Bash, 하위 에이전트 호출 |

### Input Analyzer
| 항목 | 내용 |
|------|------|
| 입력 | input/ 폴더 내 파일들 (PDF, Word, 이미지, tmp/extracted_data.txt) |
| 출력 | 구조화된 파싱 결과 (실험 목적, 원리, 문항 목록, 결과값, 족보 원문) |
| 도구 | Read, Glob |

### Style Analyzer
| 항목 | 내용 |
|------|------|
| 입력 | 족보 원문 텍스트 |
| 출력 | tmp/style_guide.md (문장 길이, 어미 패턴, 용어 사용 방식 등) |
| 도구 | Read, Write |

### Theory Researcher
| 항목 | 내용 |
|------|------|
| 입력 | 실험 주제, 강의안 파싱 결과 |
| 출력 | tmp/theory_notes.md (이론 정리, LaTeX 수식 포함) |
| 도구 | Read, Write |

### Report Writer
| 항목 | 내용 |
|------|------|
| 입력 | 문항 목록, 실험 결과값, theory_notes.md |
| 출력 | tmp/draft_answers.md (문항별 초안, LaTeX 수식 포함) |
| 도구 | Read, Write |

### Humanizer
| 항목 | 내용 |
|------|------|
| 입력 | tmp/draft_answers.md, tmp/style_guide.md |
| 출력 | 문체 변환된 답변 텍스트 |
| 도구 | Read, Write |

### Reviewer
| 항목 | 내용 |
|------|------|
| 입력 | 문체 변환된 답변, 문항 목록, 실험 결과값, 족보 원문 |
| 출력 | 승인 또는 피드백 (재작업 대상 문항 + 구체적 수정 사항) |
| 도구 | Read, Write |

### Image Recommender
| 항목 | 내용 |
|------|------|
| 입력 | 최종 답변 텍스트, 강의안 파싱 결과, 실험 매뉴얼 파싱 결과 |
| 출력 | 문항별 사진/그림 추천 목록 (삽입 위치, 설명, 출처/URL) |
| 도구 | Read, Write |

### Reference Manager
| 항목 | 내용 |
|------|------|
| 입력 | 사용된 입력 파일 목록, 이론 정리 내용 |
| 출력 | 참고문헌 목록 (한국기계학회 인용 형식) |
| 도구 | Read, Write |

## xlsx 추출 스크립트 명세

- 파일 경로: `scripts/extract_xlsx.py`
- 실행 방식: `python scripts/extract_xlsx.py input/data/[파일명].xlsx`
- 동작:
  - openpyxl로 xlsx 파일을 열어 모든 시트를 순회한다
  - 각 시트의 셀 값을 탭 구분 텍스트로 변환한다
  - 시트명과 함께 `tmp/extracted_data.txt`에 저장한다
- 출력 형식 예시:
  ```
  [시트명: 열전달 실험 결과]
  측정 번호  온도(℃)  열유속(W/m²)  대류계수(W/m²K)
  1          25.3     412.5         18.7
  2          26.1     430.2         19.1
  ```

## 에이전트 마크다운 파일 구조 (공통 템플릿)

`.claude/agents/[에이전트명].md` 파일은 다음 구조를 따른다:

```
---
name: [에이전트명]
description: [언제 이 에이전트를 호출하는지 설명]
tools: [사용할 도구 목록]
---

# [에이전트명]

## 역할
[이 에이전트의 책임과 목적]

## 입력
[받아야 하는 정보와 파일]

## 처리 방식
[단계별 처리 로직]

## 출력
[생성할 결과물의 형식과 저장 위치]

## 주의사항
[반드시 지켜야 할 제약 조건]
```

## 출력 파일 형식

### Word(.docx) 출력 구조
```
[실험명] [pre/post-lab] 레포트
─────────────────────────────
문항 1. [문항 내용]
[답변]

[수식 블록]
$$[LaTeX 수식]$$

문항 2. [문항 내용]
[답변]
...
─────────────────────────────
[사진/그림 삽입 추천]
위치: 문항 2 두 번째 단락 후
추천: 열전달 계수 비교 그래프 (강의안 5페이지 Fig. 3)

[참고문헌]
[1] ...
[2] ...
```

### Markdown 출력 구조
```markdown
# [실험명] [pre/post-lab] 레포트

## 문항 1. [문항 내용]
[답변]

$$[LaTeX 수식]$$

## 문항 2. [문항 내용]
[답변]

---

## 사진/그림 삽입 추천
| 위치 | 추천 이미지 | 출처 |
|------|-------------|------|
| 문항 2 두 번째 단락 후 | 열전달 계수 비교 그래프 | 강의안 5페이지 Fig. 3 |

## 참고문헌
[1] ...
[2] ...
```
