# Installing and Using the Tech Resume / CV Builder

## What is a `.skill` File?

A `.skill` file is a packaged set of instructions for Claude AI. It contains the prompt logic and supporting reference material Claude uses when it recognizes that the user needs help with a technology-focused resume or CV.

This version is optimized for technical roles, while still allowing for UK, EU, and Irish market variations.

---

## What is Included

The skill contains the prompt instructions plus reference material for:

- technical resume and CV structure
- bullet writing and impact language for software and engineering work
- ATS basics and keyword matching
- common mistakes to avoid in tech resumes
- adaptation for UK, EU, and Ireland job markets when relevant

---

## Installation Methods

### Method 1: Claude.ai

1. Download the skill file from this repository
2. Open Claude.ai
3. Go to Settings → Skills
4. Upload the skill file
5. Start asking for technical resume or CV help

Example prompts:
- “Create a resume for a software engineer role”
- “Help me rewrite my CV for a UK tech company”
- “Tailor my resume to this backend engineer job description”
- “Review my technical resume and improve the bullet points”
- “Create a version of my CV suitable for an Irish software market”

### Method 2: Claude Code

```bash
git clone https://github.com/your-username/resume-builder-skill.git
cp -r resume-builder-skill/skill/ ~/.claude/skills/user/resume-builder/
```

### Method 3: Manual Use

You can also use the reference files directly without installing the skill. They are useful for writing, editing, and reviewing technical career documents in Word, Google Docs, or any editor.

---

## Best Practice When Using the Skill

The skill works best when the user provides enough context. It should ideally know:

- target technical role or domain
- years of experience
- country or market
- resume or CV
- whether the goal is a fresh build or rewrite
- any specific job description to tailor against

This helps the skill generate a more relevant and accurate technical document.

---

## Market Modes to Use

The skill should ask for the user’s target market before drafting final content.

### Use these modes as needed
- **U.S. tech resume** — standard engineering resume format
- **UK tech resume** — tighter, concise, highly impact-focused
- **EU / Ireland CV** — more structured and detailed, with explicit education and skill presentation
- **Remote / international role** — keep the core technical story but adapt language to the company market

### Example prompts by market
- “Build my software engineering resume for a UK role”
- “Create a CV for a backend engineer applying in Ireland”
- “Tailor my European tech CV for a product engineering job”
- “Rewrite my resume for a U.S.-based full-stack role”

---

## Troubleshooting

### The skill does not seem to trigger

Try a prompt like:
- “Help me write a resume for a full-stack engineer role”
- “Build a CV for a software engineer applying in Ireland”
- “Review my backend resume for ATS and readability”

### The output feels too generic

Ask for a more specific version, such as:
- “Make it more suitable for a UK engineering market”
- “Adapt it for a senior software engineer profile”
- “Rewrite it with more impact-driven engineering bullets”

### The output is too broad for technical users

Specify the target field and experience level. The skill is meant to support technical candidates, not general business resumes.

---

## Recommended Workflow

1. Define the target engineering or technical role
2. Identify the market: U.S., UK, EU, or Ireland
3. Gather the key experience, stack, and impact metrics
4. Build the document around technical relevance and impact
5. Tailor the final version to the role and market
6. Review grammar, readability, and ATS compatibility

This is the most reliable way to use the skill effectively for technical applications.
