"""
Phase 6 — render manuscript_draft_v1.md to a Q1-formatted .docx (python-docx).
Times New Roman 12pt, 1.5 line spacing, justified body, styled headings, page numbers.
Local only (manuscript/ is git-excluded, Tenet 20). No pandoc dependency.
"""
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/"manuscript"/"manuscript_draft_v1.md"
OUT = ROOT/"manuscript"/"Gender_Equity_Literacy_Health_Ghana_v1.docx"
lines = SRC.read_text(encoding="utf-8").splitlines()

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
pf = st.paragraph_format; pf.line_spacing = 1.5; pf.space_after = Pt(6)

def add_runs(p, text):
    # inline **bold**
    for i, seg in enumerate(re.split(r"\*\*", text)):
        if seg == "": continue
        r = p.add_run(seg); r.bold = (i % 2 == 1)

def page_numbers(doc):
    f = doc.sections[0].footer.paragraphs[0]; f.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE"); f._p.append(fld)

skip_prefixes = ("**Draft v1",)
for ln in lines:
    s = ln.rstrip()
    if not s.strip() or s.strip() == "---":
        continue
    if any(s.startswith(p) for p in skip_prefixes):
        continue
    if s.startswith("# "):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(s[2:]); r.bold = True; r.font.size = Pt(15)
    elif s.startswith("## "):
        p = doc.add_paragraph(); r = p.add_run(re.sub(r"\*\*","",s[3:])); r.bold = True; r.font.size = Pt(13)
        p.paragraph_format.space_before = Pt(10)
    elif s.startswith("### "):
        p = doc.add_paragraph(); r = p.add_run(re.sub(r"\*\*","",s[4:])); r.bold = True; r.font.size = Pt(12)
    elif s.startswith("- "):
        p = doc.add_paragraph(style="List Bullet"); add_runs(p, s[2:])
    elif re.match(r"^\d+\.\s", s):
        p = doc.add_paragraph(); p.paragraph_format.left_indent = Pt(18); p.paragraph_format.first_line_indent = Pt(-18)
        add_runs(p, s)
    else:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; add_runs(p, s)

page_numbers(doc)
doc.save(str(OUT))
print(f"[docx] {OUT.name}  ({round(OUT.stat().st_size/1024)} KB)")
