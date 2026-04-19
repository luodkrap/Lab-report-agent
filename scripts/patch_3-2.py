"""
3-2 문항 수정 패치 스크립트
- 기존 docx: output/동역학_module#1_postlab_5조_수정본.docx (이미 원본에서 복제됨)
- 3-2 섹션의 수치·서술·Fig. 12를 in-place로 수정
- 다른 섹션(1-1 ~ 3-1, 3-3, 참고문헌 등)은 건드리지 않음
"""

import zipfile
import shutil
import os
import re

REPORT_AGENT = "/Users/doulz/Desktop/대학교/5-1/기계공학실험(2)/report_agent"
DOCX_PATH = f"{REPORT_AGENT}/output/동역학_module#1_postlab_5조_수정본.docx"
NEW_PNG = f"{REPORT_AGENT}/tmp/figures/dyn_m1_trajectory_compare_v6.png"

# 1. docx 언패키지
tmp_dir = "/tmp/docx_patch"
if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)
os.makedirs(tmp_dir)

with zipfile.ZipFile(DOCX_PATH, 'r') as z:
    z.extractall(tmp_dir)

doc_xml_path = f"{tmp_dir}/word/document.xml"
with open(doc_xml_path, 'r', encoding='utf-8') as f:
    xml = f.read()

# 2. 3-2 섹션 경계 식별 (원 본문에서 확인한 위치)
# 3-2 시작: '3-2. ' w:t 요소의 <w:p> 시작 직전
# 3-2 종료: '...3-3에서 다룬다.' 문장 끝의 </w:p> 다음

# 3-2 섹션 슬라이스: 대략 "3-2. " 앞 w:p 시작 ~ "3-3에서 다룬다." 뒤 w:p 끝
# 안전하게 문자열로 찾기
start_marker = '<w:t xml:space="preserve">3-2. </w:t>'
end_marker_text = '구체적인 수식 분석은 문항 3-3에서 다룬다.'

s_idx = xml.find(start_marker)
assert s_idx != -1, "3-2 시작 마커를 못 찾음"
# 해당 w:t의 w:p 시작 위치
p_start = xml.rfind('<w:p ', 0, s_idx)

e_text_idx = xml.find(end_marker_text)
assert e_text_idx != -1, "3-2 종료 마커를 못 찾음"
p_end = xml.find('</w:p>', e_text_idx) + len('</w:p>')

print(f"3-2 슬라이스: {p_start} ~ {p_end} (길이 {p_end-p_start})")

slice_xml = xml[p_start:p_end]
prefix = xml[:p_start]
suffix = xml[p_end:]

# ============================================================
# 3. 슬라이스 내 수치 치환
# ============================================================

# (a) 단순 수치 치환 (단일 또는 복수 occurrence, 전부 변경)
simple_replacements = [
    # 식 (43)
    ('<m:t>0.083\u2009</m:t>', '<m:t>0.283\u2009</m:t>'),  # l_0 첫 occurrence
    ('<m:t>0.083</m:t>', '<m:t>0.283</m:t>'),                # l_0 두 번째 occurrence
    ('<m:t>2.388</m:t>', '<m:t>1.764</m:t>'),                # sqrt 내부
    ('<m:t>\u20041.545\u2009</m:t>', '<m:t>\u20041.328\u2009</m:t>'),  # v_0
    # Case A
    ('<m:t>0.994</m:t>', '<m:t>0.854</m:t>'),
    ('<m:t>1.183\u2009</m:t>', '<m:t>1.017\u2009</m:t>'),
    ('<m:t>0.316</m:t>', '<m:t>0.234</m:t>'),
    ('<m:t>0.448\u2009</m:t>', '<m:t>0.331\u2009</m:t>'),
    ('<m:t>0.242</m:t>', '<m:t>0.179</m:t>'),
    ('<m:t>\u20090.203</m:t>', '<m:t>\u20090.150</m:t>'),
    ('<m:t>0.288</m:t>', '<m:t>0.213</m:t>'),
    ('<m:t>\u20090.343</m:t>', '<m:t>\u20090.253</m:t>'),
    # Case B
    ('<m:t>1.004</m:t>', '<m:t>0.863</m:t>'),
    ('<m:t>1.174\u2009</m:t>', '<m:t>1.009\u2009</m:t>'),
    ('<m:t>0.323</m:t>', '<m:t>0.239</m:t>'),         # Case B d_1 + Case C 비교문
    ('<m:t>0.442\u2009</m:t>', '<m:t>0.326\u2009</m:t>'),  # Case B d_2 (with thin space)
    ('<m:t>0.442</m:t>', '<m:t>0.326</m:t>'),         # Case C 비교문 (no thin space)
    ('<m:t>\u20090.210</m:t>', '<m:t>\u20090.155</m:t>'),  # Case B r_1 y
    ('<m:t>0.287</m:t>', '<m:t>0.212</m:t>'),         # Case B r_2 x
    ('<m:t>\u20090.336</m:t>', '<m:t>\u20090.248</m:t>'),  # Case B r_2 y
    # Case C 비교비
    ('<m:t>62</m:t>', '<m:t>83</m:t>'),         # 62% → 83%
    ('<m:t>56</m:t>', '<m:t>75</m:t>'),         # 56% → 75%
    # e 관련
    ('<m:t>0.59</m:t>', '<m:t>0.79</m:t>'),     # 거리비 2회
    ('<m:t>0.77</m:t>', '<m:t>0.89</m:t>'),     # e 값
    # Case B 보정 r_2 y
    ('<m:t>\u20090.197</m:t>', '<m:t>\u20090.196</m:t>'),
]

