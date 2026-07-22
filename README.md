# AI News Agent

An automated pipeline that fetches the latest AI news from multiple sources, summarizes each article using Gemini, and emails the digest to subscribers — fully automated, fully free, and running on a schedule via GitHub Actions.

**Want the digest in your inbox?** [Subscribe here](https://docs.google.com/forms/d/e/1FAIpQLScX3COAk9hA5TKSdZbWPgSSKpU8ue0cqJq3OGzCettAl28qJg/viewform?usp=publish-editor)

---

## What it does

1. **Fetches** the latest AI articles from TechCrunch, VentureBeat, and The Verge (RSS feeds)
2. **Filters** out anything already processed before, so no duplicates
3. **Summarizes** each new article into a short, readable post using Google's Gemini API
4. **Emails** the digest to everyone on the subscriber list (managed via a public Google Form)
5. **Runs itself** every 4 hours, automatically, with no manual triggering

## How it's built

```
ai_agent/
├── news_fetcher.py   # pulls articles from RSS feeds
├── dedup.py           # tracks which articles have already been processed
├── summarizer.py       # turns article text into a short post via Gemini
├── subscribers.py      # pulls the live subscriber list from Google Sheets
├── emailer.py          # sends the HTML digest email
├── main.py             # orchestrates the full pipeline
└── .github/workflows/run.yml   # schedules the pipeline on GitHub Actions
```

Each file has one job. `main.py` is the only file that knows the full sequence — everything else is swappable without touching the rest.

## Why these choices

- **RSS instead of scraping** — free, stable, and doesn't fight a website's terms of service.
- **Gemini over other LLMs** — genuinely usable free tier, good for a hobby-scale bot posting every few hours.
- **Email instead of X/LinkedIn** — X's API dropped its free tier entirely in early 2026 (pay-per-post now), and LinkedIn's posting API requires a verified company page and an OAuth flow that felt disproportionate for this project. Gmail's App Password approach is free, ToS-compliant, and simple.
- **Google Forms + Sheets as a "database"** — no server, no hosting cost, and non-technical people can subscribe/unsubscribe without touching any code.
- **GitHub Actions for scheduling** — free compute on a cron schedule, no server to maintain or pay for.
- **Modular file structure** — swapping the LLM, the email method, or the news source later only requires touching one file, not the whole codebase.

## What I learned building this

- How RSS feeds work and why they're a cleaner alternative to scraping
- Structuring a Python project into modules instead of one long script, and why that matters as a project grows
- Working with LLM APIs (prompt design, handling rate limits and transient server errors with retry logic)
- OAuth-style authentication (API keys, access tokens, app permissions) and why services separate read vs. write access
- Environment variables and GitHub Secrets — why credentials should never live in code, especially in a public repo
- Git fundamentals: init, commit, push, pull, merge conflicts, and rewriting/rotating credentials after an accidental exposure
- Debugging real-world errors: import collisions with installed packages, deprecated API models, case-sensitivity issues between Windows and Linux (relevant once code runs on GitHub's Linux-based runners)
- CI/CD basics — how GitHub Actions checks out code, installs dependencies, injects secrets, and runs a script on a schedule
- Using a public Google Sheet as a lightweight, serverless way to manage dynamic user data

## What I ran into along the way

- **X's API free tier disappeared** mid-project (moved to pay-per-post in Feb 2026), which forced a pivot from "post to X" to "email digest" as the delivery method
- **LinkedIn's posting API** requires a verified company page just to create a developer app — another dead end for a lightweight personal project
- **Gemini model deprecation** — `gemini-2.5-flash` stopped being available to new API keys mid-project, requiring a switch to `gemini-3.5-flash`


## Tech stack

- Python 3.11+
- `feedparser` — RSS parsing
- `google-genai` — Gemini API
- `requests` — fetching the public subscriber CSV
- `smtplib` (built-in) — sending email via Gmail
- GitHub Actions — scheduling and automation
- Google Forms + Sheets — subscriber management, published as public read-only CSVs

## Running it yourself

1. Clone the repo and install dependencies: `pip install -r requirements.txt`
2. Set the required environment variables: `GEMINI_API_KEY`, `EMAIL_ADDRESS`, `EMAIL_APP_PASSWORD`, `SUBSCRIBE_CSV_URL`, `UNSUBSCRIBE_CSV_URL`
3. Run `python main.py`

To automate it on your own schedule, fork the repo, add the same variables as GitHub Secrets, and GitHub Actions will pick up `.github/workflows/run.yml` automatically.
