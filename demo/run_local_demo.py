"""Run the end-to-end extraction pipeline against a local test target."""

import asyncio
import threading

from demo.local_target import create_server
from src.pipeline import ETLPipeline
from src.stealth import stealth_engine


async def main():
    server = create_server()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        url = "http://127.0.0.1:8765/"
        raw = await stealth_engine.fetch_page_content(url)
        if not raw.get("success"):
            raise RuntimeError(f"Local extraction failed: {raw.get('error')}")

        pipeline = ETLPipeline(output_dir="demo/output")
        item = pipeline.process_raw_payload(raw)
        if item is None:
            raise RuntimeError("Pipeline validation failed for local demo payload.")

        json_path = await pipeline.export_to_json([item], "local_demo.json")
        csv_path = await pipeline.export_to_csv([item], "local_demo.csv")

        print("PHASE 4 LOCAL DEMO: PASS")
        print(f"Target: {url}")
        print(f"HTTP status: {item.status_code}")
        print(f"Title: {item.title}")
        print(f"Content length: {item.content_length}")
        print(f"JSON: {json_path}")
        print(f"CSV: {csv_path}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    asyncio.run(main())