for old, new in simple_replacements:
    count_before = slice_xml.count(old)
    slice_xml = slice_xml.replace(old, new)
    count_after = slice_xml.count(new) - prefix.count(new) - suffix.count(new)
    print(f"  치환: {old!r} → {new!r} (횟수: {count_before})")

# (b) 0.245 치환 — Case B r_1 x(−0.245)만 변경, Case C |r_2|_실측=0.245\u2009는 유지
# 공백 패턴이 다르므로 정확한 패턴으로만 치환
old_245 = '<m:t>0.245</m:t>'  # Case B r_1^(B) (공백 없음)
new_182 = '<m:t>0.182</m:t>'
assert slice_xml.count(old_245) == 1, f"Case B 0.245 매칭 실패: {slice_xml.count(old_245)}개"
slice_xml = slice_xml.replace(old_245, new_182)
print(f"  치환: Case B r_1^(B) x = -0.245 → -0.182")

# 검증: Case C의 0.245\u2009는 그대로 있어야 함
remaining_casec = slice_xml.count('<m:t>0.245\u2009</m:t>')
print(f"  Case C 0.245 유지: {remaining_casec}개")
assert remaining_casec == 1, f"Case C 0.245 누락: {remaining_casec}개"

# ============================================================
# 4. 서술 문장 치환
# ============================================================

# (i) 식 (43) 직후 v'(22) 일치 문장 삽입
old_yeogiseo = '<w:t xml:space="preserve">여기서 </w:t>'
new_yeogiseo = '<w:t xml:space="preserve">이 값은 2-1에서 식 (22)로 구한 충돌 직전 속력 v\' = 1.328 m/s와 일치하며, 서로 다른 두 경로로 산출한 속력이 정합한다. 여기서 </w:t>'
assert slice_xml.count(old_yeogiseo) == 1, f"'여기서' w:t 매칭 실패: {slice_xml.count(old_yeogiseo)}개"
slice_xml = slice_xml.replace(old_yeogiseo, new_yeogiseo)
print("  치환: v'(22) 일치 문장 삽입")

# (ii) Case A 서술 문단 전체 교체
# 원본 문단: "ball 2는 타겟 2 ... 문항 1-4 참고)보다 크기 때문이다." 블록
case_a_start_text = '<w:r w:rsidRPr="009C6A8A"><w:rPr><w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorHAnsi" w:hAnsiTheme="minorHAnsi"/></w:rPr><w:t xml:space="preserve">ball 2는 타겟 2 </w:t></w:r>'
case_a_end_text = '<w:t>, 문항 1-4 참고)보다 크기 때문이다.</w:t></w:r>'

a_start = slice_xml.find(case_a_start_text)
a_end_search = slice_xml.find(case_a_end_text, a_start)
assert a_start != -1 and a_end_search != -1, f"Case A 문단 경계 못찾음: {a_start}, {a_end_search}"
a_end = a_end_search + len(case_a_end_text)

