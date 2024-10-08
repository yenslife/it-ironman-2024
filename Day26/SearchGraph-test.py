from scrapegraphai.graphs import SearchGraph
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

search_graph = SearchGraph(
    prompt="找到最新的五個成大住宿服務組辦的活動",
    config=graph_config,
)

result = search_graph.run()
print(result)
