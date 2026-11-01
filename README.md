# Build My Resume

Build polished, ATS-friendly resumes and CVs tailored to a specific job description, region, and hiring context.

This project turns resume writing into a repeatable workflow: read the job description, extract what matters, map your evidence, and generate recruiter-ready output that is clearer, more targeted, and easier to defend.

## Why this project exists

Most resumes fail because they are generic, unfocused, and written for the applicant instead of the hiring team.

This repo helps you:

- tailor a resume to a specific role and company
- match the language of the job description
- strengthen bullet points with measurable impact
- improve ATS compatibility without sacrificing readability
- adapt formatting and tone for different countries and hiring norms
- critique and refine the output before sending it

It is designed around the real patterns recruiters and hiring teams look for: strong role-based storytelling, domain context, impact-driven bullets, and region-aware formatting.

---

## Quick Start

### Option 1: Install the skill in Claude.ai

1. Download the [`resume-builder.skill`](resume-builder.skill) file from this repository
2. Open Claude.ai → Settings → Skills
3. Upload the `.skill` file
4. Ask Claude things like:
   - "Help me create my resume"
   - "Tailor my CV for this job description"
   - "Review my resume and make it ATS-friendly"

> A `.skill` file is a packaged instruction set that teaches Claude how to work with this resume workflow.

### Option 2: Use it with Claude Code

```bash
git clone git@github.com:anugurthi/build-my-resume.git
cd build-my-resume
cp -r resume-builder ~/.claude/skills/
```

Then invoke it from Claude Code with prompts like:

- "Build my resume for a Senior Backend Engineer role in Dublin"
- "Convert this US resume into a German CV"
- "Review my resume against this job description and flag gaps"

### Option 3: Use the scripts directly

```bash
pip install -r requirements.txt
```

Then run the local tools:

```bash
# Check keyword coverage against a job description
python resume-builder/scripts/jd_match.py --jd examples/sample_jd.txt --resume examples/Alex_Murphy_CV.pdf

# Build a resume from JSON and export a PDF
python resume-builder/scripts/build_resume.py resume-builder/assets/resume_example.json \
  --out out/Alex_Murphy_CV --pdf --paper a4

# Check a resume for ATS and formatting issues
python resume-builder/scripts/ats_check.py out/Alex_Murphy_CV.docx --region ie --years 8
```

---

## What the project does

1. Reads your experience, target role, and job description
2. Extracts required and preferred skills from the JD
3. Maps your evidence to the actual requirements
4. Writes strong bullet points using impact-oriented framing
5. Reorders and refines content for clarity and relevance
6. Generates ATS-safe output in editable and export-friendly formats
7. Flags missing evidence, weak statements, and risky assumptions

It also supports:

- country-aware resume conventions
- critique mode and improvement scoring
- ATS review and compatibility checks
- output optimization for role-specific contexts

---

## Knowledge sources

This project draws on a mix of resume-writing standards, recruiter heuristics, and ATS guidance from widely cited sources, including:

- Harvard Career Services
- r/EngineeringResumes
- The Tech Resume Inside Out
- Tech Interview Handbook
- Google XYZ formula guidance
- recruiter and hiring-manager patterns from major tech employers

> Full source references and attribution are recorded in [docs/SOURCES.md](docs/SOURCES.md).

---

## Repository structure

```text
build-my-resume/
├── LICENSE
├── README.md
├── requirements.txt
├── resume-builder.skill
├── docs/
│   └── SOURCES.md
├── examples/
│   ├── sample_jd.txt
│   └── sample outputs (if present)
├── resume-builder/
│   ├── SKILL.md
│   ├── assets/
│   │   └── resume_example.json
│   ├── evals/
│   │   └── case files and graders
│   ├── references/
│   │   ├── ats-rules.md
│   │   ├── bullet-writing.md
│   │   ├── jd-matching.md
│   │   ├── recruiter-insights.md
│   │   ├── regional-conventions.md
│   │   └── section-guide.md
│   └── scripts/
│       ├── ats_check.py
│       ├── build_resume.py
│       └── jd_match.py
└── .gitignore
```

---

## Key principles

### 1. Domain context is everything

A resume becomes much stronger when it clearly explains the business, users, or systems involved.

Instead of a vague summary, the goal is to show the actual value created.

### 2. Impact beats activity

Good bullet points describe:

- what was done
- what changed
- why it mattered
- how it was measured

### 3. ATS optimization should be quiet, not awkward

The best ATS-friendly resume is still readable by humans. This project tries to optimize for both.

### 4. Region matters

Resume expectations differ by geography. A strong US-style resume may not be appropriate for Germany, Ireland, India, or LATAM without adaptation.

---

## Example workflow

A common use case looks like this:

1. Upload or paste a job description
2. Add your experience or CV text
3. Choose the target country/region
4. Ask the skill to tailor the resume
5. Review the result for gaps, ATS risk, and relevance
6. Export the final version as a polished PDF or DOCX

---

## Requirements

- Python 3.9+
- `python-docx`, `pdfplumber`, `pypdf`
- LibreOffice for export and page-count tasks when needed

---

## Acknowledgements

This project builds on established resume best practices and public research. See [docs/SOURCES.md](docs/SOURCES.md) for the full source list and attribution.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

> A resume is not an autobiography. It is a marketing document for the role you want next.
