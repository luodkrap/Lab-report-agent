# 기계공학실험 레포트 에이전트 작업 목록

---

## T001: 프로젝트 초기 설정 및 폴더 구조 생성

- 선행 작업: 없음
- 내용:
  - `input/manual/`, `input/lecture/`, `input/form/`, `input/data/`, `input/jokbo/` 폴더 생성
  - `output/`, `tmp/`, `scripts/` 폴더 생성
  - 각 폴더에 `.gitkeep` 또는 용도 설명 `README.txt` 파일 추가
- 완료 기준: 지정된 폴더 구조가 모두 존재하고, `ls` 명령으로 확인 가능하다

---

## T002: xlsx 추출 스크립트 작성

- 선행 작업: T001
- 내용:
  - `scripts/extract_xlsx.py` 파일 생성
  - openpyxl을 사용하여 xlsx 파일의 모든 시트를 순회한다
  - 각 시트의 셀 값을 탭 구분 텍스트로 변환한다
  - 시트명 헤더와 함께 `tmp/extracted_data.txt`에 저장한다
  - 커맨드라인 인자로 xlsx 파일 경로를 받는다: `python scripts/extract_xlsx.py <파일경로>`
- 완료 기준:
  - 샘플 xlsx 파일을 넣고 스크립트를 실행했을 때 `tmp/extracted_data.txt`가 생성된다
  - 시트명이 헤더로 표시되고, 셀 값이 탭 구분 형태로 저장된다
  - 빈 셀, 병합 셀, 한국어 문자가 포함된 경우에도 오류 없이 처리된다

---

## T003: Orchestrator 에이전트 정의

- 선행 작업: T001
- 내용:
  - `.claude/agents/orchestrator.md` 파일 생성
  - 사용자로부터 실험명, 레포트 종류(pre/post), 입력 파일 경로를 받는 방식 정의
  - xlsx 파일 감지 시 T002 스크립트 실행을 먼저 지시하는 로직 기술
  - 에이전트 호출 순서 정의: Input Analyzer → Style Analyzer → Theory Researcher → Report Writer → Humanizer → Reviewer → Image Recommender → Reference Manager
  - Reviewer 피드백 수신 시 최대 2회 재시도 루프 처리 방식 기술
  - 최종 결과물을 `output/` 폴더에 저장하는 방식 기술
  - 사용 도구: Read, Write, Bash
- 완료 기준: 에이전트 파일이 존재하고, Claude Code에서 `@orchestrator` 호출 시 역할 설명이 출력된다

---

## T004: Input Analyzer 에이전트 정의

- 선행 작업: T001
- 내용:
  - `.claude/agents/input-analyzer.md` 파일 생성
  - `input/` 폴더 내 파일 유형별 파싱 방식 정의:
    - PDF/Word: Read 도구로 직접 읽기
    - 이미지: Read 도구로 시각적 분석
    - `tmp/extracted_data.txt`: Read 도구로 읽어 수치 데이터 정리
  - 파싱 결과를 구조화하여 출력하는 형식 정의 (실험 목적, 원리, 문항 목록, 결과값, 족보 원문 분리)
  - 족보 원문은 내용이 아닌 형식(문체)만 전달하도록 주의사항 명시
  - 사용 도구: Read, Glob
- 완료 기준: 에이전트 파일이 존재하고, 샘플 입력 파일을 주었을 때 구조화된 파싱 결과가 출력된다

---

## T005: Style Analyzer 에이전트 정의

- 선행 작업: T001
- 내용:
  - `.claude/agents/style-analyzer.md` 파일 생성
  - 족보 원문으로부터 분석할 항목 명시: 문장 길이 분포, 어미 패턴, 전문 용어 사용 방식, 수식 서술 방식, 단락 구성 방식
  - 분석 결과를 `tmp/style_guide.md`에 저장하는 형식 정의
  - 족보 내용(수치, 결론, 해석) 참조 금지 주의사항 명시
  - 사용 도구: Read, Write
- 완료 기준: 에이전트 파일이 존재하고, 족보 텍스트를 입력하면 `tmp/style_guide.md`에 문체 가이드가 생성된다

---

## T006: Theory Researcher 에이전트 정의

- 선행 작업: T001
- 내용:
  - `.claude/agents/theory-researcher.md` 파일 생성
  - 지원 분야 명시: 열전달, 기계진동, 유체역학, 동역학
  - 강의안(PDF) 파싱 결과를 기반으로 핵심 개념 정리 방식 기술
  - LaTeX 수식 표기 규칙 정의 (Word 수식 편집기 호환 형식)
  - 결과를 `tmp/theory_notes.md`에 저장하는 방식 기술
  - 사용 도구: Read, Write
- 완료 기준: 에이전트 파일이 존재하고, 실험 주제와 강의안을 입력하면 LaTeX 수식이 포함된 이론 정리가 `tmp/theory_notes.md`에 생성된다

---

## T007: Report Writer 에이전트 정의

- 선행 작업: T001
- 내용:
  - `.claude/agents/report-writer.md` 파일 생성
  - pre-lab 작성 지침 정의: 이론 이해, 예상 결과, 실험 방법
  - post-lab 작성 지침 정의: 결과 분석, 오차 원인, 이론 비교, 결론
  - `tmp/theory_notes.md`와 실험 결과값을 참조하는 방식 기술
  - 족보 내용 참조 절대 금지 명시
  - LaTeX 수식 포함 방식 정의
  - 결과를 `tmp/draft_answers.md`에 저장하는 형식 정의 (문항 번호 구분)
  - 사용 도구: Read, Write
