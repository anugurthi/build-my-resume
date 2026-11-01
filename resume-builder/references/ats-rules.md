# ATS Compatibility Rules

ATS parsers convert the file to plain text and try to map it into fields (name, contact, employers, titles, dates, education, skills). Anything that confuses that conversion can drop content or scramble order. The safest resume is boring in structure and rich in content.

## File format
- **.docx** is the most universally parsed format. A text-based **PDF** (exported from Word/Docs/LaTeX, not scanned or image-based) parses well in modern ATSs (Greenhouse, Lever, Workday, Ashby) and preserves layout for humans. Default: produce both; submit .docx when the portal asks or when unsure, PDF when a human will read it first (email, referral) or when the portal accepts it.
- Never an image, scanned PDF, .pages, or a design-tool export (Canva/Figma) with text as outlines.
- Check the PDF: if you can't select and copy text cleanly in order, an ATS can't either.

## Layout
- Single column. Multi-column layouts can be read row-by-row, interleaving columns.
- No tables for layout, text boxes, shapes, icons, skill bars, charts, or photos (except where regionally required — and then accept the parsing risk; see regional notes).
- Contact info in the document body, not in the Word header/footer — some parsers skip headers/footers.
- Standard section headings: Summary / Professional Summary, Experience / Work Experience / Professional Experience, Education, Skills / Technical Skills, Projects, Certifications, Publications, Awards, Volunteer Experience. Creative headings ("My Journey", "Where I've Been") can fail field mapping.
- Simple bullets (•, -) — avoid custom symbols/emoji.
- Dates consistent and parseable: `Jan 2022 – Present` or `01/2022 – Present` or `2022 – 2024`. Put dates on the same line as the employer/title or right next to them. "Present"/"Current" for ongoing.
- Each role: Title, Company, Location, Dates — in a consistent order throughout.

## Typography
- Standard fonts: Calibri, Arial, Helvetica, Garamond, Georgia, Cambria, Times New Roman, Lato, Source Sans. Body 10–11.5 pt, name 14–20 pt, headings 11–13 pt.
- Margins 0.5–1 inch (1.27–2.54 cm). Don't go below 0.5" to cram content — cut content instead.
- Bold for name, headings, titles/companies; italics sparingly; no colour reliance (a single dark accent colour is fine).
- No ligature-heavy or decorative fonts; avoid special characters that may not map (fancy quotes are fine in modern ATSs, but keep it plain where possible).

## Content mechanics
- Spell out acronyms once alongside the short form for important keywords.
- Use the employer's legal/common name; add a one-line descriptor for obscure companies ("Series B fintech, 200 staff") if useful.
- Links: plain text URLs (linkedin.com/in/name, github.com/name) — hyperlinks are fine but the visible text should be the URL itself, since parsed text loses the link.
- File name: `Firstname_Lastname_Resume.pdf` (or `_CV`). Not `resume_final_v3.pdf`.

## How ATS screening actually works
An ATS is mainly a database and workflow tool: it stores applications, parses fields, tracks stages, and lets recruiters search and filter. Most rejections come from **knockout questions** on the application form (work authorization, location, years, degree) and from **humans** skimming for 5–20 seconds — not from a parser "scoring" the resume. A few systems (e.g., Taleo's requisition ranking, newer AI-match features in Workday and others) rank candidates, but low-ranked resumes generally stay visible. Tailoring still matters because recruiters search by keyword and skim for familiar terms. (Source: Gergely Orosz, *The Tech Resume Inside Out*, with recruiter interviews.)

## Myths to correct politely if the person raises them
- "75% of resumes are rejected by ATS before a human sees them" — this statistic traces back to vendors selling ATS-beating services, not to research.
- "ATS auto-rejects most resumes" — usually it's knockout questions or recruiters filtering/searching, not the parser judging quality. Formatting problems mainly cause missing/garbled fields.
- "You need a 100% keyword match" — no. Cover the must-haves you genuinely have.
- "Hidden white text tricks the ATS" — recruiters see the plain text; it looks dishonest.
- "PDFs can't be parsed" — text PDFs generally parse fine in modern systems; some older/legacy portals do better with .docx.
