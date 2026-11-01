# Resume Builder — a Claude Skill

A Claude skill for building, tailoring and critiquing **ATS-optimized resumes and CVs** matched to a specific job description, following:

- **Harvard Career Services** resume standards (action verbs, no pronouns, achievement-focused bullets)
- **r/EngineeringResumes** best practices (single column, one page under ~10 years, XYZ bullets)
- **Big-tech recruiter knowledge**: Google (XYZ formula), Amazon (Leadership Principles), Meta (impact), Microsoft, Apple, startups
- **Country/region conventions**: US, Canada, UK, Ireland, Germany/Austria, Switzerland, France, Netherlands/Nordics, Spain/Southern Europe, Latin America, India, Australia/NZ, Singapore, Gulf, Japan, China

Every role gets **domain context** (industry, data, users, business impact), and Spanish/LATAM and other language versions are written natively rather than translated.

It will never invent employers, titles, skills or metrics. Missing requirements are reported as gaps, and uncertain numbers are marked `[confirm]`.

## What it does

1. Gathers your career history, the target JD and the target country
2. Dissects the JD into must-have and nice-to-have skills, keywords and values language
3. Maps your real evidence to each requirement and flags gaps
4. Writes quantified XYZ/CAR bullets in the JD's vocabulary, ordered by relevance
5. Renders an ATS-safe single-column `.docx` + `.pdf`
6. Verifies ATS parseability, keyword coverage, page count and regional fit
7. Delivers the resume with a short report: coverage before → after, gaps, items to confirm

It also has a **critique mode** (scorecard + top fixes) and handles **country conversion** (e.g., US resume → German Lebenslauf).

## Repository layout

```
resume-builder/
├── SKILL.md                         # skill entry point (workflow)
├── references/
│   ├── jd-matching.md               # JD dissection, evidence mapping, tailoring
│   ├── bullet-writing.md            # XYZ/CAR formulas, action verbs, seniority signals
│   ├── ats-rules.md                 # file formats, layout, fonts, ATS myths
│   ├── regional-conventions.md      # 15+ countries/regions + conversion checklist
│   ├── recruiter-insights.md        # Google, Amazon, Meta, Microsoft, Apple, startups
│   └── section-guide.md             # section order, length, gaps
├── scripts/
│   ├── jd_match.py                  # keyword coverage vs JD (required/preferred)
│   ├── build_resume.py              # JSON → ATS-safe .docx (+ .pdf)
│   └── ats_check.py                 # parsing-hazard checker for .docx/.pdf
├── assets/
│   └── resume_example.json          # input schema + example
└── evals/                           # test cases (claude plugin eval format)
docs/
└── SOURCES.md                       # sources and acknowledgements
examples/
├── sample_jd.txt
├── Alex_Murphy_CV.docx              # sample output
└── Alex_Murphy_CV.pdf
```

## Install

**Claude.ai / Claude desktop:** zip the `resume-builder/` folder (or use the packaged `.skill` file from Releases) and upload it under Settings → Capabilities → Skills.

**Claude Code:** copy the folder into your skills directory:

```bash
cp -r resume-builder ~/.claude/skills/
```

Then just ask Claude things like:

> "Here's my resume and a JD for a Senior Backend Engineer at Stripe Dublin — tailor it."
> "Review my CV and convert it for jobs in Berlin."
> "Will this resume get past ATS?"

## Using the scripts directly

```bash
pip install -r requirements.txt

# Keyword coverage of a resume against a job description
python resume-builder/scripts/jd_match.py --jd examples/sample_jd.txt --resume examples/Alex_Murphy_CV.pdf

# Build a resume from JSON (A4 or US Letter) and export PDF (needs LibreOffice)
python resume-builder/scripts/build_resume.py resume-builder/assets/resume_example.json \
  --out out/Alex_Murphy_CV --pdf --paper a4

# Check a resume for ATS hazards with regional page-length rules
python resume-builder/scripts/ats_check.py out/Alex_Murphy_CV.docx --region ie --years 8
```

`ats_check.py` regions: `us`, `ca`, `uk`, `ie`, `eu`, `in`, `au`, `gulf`, `other`.

### JSON options (`meta`)

| Key | Values | Effect |
|---|---|---|
| `paper` | `a4` / `letter` | Page size (Letter for US/Canada) |
| `font`, `font_size` | e.g. `Calibri`, `10.5` | Body font |
| `margin_in` | e.g. `0.6` | Side margins in inches |
| `accent` | hex, e.g. `1F3864` | Heading colour |
| `graduate` | `true` / `false` | Education first |

Top-level `section_order` and `headings` let you reorder and rename sections (e.g. `"summary": "Personal Profile"` for UK/Ireland).

## Running the evals

With Claude Code v2.1.269+, from the `resume-builder/` folder:

```bash
claude plugin eval . --allow-tools Write,Edit,Bash
```

## Requirements

- Python 3.9+
- `python-docx`, `pdfplumber`, `pypdf`
- LibreOffice (optional, for PDF export and page counting)

## Disclaimer

Country conventions and recruiter practices change and vary by employer. Treat them as sensible defaults, and check anything legally sensitive (work authorisation, personal data) against the employer's instructions.

## Acknowledgements

See [docs/SOURCES.md](docs/SOURCES.md). Parts of the bullet rules, domain-context guidance, Spanish-language guidance and the pre-delivery checklist are adapted from [dabydat/resume-builder-skill](https://github.com/dabydat/resume-builder-skill) (MIT).

## License

MIT, see [LICENSE](LICENSE).
