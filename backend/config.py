import os

class Config:
    # 原有配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = "BAAI/bge-m3"
    LLM_MODEL = "gpt-3.5-turbo"
    
    # 新增本地模型配置
    USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
    LOCAL_LLM_MODEL_PATH = os.getenv("LOCAL_LLM_MODEL_PATH", "/path/to/local/model")
    LOCAL_LLM_TEMPERATURE = float(os.getenv("LOCAL_LLM_TEMPERATURE", "0.3"))
    CHROMA_DB_PATH = "./chroma_db"
    DOCS_PATH = "../docs/product_manual.md"