from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import PromptTemplate
from dotenv import load_dotenv
from rich import print
import os
load_dotenv()

from llama_index.core import Settings

from llama_index.embeddings.openai import OpenAIEmbedding

my_embedding = OpenAIEmbedding(model="text-embedding-3-small")

from llama_index.core import Settings

Settings.embed_model = my_embedding

INDEX_PATH = "index"

# store if not exist
if not os.path.exists(INDEX_PATH):
    documents = SimpleDirectoryReader("data").load_data()
    for doc in documents:
        doc.text = doc.text.replace("跳到主要內容區\n學生事務長信箱\n聯絡我們\n網站地圖\nEnglish\n本校首頁\n回首頁\n", "")
        doc.text = doc.text.replace("搜尋\n\n \n\n主選單\n最新消息 \n新生專區 [*]\n行事曆 \n單位介紹 \n法規與SOP \n表單下載\n住宿知多少 \n宿委會 \n常見Q&A\n連繫方式\n防疫專區\n性別友善專區\n宿舍場地借用\n業務分類\n宿舍申請\n110-113續住試辦計劃\n住宿費減免\n宿舍餐廳\n工程類進度\n東寧宿舍興建\n宿舍自修室\n宿舍簡易廚房\n服務學習三\n宿舍會議記錄\n", "")
        doc.text = doc.text.replace("Jump to the main content block\nOffice of Student Affairs\nContact us\nSite Map\n中文\nNCKU", "")

    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(INDEX_PATH)
else:
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_PATH)
    # load index
    index = load_index_from_storage(storage_context=storage_context)


qa_template = (
"""
以下是上下文
---------------------
{context_str}
---------------------
請根據上下文信息回答以下問題，不需要事先知識，並在最後加上一個 "XD" 笑臉符號。
問題: {query_str}
回答: 
"""
)

custom_qa_prompts = PromptTemplate(qa_template)
query_engine = index.as_query_engine()
query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": custom_qa_prompts}
)
response = query_engine.query("補宿申請？")
print(response.response)