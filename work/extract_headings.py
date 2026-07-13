from pathlib import Path
import re
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1]
pdf=root/'outputs'/'华理814DSP讲义_完整重排版.pdf'
r=PdfReader(str(pdf))
for i,p in enumerate(r.pages,1):
    txt=p.extract_text() or ''
    lines=[ln.strip() for ln in txt.splitlines() if ln.strip()]
    hits=[]
    for ln in lines:
        if re.match(r'^(第[一二三四五六七八九十]+章|\d+(?:\.\d+){0,2}\s|\d+\s)', ln) or '快速傅里叶' in ln or '多采样率' in ln:
            hits.append(ln)
    print('PAGE',i)
    for h in hits[:8]:
        print(' ',h)
