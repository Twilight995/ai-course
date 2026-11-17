---
name: notice-docx
description: 공지, 안내문, 행사·모임 알림처럼 일시·장소·준비물을 알리는 한 장짜리 안내문을 워드(docx) 파일로 만들 때 쓴다. 보고서, 결과 정리, 회의록, 엑셀에는 쓰지 않는다.
---

# 안내문 docx 만들기

## 규칙

- 파일 이름은 `notice_YYYYMMDD.docx` (오늘 날짜). 다른 이름을 쓰지 않는다.
- 맨 위에 제목을 'Title' 스타일로, 가운데 정렬로 넣는다.
- 제목 아래에 2열 'Table Grid' 표를 넣는다. 왼쪽 열은 항목(일시, 장소, 대상, 준비물), 오른쪽 열은 내용이다. 받은 내용에 없는 항목은 행을 만들지 않는다.
- 표 아래에 받은 안내 문장을 그대로 한 문단으로 넣는다. 문장을 늘리지 않는다.
- 맨 아래에 "문의: (받은 연락처)"를 오른쪽 정렬로 넣는다. 연락처를 받지 않았으면 이 줄을 넣지 않는다.
- 본문 글꼴은 맑은 고딕 11pt다. 아래 코드를 그대로 써서 적용한다.

## 코드

python-docx를 쓴다. 아래 코드를 그대로 복사하고 `TITLE`, `ITEMS`, `BODY`, `CONTACT`만 받은 내용으로 바꾼다. 한글 글꼴은 `w:eastAsia`를 따로 지정해야 바뀐다.

```python
import datetime
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

TITLE = "제목"
ITEMS = [("일시", "..."), ("장소", "...")]
BODY = "안내 문장"
CONTACT = "연락처"

doc = Document()
style = doc.styles["Normal"]
style.font.name = "맑은 고딕"
style.font.size = Pt(11)
style.element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕")

doc.add_paragraph(TITLE, style="Title").alignment = WD_ALIGN_PARAGRAPH.CENTER
t = doc.add_table(rows=0, cols=2)
t.style = "Table Grid"
for k, v in ITEMS:
    cells = t.add_row().cells
    cells[0].text = k
    cells[1].text = v
doc.add_paragraph(BODY)
if CONTACT:
    doc.add_paragraph("문의: " + CONTACT).alignment = WD_ALIGN_PARAGRAPH.RIGHT

name = "notice_" + datetime.date.today().strftime("%Y%m%d") + ".docx"
doc.save(name)
print("saved", name)
```
