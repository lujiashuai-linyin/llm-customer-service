from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os
# 在文件顶部添加
import logging
from typing import List, Dict
from config import Config
from langchain.llms import LlamaCpp  # 新增导入

# 修改load_knowledge_base函数
if not os.path.exists("../docs/product_manual.md"):
    logging.warning("知识库文件不存在，将创建空向量库")
    # 创建空知识库逻辑
    with open("../docs/product_manual.md", "w", encoding="utf-8") as f:
        f.write("")

# 加载知识库
def load_knowledge_base():
    loader = TextLoader("../docs/product_manual.md", encoding="utf-8")
    documents = loader.load()

    # 文档分块（优化：根据标点符号智能拆分）
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=64,
        separators=["\n\n", "\n", "。", "！", "？"]
    )
    splits = text_splitter.split_documents(documents)

    # 初始化向量库（持久化到本地）
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    vectorstore.persist()
    return vectorstore


# 构建QA链
def build_qa_chain():
    vectorstore = load_knowledge_base()
    
    if Config.USE_LOCAL_LLM:
        # 本地模型配置
        llm = LlamaCpp(
            model_path=Config.LOCAL_LLM_MODEL_PATH,
            temperature=Config.LOCAL_LLM_TEMPERATURE,
            max_tokens=1024,
            n_ctx=2048
        )
    else:
        # 原有OpenAI配置
        llm = ChatOpenAI(
            model_name=Config.LLM_MODEL,
            temperature=0.3,
            max_tokens=1024
        )
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 3}  # 检索Top3相关文档
        ),
        return_source_documents=True  # 返回引用来源
    )