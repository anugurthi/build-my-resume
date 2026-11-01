#!/usr/bin/env python3
"""Render a resume JSON file into an ATS-safe, single-column .docx (and optional .pdf).

Usage:
    python build_resume.py resume.json --out Firstname_Lastname_Resume [--pdf] [--paper a4|letter]
                                       [--font Calibri] [--size 10.5]

Design choices (all deliberate, for ATS parsing):
  * single column, no tables, no text boxes, no images, no header/footer content
  * contact info in the document body
  * standard section headings, right-aligned dates via a tab stop (parses as plain text)
See assets/resume_example.json for the schema.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Inches, Cm, RGBColor

PAPER = {"a4": (Cm(21.0), Cm(29.7)), "letter": (Inches(8.5), Inches(11))}

DEFAULT_ORDER = ["summary", "skills", "experience", "projects", "education",
                 "certifications", "extra"]
GRAD_ORDER = ["education", "skills", "experience", "projects", "certifications", "extra"]

HEADINGS = {
    "summary": "Summary",
    "skills": "Skills",
    "experience": "Experience",
    "projects": "Projects",
    "education": "Education",
    "certifications": "Certifications",
}


def set_spacing(p, before=0, after=0, line=1.0):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line


def add_bottom_border(p, color="404040"):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    pbdr.append(bottom)
    pPr.append(pbdr)


def run(p, text, bold=False, italic=False, size=None, color=None):
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    if size:
        r.font.size = Pt(size)
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    return r


class Builder:
    def __init__(self, data, paper, font, size, accent):
        self.d = data
        self.size = size
        self.accent = accent
        self.doc = Document()
        sec = self.doc.sections[0]
        sec.page_width, sec.page_height = PAPER[paper]
        m = Inches(data.get("meta", {}).get("margin_in", 0.6))
        sec.left_margin = sec.right_margin = m
        sec.top_margin = sec.bottom_margin = Inches(0.5)
        self.text_width = sec.page_width - sec.left_margin - sec.right_margin

        st = self.doc.styles["Normal"]
        st.font.name = font
        st.font.size = Pt(size)
        rpr = st.element.get_or_add_rPr()
        rfonts = rpr.find(qn("w:rFonts"))
        if rfonts is None:
            rfonts = OxmlElement("w:rFonts")
            rpr.append(rfonts)
        for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rfonts.set(qn(attr), font)
        lb = self.doc.styles["List Bullet"]
        lb.font.name = font
        lb.font.size = Pt(size)

    # ---------- helpers ----------
    def para(self, before=0, after=0, align=None):
        p = self.doc.add_paragraph()
        set_spacing(p, before, after)
        if align:
            p.alignment = align
        return p

    def heading(self, text):
        p = self.para(before=8, after=3)
        run(p, text.upper(), bold=True, size=self.size + 1.5, color=self.accent)
        add_bottom_border(p)

    def line_with_date(self, left_parts, right, before=4, after=0):
        """left_parts: list of (text, bold, italic). right: date string, right-aligned via tab."""
        p = self.para(before=before, after=after)
        p.paragraph_format.tab_stops.add_tab_stop(self.text_width, WD_TAB_ALIGNMENT.RIGHT)
        p.paragraph_format.keep_with_next = True
        for text, b, i in left_parts:
            if text:
                run(p, text, bold=b, italic=i)
        if right:
            run(p, "\t" + right)
        return p

    def bullets(self, items):
        for b in items or []:
            p = self.doc.add_paragraph(style="List Bullet")
            set_spacing(p, 0, 1, 1.0)
            p.paragraph_format.left_indent = Inches(0.22)
            p.paragraph_format.first_line_indent = Inches(-0.16)
            run(p, b)

    @staticmethod
    def dates(obj):
        s, e = obj.get("start", ""), obj.get("end", "")
        if s and e:
            return f"{s} – {e}"
        return s or e

    # ---------- sections ----------
    def header(self):
        d = self.d
        p = self.para(after=1, align=WD_ALIGN_PARAGRAPH.CENTER)
        run(p, d["name"], bold=True, size=self.size + 9)
        if d.get("headline"):
            p = self.para(after=1, align=WD_ALIGN_PARAGRAPH.CENTER)
            run(p, d["headline"], size=self.size + 1)
        c = d.get("contact", {})
        parts = [c.get(k) for k in ("location", "phone", "email", "linkedin", "github", "website")]
        parts = [x for x in parts if x]
        if parts:
            p = self.para(after=1, align=WD_ALIGN_PARAGRAPH.CENTER)
            run(p, "  |  ".join(parts))
        if c.get("work_authorization"):
            p = self.para(after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
            run(p, c["work_authorization"], italic=True)

    def summary(self):
        if not self.d.get("summary"):
            return
        self.heading(self.d.get("headings", {}).get("summary", HEADINGS["summary"]))
        p = self.para(after=2)
        run(p, self.d["summary"])

    def skills(self):
        sk = self.d.get("skills")
        if not sk:
            return
        self.heading(self.d.get("headings", {}).get("skills", HEADINGS["skills"]))
        for g in sk:
            p = self.para(after=1)
            run(p, g["category"] + ": ", bold=True)
            run(p, ", ".join(g["items"]))

    def experience(self):
        ex = self.d.get("experience")
        if not ex:
            return
        self.heading(self.d.get("headings", {}).get("experience", HEADINGS["experience"]))
        for job in ex:
            roles = job.get("roles") or [job]
            if len(roles) == 1:
                r = roles[0]
                self.line_with_date(
                    [(r["title"], True, False), (" | " + job["company"], True, False),
                     ((" | " + job["location"]) if job.get("location") else "", False, False)],
                    self.dates(r))
                if job.get("descriptor"):
                    p = self.para()
                    run(p, job["descriptor"], italic=True)
                self.bullets(r.get("bullets"))
            else:
                # company once, roles nested to show promotion
                first, last = roles[-1], roles[0]
                span = f"{first.get('start','')} – {last.get('end','')}".strip(" –")
                self.line_with_date(
                    [(job["company"], True, False),
                     ((" | " + job["location"]) if job.get("location") else "", False, False)],
                    span)
                if job.get("descriptor"):
                    p = self.para()
                    run(p, job["descriptor"], italic=True)
                for r in roles:
                    self.line_with_date([(r["title"], True, True)], self.dates(r), before=2)
                    self.bullets(r.get("bullets"))

    def projects(self):
        pr = self.d.get("projects")
        if not pr:
            return
        self.heading(self.d.get("headings", {}).get("projects", HEADINGS["projects"]))
        for prj in pr:
            left = [(prj["name"], True, False)]
            if prj.get("tech"):
                left.append((" | " + prj["tech"], False, True))
            if prj.get("link"):
                left.append((" | " + prj["link"], False, False))
            self.line_with_date(left, self.dates(prj))
            self.bullets(prj.get("bullets"))

    def education(self):
        ed = self.d.get("education")
        if not ed:
            return
        self.heading(self.d.get("headings", {}).get("education", HEADINGS["education"]))
        for e in ed:
            self.line_with_date(
                [(e["degree"], True, False), (" | " + e["institution"], False, False),
                 ((" | " + e["location"]) if e.get("location") else "", False, False)],
                self.dates(e))
            for det in e.get("details", []):
                p = self.para()
                p.paragraph_format.left_indent = Inches(0.22)
                run(p, det)

    def certifications(self):
        ce = self.d.get("certifications")
        if not ce:
            return
        self.heading(self.d.get("headings", {}).get("certifications", HEADINGS["certifications"]))
        for c in ce:
            if isinstance(c, str):
                self.bullets([c])
                continue
            text = c["name"] + (f" — {c['issuer']}" if c.get("issuer") else "")
            self.line_with_date([(text, False, False)], str(c.get("year", "")), before=1)

    def extra(self):
        for s in self.d.get("extra_sections", []):
            self.heading(s["title"])
            self.bullets(s.get("items"))

    def build(self):
        self.header()
        default = GRAD_ORDER if self.d.get("meta", {}).get("graduate") else DEFAULT_ORDER
        for sec in self.d.get("section_order", default):
            getattr(self, sec)()
        return self.doc


def to_pdf(docx_path: Path):
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        print("LibreOffice not found; skipping PDF", file=sys.stderr)
        return None
    subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir",
                    str(docx_path.parent), str(docx_path)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pdf = docx_path.with_suffix(".pdf")
    return pdf if pdf.exists() else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json_file")
    ap.add_argument("--out", required=True, help="output path without extension")
    ap.add_argument("--pdf", action="store_true", help="also export PDF via LibreOffice")
    ap.add_argument("--paper", choices=["a4", "letter"], default=None)
    ap.add_argument("--font", default=None)
    ap.add_argument("--size", type=float, default=None, help="body font size in pt (10-11.5)")
    ap.add_argument("--accent", default=None, help="hex colour for headings, e.g. 1F3864")
    a = ap.parse_args()

    data = json.loads(Path(a.json_file).read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    paper = a.paper or meta.get("paper", "a4")
    font = a.font or meta.get("font", "Calibri")
    size = a.size or meta.get("font_size", 10.5)
    accent = a.accent or meta.get("accent", "1F3864")

    doc = Builder(data, paper, font, size, accent).build()
    out = Path(a.out).with_suffix(".docx")
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out)
    print(f"wrote {out}")
    if a.pdf:
        pdf = to_pdf(out.resolve())
        if pdf:
            try:
                from pypdf import PdfReader
                n = len(PdfReader(str(pdf)).pages)
                print(f"wrote {pdf} ({n} page{'s' if n != 1 else ''})")
            except Exception:
                print(f"wrote {pdf}")


if __name__ == "__main__":
    main()
