# Scraping & Browser Automation Demo

A focused Python + Playwright application demonstrating production-oriented browser automation, concurrent scraping, retry handling, rate limiting, structured extraction, and containerized execution against a local authorized test target.

## What it demonstrates

- Python + Playwright browser automation
- Isolated browser sessions/contexts
- Concurrent batch execution with `asyncio`
- Bounded retries with exponential backoff
- Structured JSON extraction
- Rate limiting
- Proxy-manager abstraction in safe demo mode
- Structured logging
- Docker and Docker Compose support
- A local authorized test target for reproducible development

> This project uses a local authorized test target. It does not attempt to bypass Cloudflare or other access controls.

## Architecture

```text
                 ┌──────────────────────┐
                 │   Local Test Target  │
                 │   target_site/       │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     Scraper App      │
                 │      app/main.py     │
                 └──────────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
          Worker 1       Worker 2      Worker N
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                 ┌──────────────────────┐
                 │    results.json      │
                 └──────────────────────┘
```

The worker architecture is designed so that the local demo can be extended to a queue-backed production system without changing the core scraping responsibilities.

## Key engineering decisions

### Concurrent execution

`asyncio` is used to run multiple browser tasks concurrently while keeping execution bounded.

### Retry handling

Transient task failures use bounded retries with exponential backoff rather than retrying indefinitely.

### Session isolation

Browser contexts are isolated so separate tasks do not share session state unintentionally.

### Rate limiting

Requests are rate-limited to avoid uncontrolled traffic and to make the automation behavior predictable.

### Structured extraction

Scraped data is normalized into structured JSON output instead of relying on unstructured console output.

### Proxy abstraction

The project includes a proxy-manager abstraction in safe demo mode so proxy assignment can be separated from the scraping logic.

## Project structure

```text
scraping-automation-demo/
├── app/
│   └── main.py
├── target_site/
├── README.md
├── requirements.txt
├── docker-compose.yml
└── results.json
```

## Run locally

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Start the local authorized target:

```bash
python target_site/server.py
```

Open another terminal and run the scraper:

```bash
source venv/bin/activate
python -m app.main
```

Results are written to:

```text
results.json
```

## Run with Docker

```bash
docker compose up --build
```

The Docker setup runs the scraper against the local target inside the Compose network.

## Demo flow

A Loom/demo recording can show:

1. `app/main.py` and the project architecture.
2. The local authorized target starting successfully.
3. Multiple workers executing concurrently.
4. Session IDs and proxy assignments.
5. An intentionally failing task and bounded retry behavior.
6. The generated `results.json` output.
7. How the worker architecture could scale behind a queue in production.

## Scope and safety

This repository is intentionally designed around a local authorized target. It demonstrates browser automation and scraping engineering patterns without attempting to bypass access controls such as Cloudflare.
