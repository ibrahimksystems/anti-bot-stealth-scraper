# Enterprise Anti-Bot Stealth Scraper & Data Pipeline

A production-grade, asynchronous B2B Web Scraping and Data Extraction Engine built with Python 3.12+, Camoufox (Stealth Firefox), Playwright, and Pydantic v2. Designed to reliably bypass sophisticated anti-bot protections (Cloudflare Turnstile, Akamai, Datadome) while maintaining strict schema integrity.

---

## Key Features

* **Advanced Anti-Bot Evasion:** Powered by `Camoufox` to spoof browser fingerprints, WebGL contexts, TLS handshakes, and human-like cursor movements.
* **Strict Type Safety & ETL:** Built-in `Pydantic v2` data pipeline ensuring all extracted elements meet strict B2B runtime schema rules.
* **Asynchronous & Resilient:** Fully `asyncio`-driven browser orchestration with automated exponential backoff retries for 403/429 rate limits.
* **Dual Format Export:** Clean output serialization to structured JSON and CSV formats out-of-the-box.
* **Robust Test Coverage:** Integrated `pytest-asyncio` test suite validating both local Pydantic transformation models and live target evasion.

---

## Architecture Blueprint

```text
  [ Target Website ]
          │
          ▼  (Cloudflare / Datadome Protected)
┌───────────────────────────────────┐
│       StealthEngine Module        │  <-- AsyncCamoufox (Firefox Fingerprint Spoofing)
└─────────────────┬─────────────────┘
                  │ Raw HTML / Response
                  ▼
┌───────────────────────────────────┐
│        ETLPipeline Module         │  <-- Pydantic v2 Schema Validation & Cleaners
└─────────────────┬─────────────────┘
                  │ Validated Objects
                  ▼
      [ JSON / CSV Export ]
Quickstart
1. Prerequisites
Python 3.12+

Virtual Environment (venv)

2. Installation & Setup
Bash
# Clone the repository
git clone https://github.com/ibrahimksystems/anti-bot-stealth-scraper.git
cd anti-bot-stealth-scraper

# Activate virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies and fetch stealth browser binaries
pip install -r requirements.txt
camoufox fetch
3. Environment Configuration
Copy .env.example to .env and adjust your execution settings:

Ini, TOML
HEADLESS=true
HUMANIZE=true
MAX_RETRIES=3
TIMEOUT_SECONDS=30000
Running Test Suite
Validate schema parsing and live anti-bot execution:

Bash
python -m pytest tests/
License & Support
Distributed under the MIT License. Developed by ibrahimksystems (ibrahimksystems@duck.com).
