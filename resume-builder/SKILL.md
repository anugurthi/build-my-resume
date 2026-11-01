---
name: resume-builder
description: Build, rewrite, tailor or critique professional ATS-optimized resumes and CVs that match a specific job description, using Harvard Career Services standards, r/EngineeringResumes best practices, big-tech recruiter knowledge (Google, Amazon, Meta, Microsoft, Apple) and country-specific conventions (US, UK, Ireland, EU/Germany, India, Canada, Australia, Gulf, Singapore, Japan and more). Use this skill whenever the user wants a resume or CV written, improved, reviewed, scored, tailored to a job posting or JD, converted for another country, or checked for ATS compatibility — even if they just paste a resume and a job link and say "make this better" or "will this get past ATS?". Also use for turning a LinkedIn profile or career history into a resume, and for keyword gap analysis against a JD.
---

# Resume Builder

Produce a resume that (1) parses cleanly in an Applicant Tracking System, (2) matches the target job description honestly and specifically, (3) reads well to a recruiter in the 6–10 seconds of the first skim, and (4) follows the conventions of the country where the person is applying.

The person's career is the raw material; the job description is the brief. Your job is the editor in between: pick what's relevant, phrase it as impact, and present it in a format that machines and humans both read correctly.

## Reference files — read the ones you need

| File | Read when |
|---|---|
| `references/jd-matching.md` | Any time there is a job description (almost always) |
| `references/bullet-writing.md` | Writing or rewriting experience/project bullets |
| `references/ats-rules.md` | Choosing format/output, or the person asks about ATS |
| `references/regional-conventions.md` | Target country is known, or differs from where the person lives |
| `references/recruiter-insights.md` | Big-tech / FAANG target, senior/staff roles, or critique requests |
| `references/section-guide.md` | Deciding section order, what to include/cut, career-stage specifics |

## Scripts

- `scripts/jd_match.py` — keyword coverage of a resume against a JD. `python scripts/jd_match.py --jd jd.txt --resume resume.txt [--json]`. Gives matched/missing hard skills, coverage %, and keyword frequencies. Use it before and after tailoring; it's a guide, not a target to game.
- `scripts/build_resume.py` — renders a resume from a JSON file into an ATS-safe single-column `.docx` (and `.pdf` via LibreOffice if available). `python scripts/build_resume.py resume.json --out Firstname_Lastname_Resume --pdf`. Schema and example: `assets/resume_example.json`.
- `scripts/ats_check.py` — inspects a `.docx` or `.pdf` for parsing hazards (tables, text boxes, headers/footers holding contact info, images, columns, unusual fonts, page count, missing sections). `python scripts/ats_check.py file.docx`.

## Workflow

### 1. Gather inputs (ask only for what's missing)

Needed:
- **Career material**: an existing resume, LinkedIn text, or a description of their history. If none, interview them briefly per role: what they owned, what changed because of them, numbers (users, latency, revenue, cost, time saved, team size).
- **Target job description** (pasted text or a link to fetch). If they have no specific JD, ask for target role + seniority + 1–2 example companies and build a "master" resume for that role family.
- **Target country/region** — infer from the JD's location if present; otherwise ask. This changes length, photo, personal details, spelling, and naming (resume vs CV).

- **Domain context for each role** — industry, kind of data, who the users were, business impact. Turning "developed web apps" into "developed card-issuance features for a fintech serving 50K cardholders" is the biggest single upgrade most resumes need, so ask if it isn't obvious.

