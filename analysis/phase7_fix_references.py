"""
Fix references to strict Vancouver style:
  (1) re-index in-text [n] citations by FIRST APPEARANCE (first cited -> [1], etc.; re-cites keep their integer);
  (2) reorder the bibliography 1:1 with the new in-text order;
  (3) enrich DOIs via the Crossref REST API (https://doi.org/...; placeholder if no confident match).
Body text is taken from manuscript_draft_v3.md; the 25-entry bibliography from manuscript_draft_v1.md.
Writes manuscript_draft_v4.md (+ a citation_remap.csv audit).
"""
import re, json, time, urllib.parse, urllib.request
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
M = ROOT/"manuscript"
v3 = (M/"manuscript_draft_v3.md").read_text(encoding="utf-8")
v1 = (M/"manuscript_draft_v1.md").read_text(encoding="utf-8")

# --- split body / references ---
body, _, _tail = v3.partition("## References")
# bibliography entries from v1
refblock = v1.split("## References",1)[1]
entries = {}
for line in refblock.splitlines():
    m = re.match(r"^(\d+)\.\s+(.*)$", line.strip())
    if m: entries[int(m.group(1))] = m.group(2).strip()
assert entries, "no bibliography parsed"

# --- find in-text citations in order; build old->new by first appearance ---
cite_rx = re.compile(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\]")
def expand(group):  # "6,16,17" or "21,22" or "1-3" -> list[int]
    out=[]
    for part in re.split(r"\s*,\s*", group):
        rng = re.split(r"\s*[–-]\s*", part)
        if len(rng)==2: out += list(range(int(rng[0]), int(rng[1])+1))
        else: out.append(int(part))
    return out

order=[]
for mt in cite_rx.finditer(body):
    for n in expand(mt.group(1)):
        if n not in order: order.append(n)
# any cited-but-unlisted or listed-but-uncited?
missing_in_body=[n for n in entries if n not in order]
old2new = {old:i+1 for i,old in enumerate(order)}
for n in missing_in_body:  # keep appended at end (shouldn't happen ideally)
    old2new[n]=len(old2new)+1

def collapse(nums):  # ascending, collapse 3+ consecutive into a-b (Vancouver)
    nums=sorted(set(nums)); out=[]; i=0
    while i<len(nums):
        j=i
        while j+1<len(nums) and nums[j+1]==nums[j]+1: j+=1
        if j-i>=2: out.append(f"{nums[i]}–{nums[j]}")
        else: out += [str(x) for x in nums[i:j+1]]
        i=j+1
    return "["+", ".join(out)+"]"

def remap(mt):
    return collapse([old2new[n] for n in expand(mt.group(1))])
new_body = cite_rx.sub(remap, body)

# --- Crossref DOI enrichment ---
def crossref_doi(entry_text):
    q = re.sub(r"https?://\S+","",entry_text)            # drop existing URL
    q = re.sub(r"^\*+|\*+","",q)                          # strip md emphasis
    try:
        url="https://api.crossref.org/works?rows=1&query.bibliographic="+urllib.parse.quote(q[:300])
        req=urllib.request.Request(url, headers={"User-Agent":"aipoch-ref-fixer/1.0 (mailto:valentineghanem@gmail.com)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            it=json.load(r)["message"]["items"]
        if not it: return None,None
        cand=it[0]; doi=cand.get("DOI"); title=(cand.get("title") or [""])[0]
        # confidence: share >=2 distinctive title words
        ew=set(re.findall(r"[a-z]{5,}", entry_text.lower())); tw=set(re.findall(r"[a-z]{5,}", title.lower()))
        ok = len(ew & tw) >= 3
        return (doi if ok else None), title
    except Exception as e:
        return None, "ERR:"+type(e).__name__

new_entries={}; audit=[]
for old in order + missing_in_body:
    new=old2new[old]; txt=entries.get(old,"(MISSING ENTRY)")
    base=re.sub(r"\s*https?://\S+\s*$","",txt).rstrip()
    doi,ctitle=crossref_doi(base)
    doitag = f" https://doi.org/{doi}" if doi else " [DOI: to be confirmed via Crossref]"
    new_entries[new]= base + ("." if not base.endswith(".") else "") + doitag
    audit.append({"new":new,"old":old,"doi":doi or "","crossref_title":(ctitle or "")[:80]})
    time.sleep(0.3)

# --- write v4 ---
newref="\n".join(f"{i}. {new_entries[i]}" for i in sorted(new_entries))
out = new_body.rstrip() + "\n\n## References (Vancouver; re-indexed by first in-text appearance; DOIs via Crossref)\n" + newref + "\n\n*Data sources: Ghana DHS 2022 (DHS Program); Ghana 2021 Census (GSS); WHO GHO.*\n"
(M/"manuscript_draft_v4.md").write_text(out, encoding="utf-8")
with open(M/"citation_remap.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f, fieldnames=["new","old","doi","crossref_title"]); w.writeheader(); w.writerows(audit)
print(f"[refs] {len(order)} citations re-indexed; bibliography {len(new_entries)} entries; v4 written")
print("first-appearance order (old->new):", {o:old2new[o] for o in order[:8]}, "...")
print("DOIs found:", sum(1 for a in audit if a['doi']), "/", len(audit), "| placeholders:", sum(1 for a in audit if not a['doi']))
