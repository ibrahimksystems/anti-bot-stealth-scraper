import asyncio
from typing import List, Dict, Any
from src.config import ScraperConfig
from src.stealth import AntiBotStealthEngine

class StealthPipeline:
    def __init__(self, targets: List[str]):
        self.targets = targets

    async def run(self) -> List[Dict[str, Any]]:
        results = []
        for url in self.targets:
            config = ScraperConfig(target_url=url)
            engine = AntiBotStealthEngine(config)
            res = await engine.execute_request()
            results.append(res)
        return results

if __name__ == "__main__":
    urls = ["https://httpbin.org/ip", "https://now.httpbin.org/"]
    pipeline = StealthPipeline(urls)
    res = asyncio.run(pipeline.run())
    print(f"Pipeline Execution Complete. Processed {len(res)} targets.")
