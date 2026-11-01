<p align="center">
  <h1 align="center">Tech Resume & CV Builder for Claude</h1>
  <p align="center">
    <img src="https://img.shields.io/badge/Claude_AI-Skill-blueviolet?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude AI Skill">
    <img src="https://img.shields.io/badge/Tech%20Resume%20%2F%20CV-blue?style=for-the-badge" alt="Tech Resume CV Skill">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
  </p>
</p>

A Claude skill for creating professional technology resumes and CVs with strong ATS awareness, recruiter-friendly structure, and impact-focused writing. It is optimized for software engineering and technical roles while still supporting UK, EU, and Irish market conventions where relevant.

This project keeps the original high-quality resume advice and refocuses it around what it does best: helping technical candidates present themselves clearly and professionally in job applications.

---

## What This Skill Does

This skill helps Claude act as a technical resume consultant that can:

- Build a software or tech resume from scratch
- Improve an existing tech resume or CV
- Tailor a resume for a specific engineering or technical role
- Support U.S., UK, EU, and Irish hiring conventions
- Write stronger bullet points using measurable impact and domain context
- Keep ATS principles in mind without over-optimizing the document
- Produce recruiter-friendly output for applications, referrals, and interviews

---

## Tech-Focused Scope

This project is intentionally built for technology careers, including:

- Software engineering
- Backend, frontend, full-stack, mobile, DevOps, data engineering, QA, platform, and infrastructure roles
- Product engineering and technical product work
- Technical internships and early-career software roles
- Mid-level and senior engineering profiles
- Technical CVs for UK, EU, and Ireland job markets

This is not a general-purpose document builder for every profession. The emphasis is on technical candidates and technical hiring standards.

---

## UK / EU / Ireland Support

The skill supports the following conventions where relevant:

- UK resume conventions for tech roles
- EU and Irish CV patterns for candidates applying internationally
- terminology and phrasing adjustments for local hiring expectations
- flexible format choices depending on job market and recruiter preference

This keeps the skill useful for technical candidates applying across Europe without turning it into a general business or non-technical resume tool.

---

## Market Modes

The skill should adapt based on the target market and document type.

### 1. Default U.S. Tech Resume
- concise, achievement-focused formatting
- strong skills-first layout for engineering roles
- suitable for U.S. hiring portals and recruiter workflows

### 2. UK Tech Resume
- typically shorter, clearer, and achievement-led
- often includes concise professional summary and direct role matching
- keep formatting sharper and less dense than a U.S. two-page version

### 3. EU / Ireland Tech CV
- more likely to include a detailed CV structure
- often more explicit about education, projects, certifications, and technical skills
- suitable for applications in continental Europe and Ireland

### 4. Remote / International Tech Applications
- keep a reusable core version
- adjust wording and emphasis for the target company market and local conventions

---

## Technical Role Templates

The skill should support common engineering variants without forcing one generic template:

- Backend Engineer
- Frontend Engineer
- Full-Stack Engineer
- Platform / DevOps Engineer
- Data Engineer
- QA / Automation Engineer
- Security Engineer
- ML / AI Engineer
- Site Reliability / Infrastructure Engineer

Each template changes emphasis:
- infrastructure roles prioritize reliability and scale
- frontend roles prioritize product impact and customer experience
- data roles prioritize analytical systems and data quality
- backend roles prioritize systems, APIs, architecture, and performance

---

## Quick Start

### Option 1: Install the Skill in Claude.ai

1. Download the skill file from this repository
2. Open Claude.ai and go to Settings → Skills
3. Upload the skill file
4. Ask Claude: “Help me build my software engineering resume” or “Tailor my CV for a UK tech role”

### Option 2: Use with Claude Code

```bash
git clone https://github.com/your-username/resume-builder-skill.git
cp -r resume-builder-skill/skill/ ~/.claude/skills/user/resume-builder/
```

### Option 3: Use the Guidance Files Directly

The reference files remain useful as standalone guidance for resume editing and review.

---

## Core Principles

### 1. Focus on technical relevance

The skill should prioritize the work that matters most for engineering and technical hiring:

- product or platform context
- domain experience
- architecture and system responsibility
- technical depth and impact
- measurable results

### 2. Write for recruiters and hiring managers

The strongest technical bullet points answer:

- What system or product was involved?
- What did you build or improve?
- What technology or architecture was used?
- What outcome or measurable result followed?

### 3. Keep a flexible but structured format

The skill should still support strong structure, but it should adapt to user context:

- one-page resume for early-career candidates
- one- to two-page resumes for mid-level engineers
- more detailed CVs for UK/EU and international applications

### 4. Use ATS awareness without over-engineering

The document should be easy to parse, strong in keywords, and readable by humans. The goal is relevance and clarity, not keyword stuffing.

---

## Supported Use Cases

This skill is meant to help with:

- Building a software engineering resume from scratch
- Optimizing an existing technical resume
- Tailoring a resume to a specific engineering role
- Improving bullet points for impact and clarity
- Creating UK, EU, or Ireland-specific technical CV versions
- Reviewing resumes for technical relevance and ATS readability

---

## Repository Structure

```text
resume-builder-skill/
├── README.md
├── LICENSE
├── resume-builder.skill
├── docs/
│   ├── INSTALLATION.md
│   └── SOURCES.md
├── skill/
│   ├── SKILL.md
│   └── references/
│       ├── format-and-structure.md
│       ├── bullet-writing-guide.md
│       ├── ats-and-keywords.md
│       └── common-mistakes.md
└── examples/
    ├── kiran-devops-engineer-resume.md
    └── sample-fullstack-engineer-resume.md
```

---

## Example Files

The examples folder includes fresh technical samples for the skill:

- [examples/kiran-devops-engineer-resume.md](examples/kiran-devops-engineer-resume.md) — DevOps engineer resume example for Kiran
- [examples/sample-fullstack-engineer-resume.md](examples/sample-fullstack-engineer-resume.md) — Full-stack engineer resume example

---

## Example Prompts

- “Help me build my software engineering resume.”
- “Rewrite my existing resume for a backend engineer role.”
- “Tailor my CV for a UK software engineer position.”
- “Make my resume more ATS-friendly for a full-stack role.”
- “Review my technical resume and improve the bullets for impact.”
- “Create a version of my CV for a European tech job market.”

---

## Contribution

This project is focused on technical career documents, but there is room to improve the skill for:

- more engineering subfields
- UK, EU, and Ireland conventions
- stronger technical bullet writing examples
- additional ATS guidance for modern hiring systems
- more sample resumes for different roles and seniority levels

---

## License

MIT License — see [LICENSE](./LICENSE).

---

> “A strong tech resume is not just a list of tools. It is a concise proof of technical impact, business value, and fit for the role.”
