# Enterprise Anti-Bot Stealth Scraper & Data Pipeline

A production-grade, asynchronous B2B web scraping and data extraction engine built with **Python 3.12+**, **Camoufox**, **Playwright**, and **Pydantic v2**.

Designed for reliable data extraction from modern, anti-bot-protected web applications while maintaining strict schema integrity, resilient execution, and structured output.

---

## Key Features

- **Advanced Browser Automation:** Powered by `Camoufox` and `Playwright` for browser-based data extraction in challenging web environments.
- **Strict Type Safety & ETL:** Built-in `Pydantic v2` data pipeline ensuring extracted elements conform to defined B2B runtime schemas.
- **Asynchronous & Resilient:** Fully `asyncio`-driven browser orchestration with automated exponential-backoff retries for `403` and `429` responses.
- **Dual Format Export:** Structured output serialization to both JSON and CSV.
- **Robust Test Coverage:** Integrated `pytest-asyncio` test suite for validating Pydantic transformations and target execution workflows.

---

## Architecture

```text
[ Target Website ]
        │
        ▼
[ Browser / Anti-Bot Protected Environment ]
        │
        ▼
┌───────────────────────────────────┐
│       StealthEngine Module        │
│   AsyncCamoufox / Playwright      │
└─────────────────┬─────────────────┘
                  │
                  │ Raw HTML / Response
                  ▼
┌───────────────────────────────────┐
│        ETLPipeline Module         │
│ Pydantic v2 Schema Validation     │
│ Data Cleaning & Transformation    │
└─────────────────┬─────────────────┘
                  │
                  │ Validated Objects
                  ▼
        [ JSON / CSV Export ]

        Technology Stack
Component	Technology
Language	Python 3.12+
Browser Automation	Playwright
Stealth Browser	Camoufox
Data Validation	Pydantic v2
Async Runtime	asyncio
Data Processing	ETL Pipeline
Output Formats	JSON / CSV
Testing	pytest / pytest-asyncio

Quickstart
1. Prerequisites
Python 3.12+
Git
Virtual environment (venv)
2. Clone the Repository
git clone https://github.com/ibrahimksystems/anti-bot-stealth-scraper.git
cd anti-bot-stealth-scraper
3. Create a Virtual Environment
Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
4. Install Dependencies
pip install -r requirements.txt

Fetch the Camoufox browser binaries:

camoufox fetch
Environment Configuration

Copy .env.example to .env and configure the execution settings:

HEADLESS=true
HUMANIZE=true
MAX_RETRIES=3
TIMEOUT_SECONDS=30000

Adjust these values according to your execution environment and target workload.

Running the Test Suite

Run the automated test suite with:

python -m pytest tests/

The test suite validates schema parsing, data transformation, and the project's browser execution workflows.

Project Structure
.
├── ...
├── tests/
├── .env.example
├── requirements.txt
└── README.md
Data Pipeline

The extraction workflow follows a structured processing model:

Target Website
      │
      ▼
Browser Automation
      │
      ▼
Raw Data Extraction
      │
      ▼
Pydantic Validation
      │
      ▼
ETL Transformation
      │
      ▼
Structured JSON / CSV

This separation keeps browser interaction, data validation, transformation, and output serialization independently maintainable.

Engineering Focus

The project demonstrates practical engineering patterns for:

Asynchronous browser automation
Structured web data extraction
ETL pipeline architecture
Runtime schema validation
Resilient retry strategies
Rate-limit handling
Structured data serialization
Automated testing
Modular Python architecture
License

Distributed under the MIT License.

Developed by IbrahimK. Systems.
