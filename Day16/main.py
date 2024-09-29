from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MAX_ITEMS = 10
DEFAULT_SKIP = 0

# 定義水果模型
class Fruit(BaseModel):
	name: str
	price: float
	
# 模擬資料庫
FRUIT_DATABASE: list[Fruit] = [
	Fruit(name="蘋果", price=10.0),
	Fruit(name="香蕉", price=5.0),
	Fruit(name="橘子", price=8.0),
	Fruit(name="芭樂", price=7.0),
	Fruit(name="西瓜", price=15.0),
	Fruit(name="梨子", price=6.0),
	Fruit(name="櫻桃", price=20.0),
	Fruit(name="葡萄", price=12.0),
	Fruit(name="橙子", price=9.0),
	Fruit(name="柚子", price=11.0),
]

app = FastAPI(
	title="水果 API",
	description="一個用來回傳水果資料的 API",
	version="1.0.0",
	servers=[
		{"url": "http://localhost:8000", "description": "本地伺服器"},
	]
)

@app.get("/", operation_id="get_welcome_message")
async def get_welcome_message() -> dict[str, str]:
	"""
	回傳歡迎訊息。
	
	Returns:
		Dict[str, str]: 包含歡迎訊息的字典。
	"""
	return {"message": "歡迎使用水果 API！"}

@app.get("/fruits/{fruit_id}", operation_id="get_fruit_by_id")
async def get_fruit_by_id(fruit_id: int) -> Fruit:
	"""
	根據 ID 取得特定水果的資訊。
	Args:
		fruit_id (int): 水果的 ID。
	Returns:
		Fruit: 對應 ID 的水果資訊。
	Raises:
		HTTPException: 如果找不到對應 ID 的水果，則拋出 404 錯誤。
	"""
	try:
		return FRUIT_DATABASE[fruit_id]
	except IndexError:
		raise HTTPException(status_code=404, detail="找不到指定 ID 的水果")
		
@app.get("/fruits/", operation_id="get_fruits")
async def get_fruits(skip: int = DEFAULT_SKIP, limit: int = MAX_ITEMS) -> list[Fruit]:
	"""
	取得水果列表
	Args:
		skip (int, optional): 要跳過的水果數量。默認為 0。
		limit (int, optional): 要返回的最大水果數量。默認為 10。
	Returns:
		List[Fruit]: 符合條件的水果列表。
	"""
	return FRUIT_DATABASE[skip : skip + limit]

if __name__ == "__main__":
	app.run()
	
# 使用 uvicorn main:app --reload --host=0.0.0.0 --port=8000 啟動伺服器