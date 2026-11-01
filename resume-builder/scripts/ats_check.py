#!/usr/bin/env python3
"""Check a resume (.docx or .pdf) for ATS parsing hazards.

Usage:
    python ats_check.py resume.docx [--region us|uk|ie|eu|in|au|ca|gulf|other] [--years N] [--json]

Checks:
  docx: tables, text boxes, images/shapes, multi-column sections, contact info in header/footer,
        non-standard fonts, standard section headings, email/phone in body, bullet consistency.
  pdf:  extractable text, page count, likely multi-column layout, images, headings, contact info.
Page-count expectations depend on --region and --years.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SAFE_FONTS = {"calibri", "arial", "helvetica", "garamond", "georgia", "cambria", "times new roman",
              "lato", "source sans pro", "carlito", "liberation sans", "verdana", "tahoma",
              "book antiqua", "palatino linotype", "aptos", "roboto", "open sans", "computer modern",
              "latin modern", "cmu serif", "lmroman10"}
HEADING_RX = {
    "experience": r"\b(work |professional |relevant )?experience\b|\bemployment( history)?\b|\bwork history\b",
    "education": r"\beducation\b|\bacademic",
    "skills": r"\b(technical |core |key )?skills\b|\bcompetenc",
}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE = re.compile(r"(\+?\d[\d\s().-]{7,}\d)")
PERSONAL = re.compile(r"\b(date of birth|DOB|marital status|married|single|religion|gender|nationality)\b", re.I)


def page_limit(region, years):
    if region in ("us", "ca"):
        return 1 if years < 10 else 2
    if region in ("au",):
        return 3
    return 2 if years >= 2 else 1


def docx_checks(path):
    from docx import Document
    from docx.oxml.ns import qn
    doc = Document(path)
    issues, info = [], {}
    body = doc.element.body
    xml = body.xml
    if body.findall(".//" + qn("w:tbl")):
        issues.append(("high", "Contains tables — ATS may scramble reading order. Use plain paragraphs."))
    if "txbxContent" in xml:
        issues.append(("high", "Contains text boxes — content inside is often skipped by parsers."))
    if "<w:drawing" in xml or "<w:pict" in xml:
        issues.append(("medium", "Contains images/shapes/icons — not parsed; remove unless regionally expected (photo)."))
    for s in doc.sections:
        cols = s._sectPr.find(qn("w:cols"))
        if cols is not None and int(cols.get(qn("w:num"), "1")) > 1:
            issues.append(("high", "Multi-column section layout — use a single column."))
        hf = " ".join(p.text for p in s.header.paragraphs) + " " + " ".join(p.text for p in s.footer.paragraphs)
        if EMAIL.search(hf) or PHONE.search(hf):
            issues.append(("high", "Contact info in header/footer — some ATSs ignore headers; move it into the body."))
    fonts = set()
    used_styles = {p.style.name for p in doc.paragraphs if p.style is not None} | {"Normal"}
    for st in doc.styles:
        try:
            if st.name in used_styles and st.font and st.font.name:
                fonts.add(st.font.name)
        except Exception:
            pass
    for p in doc.paragraphs:
        for r in p.runs:
            if r.font.name:
                fonts.add(r.font.name)
    used = {f for f in fonts if f}
    odd = [f for f in used if f.lower() not in SAFE_FONTS and not f.startswith("+")]
    if odd:
        issues.append(("low", f"Non-standard fonts present: {', '.join(sorted(odd))} (fine if embedded in PDF; risky in .docx)."))
    text = "\n".join(p.text for p in doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            text += "\n" + " ".join(c.text for c in row.cells)
    info["fonts"] = sorted(used)
    return text, issues, info


def pdf_checks(path):
    import pdfplumber
    issues, info = [], {}
    with pdfplumber.open(path) as pdf:
        pages = pdf.pages
        info["pages"] = len(pages)
        text = "\n".join((p.extract_text() or "") for p in pages)
        imgs = sum(len(p.images) for p in pages)
        if imgs:
            issues.append(("medium", f"{imgs} image(s) found — not parsed; fine only for an intended photo."))
        # column heuristic: many lines whose words start in the right half after a big gap
        for p in pages[:2]:
            words = p.extract_words()
            if not words:
                continue
            mid = p.width / 2
            left = sum(1 for w in words if w["x0"] < mid * 0.6)
            right_starts = 0
            lines = {}
            for w in words:
                lines.setdefault(round(w["top"]), []).append(w)
            for ws in lines.values():
                ws.sort(key=lambda w: w["x0"])
                for a, b in zip(ws, ws[1:]):
                    if b["x0"] - a["x1"] > p.width * 0.12 and b["x0"] < p.width * 0.8:
                        right_starts += 1
                        break
            if right_starts > len(lines) * 0.35 and left > 20:
                issues.append(("high", "Layout looks multi-column — parsers may interleave columns."))
                break
    if len(text.strip()) < 200:
        issues.append(("high", "Little or no extractable text — likely image/scanned PDF. ATS cannot read it."))
    return text, issues, info


def pdf_pages_for_docx(path):
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        return None
    with tempfile.TemporaryDirectory() as td:
        subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", td, str(path)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out = Path(td) / (Path(path).stem + ".pdf")
        if out.exists():
            from pypdf import PdfReader
            return len(PdfReader(str(out)).pages)
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--region", default="other")
    ap.add_argument("--years", type=float, default=5)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    path = Path(a.file)
    if path.suffix.lower() == ".docx":
        text, issues, info = docx_checks(path)
        info["pages"] = pdf_pages_for_docx(path)
    elif path.suffix.lower() == ".pdf":
        text, issues, info = pdf_checks(path)
    else:
        sys.exit("Provide a .docx or .pdf")

    for name, rx in HEADING_RX.items():
        if not re.search(rx, text, re.I):
            issues.append(("medium", f"No standard '{name}' heading found."))
    head = text[:600]
    if not EMAIL.search(head):
        issues.append(("high", "No email address near the top of the body text."))
    if not PHONE.search(head):
        issues.append(("medium", "No phone number near the top of the body text."))
    if PERSONAL.search(text) and a.region in ("us", "ca", "uk", "ie", "au"):
        issues.append(("medium", "Personal details (DOB/marital/religion/gender/nationality) found — not customary in this region."))
    if re.search(r"\b(I|me|my)\b", text):
        issues.append(("low", "First-person pronouns found (I/me/my) — remove from bullets."))
    if re.search(r"responsible for", text, re.I):
        issues.append(("low", "'Responsible for' found — rewrite as an achievement with an action verb."))
    weak = re.findall(r"^\W*(helped|assisted|worked on|participated in|was involved in)\b", text, re.I | re.M)
    if weak:
        issues.append(("low", f"Weak bullet openers: {', '.join(sorted(set(w.lower() for w in weak)))} — say what was actually done."))
    fluff = re.findall(r"\b(spearheaded|orchestrated|leveraged|utili[sz]ed|synergi[sz]ed|revolutioni[sz]ed|pioneered|"
                       r"amplified|conceptuali[sz]ed|honed|fostered|elevated|successfully)\b", text, re.I)
    if fluff:
        issues.append(("low", f"Superfluous words: {', '.join(sorted(set(f.lower() for f in fluff)))} — use plain verbs."))
    if re.search(r"https?://|www\.", text):
        issues.append(("low", "URLs include https:// or www. — write them plain (linkedin.com/in/name)."))
    if re.search(r"^\s*(email|e-mail|phone|mobile|github|linkedin|portfolio)\s*:", text, re.I | re.M):
        issues.append(("low", "Contact prefixes like 'Email:' found — drop them."))
    if re.search(r"\b(19|20)\d\d\s+-\s+((19|20)\d\d|present|current|now)", text, re.I):
        issues.append(("low", "Date ranges use a hyphen — use an en dash (Mar 2022 – Present)."))
    if re.search(r"[–-]\s*(current|now|ongoing|today)\b", text, re.I):
        issues.append(("low", "Use 'Present' for current roles, not Current/Now/Ongoing."))
    if re.search(r"\b(spring|summer|fall|autumn|winter) (19|20)\d\d\b", text, re.I):
        issues.append(("low", "Seasons used as dates — use months."))
    spelled = re.findall(r"\b(two|three|four|five|six|seven|eight|nine|ten|twelve|fifteen|twenty)\s+(engineers|services|teams|"
                         r"developers|people|members|projects|clients|countries|regions|products|apps|applications|years|months)\b", text, re.I)
    if spelled:
        issues.append(("low", "Numbers spelled out (e.g. 'eight engineers') — use digits."))
    if re.search(r"references (available )?(up)?on request", text, re.I):
        issues.append(("low", "'References available on request' wastes a line."))

    limit = page_limit(a.region, a.years)
    pages = info.get("pages")
    if pages and pages > limit:
        issues.append(("medium", f"{pages} pages — norm for region '{a.region}' with {a.years:g} yrs is ≤{limit}."))

    bullets = [l for l in text.splitlines() if l.strip()]
    nums = sum(1 for l in bullets if re.search(r"\d", l) and len(l) > 40)
    long_lines = sum(1 for l in bullets if len(l) > 40)
    info["lines_with_numbers_pct"] = round(100 * nums / long_lines) if long_lines else 0
    if long_lines and info["lines_with_numbers_pct"] < 40:
        issues.append(("low", f"Only {info['lines_with_numbers_pct']}% of content lines contain a number — quantify more impact."))
    info["word_count"] = len(re.findall(r"\w+", text))

    order = {"high": 0, "medium": 1, "low": 2}
    issues.sort(key=lambda x: order[x[0]])
    if a.json:
        print(json.dumps({"info": info, "issues": [{"severity": s, "message": m} for s, m in issues]}, indent=2))
        return
    print(f"File: {path.name} | pages: {pages} | words: {info['word_count']} | "
          f"lines with numbers: {info['lines_with_numbers_pct']}%")
    if not issues:
        print("No ATS issues found.")
    for s, m in issues:
        print(f"[{s.upper():6}] {m}")


if __name__ == "__main__":
    main()
