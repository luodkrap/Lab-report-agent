"""docx 내 모든 표에 회색 테두리·중앙정렬·고정 너비를 적용한다.

사용법:
    python3 scripts/style_docx_tables.py <input.docx> [output.docx]

output 경로를 생략하면 input을 in-place 갱신한다.
"""

import re
import shutil
import sys
import zipfile
from pathlib import Path

TBL_PR_REPLACEMENT = (
    '<w:tblPr>'
    '<w:tblStyle w:val="Table"/>'
    '<w:tblW w:type="dxa" w:w="9026"/>'
    '<w:jc w:val="center"/>'
    '<w:tblLayout w:type="fixed"/>'
    '<w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0"'
    ' w:lastColumn="0" w:noHBand="0" w:noVBand="0" w:val="0020"/>'
    '<w:tblInd w:type="dxa" w:w="0"/>'
    '<w:tblBorders>'
    '<w:top w:val="single" w:sz="6" w:space="0" w:color="808080"/>'
    '<w:left w:val="single" w:sz="6" w:space="0" w:color="808080"/>'
    '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="808080"/>'
    '<w:right w:val="single" w:sz="6" w:space="0" w:color="808080"/>'
    '<w:insideH w:val="single" w:sz="6" w:space="0" w:color="808080"/>'
    '<w:insideV w:val="single" w:sz="6" w:space="0" w:color="808080"/>'
    '</w:tblBorders>'
    '</w:tblPr>'
)

TBL_PR_PATTERN = re.compile(r'<w:tblPr>.*?</w:tblPr>', re.DOTALL)


def style_tables(xml: str) -> str:
    return TBL_PR_PATTERN.sub(TBL_PR_REPLACEMENT, xml)


def process(src: Path, dst: Path) -> int:
    tmp = dst.with_suffix(dst.suffix + '.tmp')
    n = 0
    with zipfile.ZipFile(src, 'r') as zin, zipfile.ZipFile(
        tmp, 'w', zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                text = data.decode('utf-8')
                new_text, n = TBL_PR_PATTERN.subn(TBL_PR_REPLACEMENT, text)
                data = new_text.encode('utf-8')
            zout.writestr(item, data)
    shutil.move(tmp, dst)
    return n


def main(argv: list[str]) -> int:
    if not 2 <= len(argv) <= 3:
        print(__doc__)
        return 2
    src = Path(argv[1])
    dst = Path(argv[2]) if len(argv) == 3 else src
    if not src.exists():
        print(f'입력 파일이 없습니다: {src}')
        return 1
    if dst == src:
        backup = src.with_suffix('.bak.docx')
        shutil.copy(src, backup)
        print(f'원본 백업: {backup}')
    n = process(src, dst)
    print(f'표 {n}개 스타일 적용 완료 → {dst}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
