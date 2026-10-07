# Enterprise Authorized Web Data Extraction & ETL Engine

![CI & Code Quality](https://github.com/Ibrahimksystems/anti-bot-stealth-scraper/actions/workflows/ci.yml/badge.svg)

A production-oriented asynchronous Python data-extraction and ETL architecture for targets that the operator is authorized or legally permitted to access.

> **Important:** This project is not intended to defeat, circumvent, or weaken third-party security or access controls. The included demonstration runs against a local test target. Configure additional hosts only where you have explicit authorization.

## Engineering capabilities

- Async browser automation with Playwright/Camoufox
- Strict Pydantic v2 runtime validation
- ETL-style transformation from raw browser payloads to typed records
- JSON and CSV serialization
- Bounded retry/backoff handling for transient failures
- Safety-by-default target allowlist
- Automated unit/integration tests
- Reproducible local demonstration

## Architecture

```text
Authorized / Local Test Target
          |
          v
  Async Browser Engine
          |
          v
     Raw HTML + Metadata
          |
          v
   Pydantic Validation
          |
          v
     ETL Transformation
          |
          v
     JSON / CSV Output
```

## Technology stack

| Component | Technology |
|---|---|
| Language | Python 3.12+ |
| Browser automation | Playwright / Camoufox |
| Validation | Pydantic v2 |
| Settings | pydantic-settings |
| Async runtime | asyncio |
| Testing | pytest / pytest-asyncio |
| Output | JSON / CSV |

## Setup — Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
camoufox fetch
```

Create your local configuration:

```powershell
Copy-Item .env.example .env
```

The default `.env.example` allows only `localhost` and `127.0.0.1`.

## Automated tests

```powershell
python -m pytest
```

The suite covers schema validation, target allowlisting, and JSON/CSV exports without contacting third-party websites.

## Local end-to-end demo

The demo starts a small HTTP server on `127.0.0.1:8765`, opens it through the browser engine, validates the response, and writes JSON/CSV output.

```powershell
python -m demo.run_local_demo
```

Expected high-level result:

```text
PHASE 4 LOCAL DEMO: PASS
Target: http://127.0.0.1:8765/
HTTP status: 200
...
```

Generated demo output is written under `demo/output/` and should not be committed.

## Authorized targets

The browser engine enforces an explicit `ALLOWED_HOSTS` list. For a system you are authorized to access, add its hostname to `.env` deliberately, for example:

```text
ALLOWED_HOSTS=localhost,127.0.0.1,authorized.example.com
```

Only use targets where you have the necessary permission and where applicable comply with the target's terms, robots directives, contractual restrictions, rate limits, and applicable law.

The project does not provide instructions for bypassing CAPTCHAs, access controls, rate limits, WAF protections, or other security mechanisms.

## Project structure

```text
.
├── demo/
│   ├── local_target.py
│   └── run_local_demo.py
├── src/
│   ├── config.py
│   ├── pipeline.py
│   └── stealth.py
├── tests/
│   └── test_pipeline.py
├── .env.example
├── LICENSE
├── README.md
├── pytest.ini
└── requirements.txt
```

## Engineering focus

This repository demonstrates modular Python engineering around browser automation, asynchronous execution, schema validation, ETL processing, resilient error handling, and structured data serialization. The local demo provides a deterministic target so the architecture can be demonstrated without relying on an external website or attempting to circumvent its controls.

## License

MIT License. See `LICENSE`.

Developed by **Ibrahim K. Systems**.
