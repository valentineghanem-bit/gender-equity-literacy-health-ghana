"""
Stage 10/11 — render manuscript_draft_v2.md to a Q1-formatted .docx WITH EMBEDDED FIGURES.
Times New Roman 12pt, 1.5 spacing, justified body, styled headings, page numbers.
Figures embedded at the 'Figure legends' section; full reference list pulled from v1.
Local only (manuscript/ git-excluded, Tenet 20). No pandoc/LaTeX dependency.
"""
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parents[1]
M = ROOT/"manuscript"; F = ROOT/"outputs"/"figures"
SRC = M/"manuscript_draft_v2.md"; V1 = M/"manuscript_draft_v1.md"
OUT = M/"Gender_Equity_Literacy_Health_Ghana_v2.docx"

FIGMAP = {
 "1": ["fig_choropleth_illiteracy_261.png", "fig_choropleth_poverty_261.png"],
 "2": ["fig_lisa_illiteracy_261.png", "fig_lisa_poverty_261.png"],
 "3": ["shap_summary_district.png"],
 "4": ["fig04_multivariate_disparity.png"],
 "5": ["fig_mediation_forest.png"],
}

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
st.paragraph_format.line_spacing = 1.5; st.paragraph_format.space_after = Pt(6)

def runs(p, text):
    for i, seg in enumerate(re.split(r"\*\*", text)):
        if seg == "": continue
        r = p.add_run(seg); r.bold = (i % 2 == 1)

def heading(text, size, before=10):
    p = doc.add_paragraph(); r = p.add_run(re.sub(r"\*\*", "", text)); r.bold = True; r.font.size = Pt(size)
    p.paragraph_format.space_before = Pt(before); return p

def embed_figure(num, caption):
    for png in FIGMAP.get(num, []):
        fp = F/png
        if fp.exists():
            doc.add_picture(str(fp), width=Inches(6.2))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(caption); r.italic = True; r.font.size = Pt(10)

lines = SRC.read_text(encoding="utf-8").splitlines()
in_legends = False
for ln in lines:
    s = ln.rstrip()
    if not s.strip() or s.strip() == "---": continue
    if s.startswith("**Draft v2"): continue
    if s.startswith("## References"): break          # refs appended from v1 below
    if s.startswith("## Figure legends"):
        in_legends = True; heading("Figures", 13); continue
    if in_legends and s.startswith("- **Figure"):
        m = re.match(r"- \*\*Figure (\d+)\.\*\*\s*(.*)", s)
        if m: embed_figure(m.group(1), "Figure %s. %s" % (m.group(1), re.sub(r"\*\*","",m.group(2)))); continue
    if in_legends and s.startswith("- **Table"):
        p = doc.add_paragraph(); runs(p, s[2:]); continue
    if s.startswith("# "):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(s[2:]); r.bold = True; r.font.size = Pt(15)
    elif s.startswith("## "): heading(s[3:], 13)
    elif s.startswith("### "): heading(s[4:], 12, before=4)
    elif s.startswith("- "):
        p = doc.add_paragraph(style="List Bullet"); runs(p, s[2:])
    elif s.startswith("*(") :  # editorial note line -> small italic
        p = doc.add_paragraph(); r = p.add_run(re.sub(r"[*()]","",s)); r.italic=True; r.font.size=Pt(9)
    else:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; runs(p, s)

# ---- append references from v1 ----
heading("References", 13)
v1 = V1.read_text(encoding="utf-8").splitlines()
grab = False
for ln in v1:
    s = ln.rstrip()
    if s.startswith("## References"): grab = True; continue
    if grab:
        if s.startswith("## ") or s.startswith("*Data sources:*"):
            if s.startswith("*Data sources:*"):
                p = doc.add_paragraph(); r=p.add_run(re.sub(r"[*]","",s)); r.italic=True; r.font.size=Pt(10)
            break
        if re.match(r"^\d+\.\s", s):
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Pt(18)
            p.paragraph_format.first_line_indent = Pt(-18); p.add_run(s).font.size = Pt(11)

# page numbers
f = doc.sections[0].footer.paragraphs[0]; f.alignment = WD_ALIGN_PARAGRAPH.CENTER
fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE"); f._p.append(fld)
doc.save(str(OUT))
import os
print(f"[docx] {OUT.name}  ({round(os.path.getsize(OUT)/1024)} KB)")
imgs = sum(1 for _ in doc.inline_shapes)
print(f"[docx] embedded inline images: {imgs}")
