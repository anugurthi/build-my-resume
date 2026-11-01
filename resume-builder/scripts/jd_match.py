#!/usr/bin/env python3
"""Keyword coverage of a resume against a job description.

Usage:
    python jd_match.py --jd jd.txt --resume resume.(txt|docx|pdf) [--json] [--extra "term1,term2"]

What it does:
  1. Finds known hard-skill terms (with aliases, e.g. k8s -> Kubernetes) in the JD.
  2. Splits JD terms into "required" vs "preferred" using section cues
     (Requirements / Qualifications / Must have  vs  Preferred / Nice to have / Bonus).
  3. Adds frequent capitalised/technical tokens in the JD not in the dictionary (so new tools are not missed).
  4. Reports which appear in the resume, coverage %, and counts.

It is a guide for honest tailoring, not a score to maximise. Only add a missing keyword to the
resume if the candidate genuinely has that skill.
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

# canonical -> aliases (lowercase). Extend freely.
SKILLS = {
    # languages
    "Python": ["python"], "Java": ["java"], "JavaScript": ["javascript", "js", "ecmascript"],
    "TypeScript": ["typescript", "ts"], "Go": ["golang", "go lang"], "Rust": ["rust"],
    "C++": ["c++", "cpp"], "C#": ["c#", "csharp", ".net c#"], "C": [], "Kotlin": ["kotlin"],
    "Swift": ["swift"], "Scala": ["scala"], "Ruby": ["ruby"], "PHP": ["php"], "R": [],
    "SQL": ["sql"], "Bash": ["bash", "shell scripting", "shell"], "PowerShell": ["powershell"],
    "Dart": ["dart"], "Elixir": ["elixir"], "Haskell": ["haskell"], "MATLAB": ["matlab"],
    # web / frameworks
    "React": ["react", "react.js", "reactjs"], "Angular": ["angular", "angularjs"],
    "Vue": ["vue", "vue.js", "vuejs"], "Next.js": ["next.js", "nextjs"], "Node.js": ["node.js", "nodejs", "node"],
    "Express": ["express", "express.js"], "Django": ["django"], "Flask": ["flask"], "FastAPI": ["fastapi"],
    "Spring Boot": ["spring boot", "springboot"], "Spring": ["spring framework", "spring"],
    ".NET": [".net", "dotnet", "asp.net", ".net core"], "Ruby on Rails": ["rails", "ruby on rails"],
    "GraphQL": ["graphql"], "REST": ["rest", "restful", "rest api", "rest apis", "restful apis"],
    "gRPC": ["grpc"], "HTML": ["html", "html5"], "CSS": ["css", "css3", "sass", "scss"],
    "Tailwind": ["tailwind", "tailwindcss"], "Redux": ["redux"], "Flutter": ["flutter"],
    "React Native": ["react native"], "Android": ["android"], "iOS": ["ios"],
    # cloud / devops
    "AWS": ["aws", "amazon web services"], "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"], "Kubernetes": ["kubernetes", "k8s", "eks", "aks", "gke"],
    "Docker": ["docker", "containers", "containerization", "containerisation"], "Terraform": ["terraform"],
    "Ansible": ["ansible"], "Helm": ["helm"], "CI/CD": ["ci/cd", "cicd", "continuous integration", "continuous delivery", "continuous deployment"],
    "Jenkins": ["jenkins"], "GitHub Actions": ["github actions"], "GitLab CI": ["gitlab ci", "gitlab"],
    "ArgoCD": ["argocd", "argo cd"], "Serverless": ["serverless", "lambda", "aws lambda", "cloud functions"],
    "Linux": ["linux", "unix"], "Git": ["git"], "Microservices": ["microservices", "micro-services", "microservice"],
    "Infrastructure as Code": ["infrastructure as code", "iac"], "CloudFormation": ["cloudformation"],
    "Prometheus": ["prometheus"], "Grafana": ["grafana"], "Datadog": ["datadog"], "Splunk": ["splunk"],
    "OpenTelemetry": ["opentelemetry", "otel"], "Observability": ["observability", "monitoring"],
    "SRE": ["sre", "site reliability"], "Istio": ["istio", "service mesh"],
    # data
    "PostgreSQL": ["postgresql", "postgres"], "MySQL": ["mysql"], "MongoDB": ["mongodb", "mongo"],
    "Redis": ["redis"], "DynamoDB": ["dynamodb"], "Cassandra": ["cassandra"], "Elasticsearch": ["elasticsearch", "opensearch", "elk"],
    "Kafka": ["kafka"], "RabbitMQ": ["rabbitmq"], "Spark": ["spark", "pyspark", "apache spark"],
    "Airflow": ["airflow"], "dbt": ["dbt"], "Snowflake": ["snowflake"], "BigQuery": ["bigquery"],
    "Databricks": ["databricks"], "Hadoop": ["hadoop"], "ETL": ["etl", "elt", "data pipelines", "data pipeline"],
    "NoSQL": ["nosql"], "Oracle": ["oracle"], "SQL Server": ["sql server", "mssql"],
    "Tableau": ["tableau"], "Power BI": ["power bi", "powerbi"], "Pandas": ["pandas"], "NumPy": ["numpy"],
    # AI/ML
    "Machine Learning": ["machine learning", "ml"], "Deep Learning": ["deep learning"],
    "PyTorch": ["pytorch"], "TensorFlow": ["tensorflow"], "scikit-learn": ["scikit-learn", "sklearn"],
    "LLM": ["llm", "llms", "large language model", "large language models"], "Generative AI": ["generative ai", "genai", "gen ai"],
    "RAG": ["rag", "retrieval augmented generation", "retrieval-augmented generation"], "LangChain": ["langchain"],
    "LlamaIndex": ["llamaindex"], "Vector Database": ["vector database", "vector db", "pinecone", "weaviate", "pgvector", "faiss", "chroma"],
    "NLP": ["nlp", "natural language processing"], "Computer Vision": ["computer vision"],
    "MLOps": ["mlops"], "Hugging Face": ["hugging face", "huggingface", "transformers"],
    "Prompt Engineering": ["prompt engineering"], "AI Agents": ["ai agents", "agentic", "agents"],
    "Fine-tuning": ["fine-tuning", "fine tuning", "finetuning"], "SageMaker": ["sagemaker"], "Bedrock": ["bedrock"],
    "Vertex AI": ["vertex ai"], "OpenAI API": ["openai"],
    # practices
    "Distributed Systems": ["distributed systems", "distributed system"], "System Design": ["system design", "systems design"],
    "Agile": ["agile", "scrum", "kanban"], "TDD": ["tdd", "test-driven development", "test driven development"],
    "Unit Testing": ["unit testing", "unit tests", "jest", "junit", "pytest"], "Security": ["security", "appsec", "devsecops"],
    "OAuth": ["oauth", "oauth2", "oidc", "openid connect"], "API Design": ["api design"],
    "Event-Driven Architecture": ["event-driven", "event driven"], "Performance Optimization": ["performance optimization", "performance tuning"],
    "Data Structures": ["data structures"], "Algorithms": ["algorithms"],
    "Mentoring": ["mentoring", "mentor", "mentorship"], "Technical Leadership": ["technical leadership", "tech lead"],
    "Stakeholder Management": ["stakeholder management", "stakeholders"],
    # product / business
    "A/B Testing": ["a/b testing", "a/b tests", "experimentation"], "Jira": ["jira"],
    "Product Management": ["product management", "product roadmap", "roadmap"],
    "SaaS": ["saas"], "Payments": ["payments"], "Fintech": ["fintech"], "Telecom": ["telecom", "telecommunications", "5g"],
}

REQ_CUES = re.compile(r"(requirement|qualification|must[- ]have|what you('| wi)ll need|you have|you bring|minimum|basic qualifications|required)", re.I)
PREF_CUES = re.compile(r"(preferred|nice[- ]to[- ]have|bonus|plus|desirable|ideally|good to have|additional)", re.I)

STOP = set("""a an and or the to of in on for with by at as is are be will you your our we this that from
it its their they role team work working years year experience strong ability skills knowledge using use
including etc across within who what how new more must have has can able plus about us job company
equal opportunity employer""".split())


def read_text(path):
    p = Path(path)
    if p.suffix.lower() == ".docx":
        from docx import Document
        d = Document(p)
        return "\n".join(par.text for par in d.paragraphs)
    if p.suffix.lower() == ".pdf":
        import pdfplumber
        with pdfplumber.open(p) as pdf:
            return "\n".join((pg.extract_text() or "") for pg in pdf.pages)
    return p.read_text(encoding="utf-8", errors="ignore")


def alias_pattern(alias):
    esc = re.escape(alias)
    return re.compile(r"(?<![A-Za-z0-9+#])" + esc + r"(?![A-Za-z0-9+#])", re.I)


def build_patterns(extra):
    pats = {}
    for canon, aliases in SKILLS.items():
        forms = set(a for a in aliases) | {canon.lower()}
        # single letters like C or R are too ambiguous unless exact-case word
        if canon in ("C", "R"):
            pats[canon] = [re.compile(r"(?<![A-Za-z0-9+#/])" + canon + r"(?![A-Za-z0-9+#/])")]
            continue
        # "go" alias only as golang/explicit; canonical 'go' match must be case-sensitive "Go"
        if canon == "Go":
            pats[canon] = [alias_pattern(a) for a in aliases] + [re.compile(r"(?<![A-Za-z])Go(?![A-Za-z])")]
            continue
        pats[canon] = [alias_pattern(f) for f in forms]
    for t in extra:
        pats[t] = [alias_pattern(t.lower())]
    return pats


def count(text, patterns):
    """Count non-overlapping matches across all alias patterns (so 'event-driven architecture' counts once)."""
    spans = sorted({m.span() for p in patterns for m in p.finditer(text)})
    n, end = 0, -1
    for a, b in spans:
        if a >= end:
            n += 1
            end = b
    return n


def split_sections(jd):
    """Label each line of the JD as required / preferred / other based on the nearest preceding cue line."""
    label = "other"
    req, pref, other = [], [], []
    for line in jd.splitlines():
        s = line.strip()
        if not s:
            continue
        short = len(s) < 80
        if short and PREF_CUES.search(s):
            label = "preferred"
        elif short and REQ_CUES.search(s):
            label = "required"
        {"required": req, "preferred": pref, "other": other}[label].append(s)
    return "\n".join(req), "\n".join(pref), "\n".join(other)


def unknown_terms(jd, pats, top=15):
    """Capitalised/technical tokens frequent in the JD but not in the dictionary."""
    known = set()
    for ps in pats.values():
        for p in ps:
            known.add(p.pattern.lower())
    toks = re.findall(r"\b([A-Z][A-Za-z0-9+.#/-]{1,}|[a-z]+[A-Z][A-Za-z0-9]+)\b", jd)
    c = Counter(t for t in toks if t.lower() not in STOP and not any(p.search(t) for ps in pats.values() for p in ps))
    return [t for t, n in c.most_common(top * 3) if n >= 2][:top]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--jd", required=True)
    ap.add_argument("--resume", required=True)
    ap.add_argument("--extra", default="", help="comma-separated extra terms to check")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    jd = read_text(a.jd)
    cv = read_text(a.resume)
    extra = [t.strip() for t in a.extra.split(",") if t.strip()]
    pats = build_patterns(extra)
    req_txt, pref_txt, _ = split_sections(jd)

    rows = []
    for canon, ps in pats.items():
        jd_n = count(jd, ps)
        if not jd_n:
            continue
        tier = "required" if count(req_txt, ps) else ("preferred" if count(pref_txt, ps) else "mentioned")
        rows.append({"term": canon, "tier": tier, "jd_count": jd_n, "resume_count": count(cv, ps)})
    order = {"required": 0, "mentioned": 1, "preferred": 2}
    rows.sort(key=lambda r: (order[r["tier"]], -r["jd_count"], r["term"]))

    def cov(tier=None):
        sel = [r for r in rows if tier is None or r["tier"] == tier]
        if not sel:
            return None
        return round(100 * sum(1 for r in sel if r["resume_count"]) / len(sel))

    unk = unknown_terms(jd, pats)
    unk_rows = [{"term": t, "in_resume": bool(re.search(re.escape(t), cv, re.I))} for t in unk]
    result = {
        "coverage_all_pct": cov(), "coverage_required_pct": cov("required"),
        "coverage_preferred_pct": cov("preferred"),
        "terms": rows,
        "missing_required": [r["term"] for r in rows if r["tier"] == "required" and not r["resume_count"]],
        "missing_other": [r["term"] for r in rows if r["tier"] != "required" and not r["resume_count"]],
        "other_jd_terms_to_review": unk_rows,
        "resume_word_count": len(re.findall(r"\w+", cv)),
    }
    if a.json:
        print(json.dumps(result, indent=2))
        return

    print(f"Coverage — all JD skills: {result['coverage_all_pct']}%  |  required: {result['coverage_required_pct']}%"
          f"  |  preferred: {result['coverage_preferred_pct']}%")
    print(f"Resume words: {result['resume_word_count']}\n")
    print(f"{'term':28} {'tier':10} {'JD':>3} {'CV':>3}")
    for r in rows:
        mark = "  " if r["resume_count"] else "✗ "
        print(f"{mark}{r['term']:26} {r['tier']:10} {r['jd_count']:>3} {r['resume_count']:>3}")
    if result["missing_required"]:
        print("\nMissing REQUIRED (add only if genuinely true):", ", ".join(result["missing_required"]))
    if unk_rows:
        print("\nOther recurring JD terms to review:",
              ", ".join(f"{u['term']}{'' if u['in_resume'] else ' (absent)'}" for u in unk_rows))


if __name__ == "__main__":
    main()