Useful but optional: language (e.g., an English and a Spanish version), years of experience, work authorization/visa needs for the target country, output format preference, anything they want hidden (gaps, a role they'd rather drop).

Don't stall the work on optional items. If the person's present, ask the 1–3 questions that change the output most in one message; otherwise state assumptions at the top and proceed.

### 2. Analyse the JD (see `jd-matching.md`)

Extract: job title, seniority signals, must-have vs nice-to-have skills, hard-skill keywords (exact spellings and acronyms), responsibilities, domain, and the company's values language (e.g., Amazon Leadership Principles). Run `jd_match.py` on the original resume to get a baseline.

### 3. Map evidence → requirements

For each top requirement, find the strongest true evidence in the person's history. Build a short mapping table for yourself. Requirements with no evidence are **gaps** — never invent experience to fill them. Surface gaps to the person: either they have evidence you don't know about (ask), or the gap stays and you suggest how to address it (cover letter, adjacent experience, learning project).

### 4. Write

- **Order and length** per region and seniority (`regional-conventions.md`, `section-guide.md`).
- **Bullets** with the XYZ / CAR pattern, strong action verbs, quantified outcomes, the JD's own terminology where truthful (`bullet-writing.md`).
- **Front-load relevance**: the most JD-relevant bullet goes first in each role; the most relevant role/project gets the most bullets.
- **Skills section** mirrors JD keywords the person actually has, grouped (Languages / Frameworks / Cloud & DevOps / Data / Tools). No proficiency bars, no "soft skills" lists.
- **Summary** (if the region/seniority calls for one): 2–3 lines, title + years + 2–3 headline specialities matching the JD + one signature achievement. Skip it for US new grads unless switching careers.

Integrity rules (these protect the person — fabricated claims get caught in interviews and background checks):
- Never invent employers, titles, dates, degrees, certifications, or metrics.
- If a metric is missing, ask for it or use an honest estimate the person confirms ("~30%"), or describe scale qualitatively. Mark any number you're unsure of with `[confirm]` in the draft.
- Rewording a real accomplishment in the JD's vocabulary is good; claiming a technology they never used is not.

### 5. Render

Default output: an ATS-safe `.docx` built with `build_resume.py`, plus a PDF of the same content. In the JSON, set `meta.paper` (`letter` for US/Canada, `a4` elsewhere), `meta.graduate: true` to put Education first, `headings` to rename sections (e.g. "Personal Profile" for UK/IE), and `section_order` to override order. After building, look at the PDF (render page 1 to PNG) to catch awkward wraps or a stray line spilling onto page 2 — tighten wording rather than shrinking margins. File name `Firstname_Lastname_Resume.docx` (or `_CV` for UK/IE/EU/AU/IN conventions). If the person wants a different format (LaTeX, Google Doc, Markdown, plain text for a web form), produce that instead — the content rules don't change. Keep design minimal: one column, standard fonts, no tables/text boxes/icons/graphics, contact info in the body (not the header).

### 6. Verify

1. Run `ats_check.py` on the output and fix any issues.
2. Re-run `jd_match.py` and compare with the baseline. Aim for strong coverage of must-have hard skills the person genuinely has (typically 70%+ of must-haves); don't stuff.
3. Check page count against the regional/seniority norm.
4. Read it as a recruiter would in 8 seconds: are title, most recent role, top skills and one big number visible at a glance?
5. Run the pre-delivery checklist:
   - Single column, standard fonts ≥10 pt body, name fits on one line, contact info in the body
   - Standard headings; reverse-chronological order; dates as `Mon YYYY – Present` with en dashes, right-aligned
   - Every bullet starts with a plain action verb, no pronouns, no end periods, digits for numbers, no "Responsible for"/"Helped"/"Worked on", none of the superfluous verbs listed in `bullet-writing.md`
   - Every role carries domain context; most bullets carry a number; tech appears in bullets and Skills
   - Tense consistent (past for previous roles; current role all-present or all-past)
   - Spelling variant matches the region (US vs UK/IE English); no internal jargon or codenames
   - URLs plain (`github.com/name`), no "Email:" prefixes
   - PDF text is selectable/extractable and page count matches the norm

### 7. Deliver

Give the file(s) plus a short report:
- **Match summary**: coverage before → after, must-haves covered.
- **Gaps** honestly listed, with how to address each.
- **Items to confirm** (`[confirm]` markers, estimated metrics).
- **Country notes** applied (e.g., "No photo or DOB — standard for Ireland; added work authorization line").

Keep the report short; the resume is the deliverable.

## Critique mode

When asked to review/score a resume rather than rewrite it: give a scorecard (ATS parseability, JD match, impact/quantification, clarity & concision, formatting, regional fit — each 1–10 with one line of reasoning), then the top 5 fixes in priority order with before/after rewrites of the weakest bullets. Offer to apply the fixes.

## Other languages
For Spanish, Portuguese, German or other versions, follow "Language versions" in `regional-conventions.md`: write natively (not a literal translation), keep standard tech terms in English, translate headings and month names.

## Multiple applications

For several JDs, keep a master resume (everything, unfiltered) and produce one tailored version per JD. Tailoring usually changes the summary, skills order, bullet order/selection and a few word choices — not the person's history.