- 완료 기준: 에이전트 파일이 존재하고, 문항 목록과 이론 정리를 입력하면 문항별 초안이 `tmp/draft_answers.md`에 생성된다

---

## T008: Humanizer 에이전트 정의

- 선행 작업: T001
- 내용:
  - `.claude/agents/humanizer.md` 파일 생성
  - `tmp/style_guide.md`를 읽어 문체 가이드를 적용하는 방식 정의
  - AI 탐지 회피를 위한 변환 원칙 명시:
    - AI 특유의 대칭적 문장 구조 제거
    - 과도하게 매끄러운 연결어 다양화
    - 문장 길이 불규칙하게 조정
    - 수동태/능동태 혼용
    - 학부생이 실제로 쓰는 표현 패턴 반영
  - GPTZero, Turnitin 기준 통과 목표 명시
  - 표절률 최소화를 위한 원문 재구성 원칙 명시
  - 사용 도구: Read, Write
- 완료 기준: 에이전트 파일이 존재하고, 초안 답변을 입력하면 문체가 변환된 결과가 출력된다

---

## T009: Reviewer 에이전트 정의

- 선행 작업: T001
- 내용:
  - `.claude/agents/reviewer.md` 파일 생성
  - 검토 항목 명시:
    - 수식, 단위, 수치의 사실 정확성
    - 문항 요구사항 충족 여부
    - 논리적 흐름
    - 족보 내용과의 유사도
  - 피드백 형식 정의: 승인(`PASS`) 또는 재작업 요청(`REVISE: [문항 번호] [수정 사항]`)
  - 재시도 불필요 시 최종 승인 후 Orchestrator에 반환하는 방식 기술
  - 사용 도구: Read, Write
- 완료 기준: 에이전트 파일이 존재하고, 답변을 입력하면 PASS 또는 구체적인 REVISE 피드백이 출력된다

---

## T010: Image Recommender 에이전트 정의

- 선행 작업: T001
- 내용:
  - `.claude/agents/image-recommender.md` 파일 생성
  - 강의안 및 매뉴얼 내 그림 추천 시 파일명 + 페이지 명시 방식 정의
  - 외부 이미지 추천 시 검색 키워드, 출처, URL 제공 형식 정의
  - 실제 삽입은 사용자 직접 수행임을 주의사항으로 명시
  - 추천 목록 출력 형식 정의 (Markdown 표 형태)
  - 사용 도구: Read, Write
- 완료 기준: 에이전트 파일이 존재하고, 답변 텍스트를 입력하면 문항별 이미지 추천 목록이 Markdown 표로 출력된다

---

## T011: Reference Manager 에이전트 정의

- 선행 작업: T001
- 내용:
  - `.claude/agents/reference-manager.md` 파일 생성
  - 입력 파일(매뉴얼, 강의안, 교재)을 참고문헌으로 변환하는 형식 정의
  - 한국기계학회 인용 형식 규칙 명시
  - 추가 참고문헌 필요 시 논문, 교재, 웹 자료 제안 방식 기술
  - 참고문헌 번호 자동 부여 방식 기술
  - 사용 도구: Read, Write
- 완료 기준: 에이전트 파일이 존재하고, 입력 파일 목록을 주면 인용 형식에 맞는 참고문헌 목록이 출력된다

---

## T012: 엔드-투-엔드 통합 테스트 (열전달 post-lab)

- 선행 작업: T002, T003, T004, T005, T006, T007, T008, T009, T010, T011
- 내용:
  - 열전달 실험 1건을 대상으로 전체 파이프라인을 실행한다
  - 테스트 입력 파일 구성:
    - `input/manual/` : 열전달 실험 매뉴얼 PDF
    - `input/lecture/` : 강의안 PDF (pptx → PDF 변환 완료본)
    - `input/form/` : 레포트 양식 PDF
    - `input/data/` : 실험 결과 xlsx 파일
    - `input/jokbo/` : 선배 레포트 PDF (있는 경우)
  - Orchestrator에 "열전달 실험 1, post-lab" 명령을 입력한다
  - 전체 에이전트가 순서대로 실행되는지 확인한다
- 완료 기준:
  - `output/` 폴더에 결과 파일(.docx 또는 .md)이 생성된다
  - 모든 문항에 답변이 포함된다
  - LaTeX 수식이 포함된다
  - 이미지 추천 목록이 포함된다
  - 참고문헌 목록이 포함된다
  - xlsx 데이터가 답변에 반영된다

---

## T013: pre-lab 지원 검증

- 선행 작업: T012
- 내용:
  - 동일한 실험에 대해 "pre-lab" 명령을 입력하여 파이프라인을 실행한다
  - pre-lab 특화 내용(이론 이해, 예상 결과, 실험 방법)이 답변에 포함되는지 확인한다
  - post-lab과 구분된 별도 출력 파일이 생성되는지 확인한다
- 완료 기준:
  - `output/[실험명]_prelab.docx` 또는 `.md` 파일이 생성된다
  - 답변 내용이 실험 전 관점(이론, 예상, 방법)으로 작성된다

---

## T014: 나머지 3개 분야 동작 확인

- 선행 작업: T012
- 내용:
  - 기계진동, 유체역학, 동역학 각 1개 실험에 대해 Orchestrator를 실행한다
  - 분야별 특화 이론(Theory Researcher)이 올바르게 적용되는지 확인한다
- 완료 기준:
  - 각 분야별로 결과 파일이 생성된다
  - 분야에 맞는 수식과 이론이 포함된다
  - 오류 없이 파이프라인이 완료된다
