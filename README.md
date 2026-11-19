# Anti-Bot Stealth Scraper

Production-grade web scraping and data extraction framework for high-friction targets.

Built for engineers who need reliable structured data from sites protected by Cloudflare, Turnstile, Datadome, Akamai, rate limiting, or aggressive bot detection.

## Why this project exists

Most scrapers fail in production because they optimize for one-off requests, not sustained extraction.  
This project is designed around the problems that actually matter:

- TLS and browser fingerprinting
- proxy rotation and health checks
- realistic pacing and retry behavior
- strict output validation
- operational reliability
- clean integration into downstream pipelines

## Features

- **Stealth browsing** — Camoufox / Playwright-based headless execution
- **TLS fingerprinting** — JA3/JA4-style protocol spoofing
- **Proxy rotation** — automatic rotation with health monitoring
- **User-Agent rotation** — realistic browser identity management
- **Rate-limit handling** — configurable pacing, backoff, and retries
- **Structured output** — Pydantic v2 validation for reliable downstream ingestion
- **CLI-first design** — easy to script, automate, and integrate
- **Test coverage** — unit and integration tests for core pipeline behavior

## Installation

```bash
git clone https://github.com/ibrahimksystems/anti-bot-stealth-scraper.git
cd anti-bot-stealth-scraper

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium
```

## Quick start

```bash
python -m src.cli scrape --url https://example.com
```

With proxy rotation:

```bash
python -m src.cli scrape --url https://example.com --proxy-list proxies.txt
```

Stealth mode:

```bash
python -m src.cli scrape --url https://example.com --stealth
```

## Configuration

Environment variables:

| Variable | Description | Default |
|---|---|---|
| `PROXY_LIST` | Path to proxy list file | `proxies.txt` |
| `USER_AGENTS` | Path to user agents file | `user_agents.txt` |
| `REQUEST_DELAY` | Delay between requests (seconds) | `2.0` |
| `MAX_RETRIES` | Maximum retry attempts | `3` |
| `TIMEOUT` | Request timeout (seconds) | `30` |

Example `.env`:

```env
PROXY_LIST=./proxies.txt
USER_AGENTS=./user_agents.txt
REQUEST_DELAY=2.5
MAX_RETRIES=5
TIMEOUT=45
```

## Project structure

```
anti-bot-stealth-scraper/
├── src/
│   ├── cli.py            # CLI entrypoint
│   ├── config.py         # Configuration management
│   ├── pipeline.py       # Scraping pipeline orchestration
│   ├── proxy_manager.py  # Proxy rotation and health checks
│   ├── security.py       # Security inspection and validation
│   └── stealth.py        # Anti-detection behavior
├── tests/
├── demo/
├── scripts/
└── docs/
```

## Testing

```bash
pytest tests/ -v
```

Run local demo:

```bash
python demo/run_local_demo.py
```

## Use cases

- B2B lead data extraction
- pricing intelligence
- competitor monitoring
- e-commerce data collection
- AI training data pipelines
- high-friction web ingestion

## License

MIT License — see [LICENSE](LICENSE).

## Built by

**Ibrahim K. Systems**  
Production data engineering and anti-bot extraction for AI systems.
