# Matching a Resume to a Job Description

## Why this matters
Most mid-to-large employers screen through an ATS (Workday, Greenhouse, Lever, iCIMS, SuccessFactors, Taleo, SmartRecruiters, Ashby). Recruiters search the candidate database with keyword queries and filter on knockout questions; some systems also rank candidates by match. Then a human skims. So the resume must contain the JD's real terms (for search) and show evidence for them (for the human). Keyword lists with no evidence fail the human step.

## Step 1 — Dissect the JD

Produce, for yourself, a structured breakdown:

```
Title: Senior Software Engineer, Platform
Level signals: "5+ years", "lead design", "mentor" → senior IC
Must-have (required / "you have"): Java or Go; Kubernetes; AWS; distributed systems; CI/CD
Nice-to-have (preferred / "bonus"): Terraform; Kafka; observability (Prometheus/Grafana)
Responsibilities: design & build services; on-call; mentor; partner with product
Domain: payments / fintech
Values language: ownership, customer obsession, bias for action
Exact strings to mirror: "Kubernetes" (not just k8s), "CI/CD", "microservices", "AWS"
```

Tips:
- Requirements listed first and repeated across the posting are usually the true priorities.
- "Equivalent experience" means the degree is a soft filter.
- Note both acronym and full form ("Amazon Web Services (AWS)", "Continuous Integration/Continuous Deployment (CI/CD)") — include both once on the resume, because recruiters search either.
- Match the job title where honest: if the person was "Software Developer III" and the JD says "Senior Software Engineer", a format like `Senior Software Engineer (Software Developer III)` is acceptable only if the level is genuinely equivalent; otherwise keep the real title and let bullets show seniority.
- If the company is a big-tech firm, read `recruiter-insights.md` for that company's signals.

## Step 2 — Baseline coverage
Run `scripts/jd_match.py --jd jd.txt --resume current.txt`. Note missing must-haves.

## Step 3 — Evidence map

| JD requirement | Evidence from history | Where it goes | Strength |
|---|---|---|---|
| Kubernetes | Migrated 40 services to EKS at X | Role 1, bullet 1; Skills | Strong |
| Kafka | Used it on one project | Role 2 bullet; Skills | Medium |
| Go | None | — | GAP |

Strong evidence goes in the most recent/prominent role and early in its bullet list. Weak-but-real evidence can sit in Skills or a project. Gaps go in the report to the person.

## Step 4 — Tailoring moves (in order of impact)
1. **Summary/headline**: title matching the JD + years + 2–3 must-haves + one achievement.
2. **Skills section**: reorder so JD must-haves appear first; use the JD's spelling.
3. **Bullet selection and order**: lead each role with the most relevant bullet; cut irrelevant bullets before cutting relevant ones.
4. **Vocabulary**: describe the same real work in the JD's words ("built pipelines" → "designed CI/CD pipelines" if that's what it was).
5. **Projects** (early career or career switchers): pick projects that cover gaps.

## Keyword density — don't game it
- Each must-have keyword should appear at least once in context (a bullet) and once in Skills where relevant. 2–3 total mentions is plenty.
- White-text keywords, copying the JD verbatim, or keyword blocks are detectable (many ATSs show plain-text view to recruiters) and read as dishonest. Never do it.
- Soft skills ("communication", "leadership") are shown through bullets (led, mentored, presented), not listed.

## Knockout factors to flag to the person
Work authorization/sponsorship, location/onsite requirements, required degrees, required certifications (e.g., security clearance, CPA, PE), minimum years. You can't fix these with wording — tell the person honestly when one is a likely blocker, and where a resume line helps (e.g., stating authorization status where that's conventional).

## No JD available
Build from 3–5 representative postings for the target title: union of their recurring must-haves forms the target keyword set.
