from scrapegraphai.graphs import SmartScraperGraph
from dotenv import load_dotenv
import os

load_dotenv()

graph_config = {
    "llm": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "openai/gpt-4o-mini",
    },
    "embedding": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "text-embedding-3-small",
    }
}

# smart_scraper_multi_graph = SmartScraperMultiGraph(
#     prompt="找到最新的五個成大住宿服務組辦的活動",
#     config=graph_config,
#     source="https://housing-osa.ncku.edu.tw/p/403-1052-407-1.php?Lang=zh-tw",
#     schema=schema,
# )
smart_scraper_graph = SmartScraperGraph(
    prompt="總結海狸大師最新的五篇文章",
    config=graph_config,
    source="https://yenslife.top",
)
result = smart_scraper_graph.run()
print(result)