# 새 Case A 본문 XML 구성 (same font style, plain text only — Unicode subscripts)
# 수식 블록은 유지하기 위해 일부 inline OMML 보존, 나머지는 plain text
# 간소화: 전체를 plain w:t로 교체하되 좌표와 숫자만 유지
new_case_a = (
    '<w:r w:rsidRPr="009C6A8A">'
    '<w:rPr><w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorHAnsi" w:hAnsiTheme="minorHAnsi"/></w:rPr>'
    '<w:t xml:space="preserve">ball 2는 타겟 2 (0.268, 0.319) 방향으로 직진하지만, 타겟까지의 거리 0.417 m에 비해 d\u2082 = 0.331 m에 그쳐 약 0.086 m 앞에서 멈춘다. 이는 l_free = 0.283 m 구간의 마찰로 운동에너지가 상당 부분 소모되어, 충돌 직전 속력 v\u2080가 v_release보다 크게 낮아졌기 때문이다.</w:t>'
    '</w:r>'
)
slice_xml = slice_xml[:a_start] + new_case_a + slice_xml[a_end:]
print("  치환: Case A 서술 문단 전체 교체")

# (iii) Case B 마지막 문장 교체
old_case_b_end = '이므로 두 궤적은 거의 겹치며, ball 2가 타겟 2 방향으로 나아가되 역시 타겟보다 멀리 정지한다.'
new_case_b_end = '이므로 두 궤적은 거의 겹치며, ball 2가 타겟 2 방향으로 나아가되 역시 타겟에 도달하지 못하고 앞에서 멈춘다.'
assert slice_xml.count(old_case_b_end) == 1, f"Case B 종결 문장 매칭 실패"
slice_xml = slice_xml.replace(old_case_b_end, new_case_b_end)
print("  치환: Case B 종결 문장")

# (iv) Fig 1 참조 문장 수정
old_fig_ref = ' 궤적의 절반 거리 근처에 놓여 있다. 두 이상 궤적('
new_fig_ref = ' 궤적의 약 80% 지점 부근에 놓여 있다. 두 이상 궤적('
assert slice_xml.count(old_fig_ref) == 1, "Fig 1 참조 문장 매칭 실패"
slice_xml = slice_xml.replace(old_fig_ref, new_fig_ref)
print("  치환: Fig 1 참조 문장")

# ============================================================
# 5. Fig. 1 캡션 alt text v_0 값 수정
# ============================================================
# descr="Fig. 1. 이론 발사대(점선)와 실험 발사대(파선) 조건의 이상 궤적, 그리고 5회 실측 착지점의 비교 (v_0=1.545\\,\\mathrm{m/s})"
old_descr = 'v_0=1.545'
new_descr = 'v_0=1.328'
if old_descr in slice_xml:
    slice_xml = slice_xml.replace(old_descr, new_descr)
    print("  치환: Fig 1 캡션 alt text v_0")

# ============================================================
# 6. 슬라이스를 원본 XML에 재삽입
# ============================================================
new_xml = prefix + slice_xml + suffix

# document.xml 덮어쓰기
with open(doc_xml_path, 'w', encoding='utf-8') as f:
    f.write(new_xml)

# ============================================================
# 7. image21.png (Fig. 12) 교체
# ============================================================
target_png = f"{tmp_dir}/word/media/image21.png"
assert os.path.exists(target_png), "image21.png 없음"
assert os.path.exists(NEW_PNG), f"새 PNG 없음: {NEW_PNG}"
shutil.copy2(NEW_PNG, target_png)
print(f"  교체: image21.png ← {NEW_PNG}")

# ============================================================
# 8. 새 docx로 재패키징
# ============================================================
output_path = DOCX_PATH  # 같은 경로 덮어쓰기
# zip의 구조를 보존하며 재패키지
with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, _, files in os.walk(tmp_dir):
        for file in files:
            abs_path = os.path.join(root, file)
            arcname = os.path.relpath(abs_path, tmp_dir)
            zf.write(abs_path, arcname)

size = os.path.getsize(output_path)
print(f"\n완료: {output_path} ({size:,} bytes)")
