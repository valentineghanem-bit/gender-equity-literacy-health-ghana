"""
Render manuscript_draft_v4.md -> Q1 .docx: DOUBLE-SPACED (review format), embedded Tables 1-2
(real Word tables) and Figures 1-6 (Arial PNGs), re-indexed Vancouver references with DOIs.
1-inch margins. Local only (Tenet 20).
"""
import re
from pathlib import Path
import pandas as pd
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parents[1]
M = ROOT/"manuscript"; F = ROOT/"outputs"/"figures"; T = ROOT/"outputs"/"tables"
SRC = M/"manuscript_draft_v4.md"; OUT = M/"Gender_Equity_Literacy_Health_Ghana_v4.docx"

FIGMAP = {"1":["fig01_choropleths.png"], "2":["fig02_lisa.png"], "3":["fig03_shap.png"],
          "4":["fig04_parallel_coordinates.png"], "5":["fig05_dumbbell.png"], "6":["fig06_mediation_forest.png"]}
TABMAP = {"1":"manuscript_table1.csv", "2":"manuscript_table2.csv"}

doc = Document()
for s in doc.sections:
    s.top_margin=s.bottom_margin=s.left_margin=s.right_margin=Inches(1)
st = doc.styles["Normal"]; st.font.name="Times New Roman"; st.font.size=Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"),"Times New Roman")
st.paragraph_format.line_spacing=2.0; st.paragraph_format.space_after=Pt(0)   # double-spaced for review

def runs(p,text):
    for i,seg in enumerate(re.split(r"\*\*",text)):
        if seg: r=p.add_run(seg); r.bold=(i%2==1)
def heading(text,size,before=12):
    p=doc.add_paragraph(); r=p.add_run(re.sub(r"\*\*","",text)); r.bold=True; r.font.size=Pt(size)
    p.paragraph_format.space_before=Pt(before)
def caption(text):
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.line_spacing=1.0
    m=re.match(r"(Table \d+\.|Figure \d+\.)\s*(.*)",text)
    if m: r=p.add_run(m.group(1)+" "); r.bold=True; r.font.size=Pt(10); r2=p.add_run(m.group(2)); r2.italic=True; r2.font.size=Pt(10)
    else: r=p.add_run(text); r.italic=True; r.font.size=Pt(10)
def add_table(csv):
    df=pd.read_csv(T/csv).fillna(""); tb=doc.add_table(rows=1,cols=len(df.columns)); tb.style="Table Grid"
    for j,c in enumerate(df.columns):
        rr=tb.rows[0].cells[j].paragraphs[0].add_run(str(c)); rr.bold=True; rr.font.size=Pt(8.5)
        tb.rows[0].cells[j].paragraphs[0].paragraph_format.line_spacing=1.0
    for _,row in df.iterrows():
        cells=tb.add_row().cells
        for j,v in enumerate(row):
            par=cells[j].paragraphs[0]; par.paragraph_format.line_spacing=1.0; rr=par.add_run(str(v)); rr.font.size=Pt(8.5)
def embed_fig(num):
    for png in FIGMAP.get(num,[]):
        if (F/png).exists(): doc.add_picture(str(F/png),width=Inches(6.3)); doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER

mode=None
for ln in SRC.read_text(encoding="utf-8").splitlines():
    s=ln.rstrip()
    if not s.strip() or s.strip()=="---": continue
    if s.startswith("**Draft v4"): continue
    if s.startswith("## References"): heading("References",13); mode="refs"; continue
    if s.startswith("## Tables"): heading("Tables",13); mode="tab"; continue
    if s.startswith("## Figure legends"): heading("Figures",13); mode="fig"; continue
    if mode=="tab" and s.startswith("- **Table"):
        m=re.match(r"- \*\*Table (\d+)\.\*\*\s*(.*)",s)
        if m: caption("Table %s. %s"%(m.group(1),re.sub(r"\*\*","",m.group(2)))); add_table(TABMAP[m.group(1)]); doc.add_paragraph(); continue
    if mode=="fig" and s.startswith("- **Figure"):
        m=re.match(r"- \*\*Figure (\d+)\.\*\*\s*(.*)",s)
        if m: embed_fig(m.group(1)); caption("Figure %s. %s"%(m.group(1),re.sub(r"\*\*","",m.group(2)))); continue
    if mode=="refs" and re.match(r"^\d+\.\s",s):
        p=doc.add_paragraph(); p.paragraph_format.left_indent=Pt(18); p.paragraph_format.first_line_indent=Pt(-18); p.add_run(s).font.size=Pt(11); continue
    if mode=="refs" and s.startswith("*Data sources"):
        p=doc.add_paragraph(); r=p.add_run(re.sub(r"[*]","",s)); r.italic=True; r.font.size=Pt(10); continue
    if s.startswith("# "):
        p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; r=p.add_run(s[2:]); r.bold=True; r.font.size=Pt(15)
    elif s.startswith("## "): heading(s[3:],13)
    elif s.startswith("### "): heading(s[4:],12,4)
    elif s.startswith("- "): p=doc.add_paragraph(style="List Bullet"); runs(p,s[2:])
    else: p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY; runs(p,s)

f=doc.sections[0].footer.paragraphs[0]; f.alignment=WD_ALIGN_PARAGRAPH.CENTER
fld=OxmlElement("w:fldSimple"); fld.set(qn("w:instr"),"PAGE"); f._p.append(fld)
doc.save(str(OUT))
import os
print(f"[docx] {OUT.name} ({round(os.path.getsize(OUT)/1024)} KB) | images={len(doc.inline_shapes)} | tables={len(doc.tables)} | double-spaced")
