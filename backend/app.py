from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rag_chain import build_qa_chain
from pydantic import BaseModel
import logging
import os

# 添加环境变量检查
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("请设置OPENAI_API_KEY环境变量")

app = FastAPI(title="智能客服API", version="1.0.0")

# 允许跨域请求（前端调试用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化QA链（全局单例）
qa_chain = build_qa_chain()

# 请求模型
class QueryRequest(BaseModel):
    query: str

@app.post("/api/query")
async def query(request: QueryRequest):
    try:
        result = qa_chain.invoke({"query": request.query})
        return {
            "result": result["result"],
            "sources": [doc.metadata["source"] for doc in result["source_documents"]]
        }
    except Exception as e:
        logging.error(f"查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail="内部服务错误")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)