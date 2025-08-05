## 🐳 Docker 部署

### 前置要求
- 已安装 Docker 和 Docker Compose
- 设置 OPENAI_API_KEY 环境变量

### 启动全栈服务
```bash
export OPENAI_API_KEY=your_api_key
docker-compose up --build
```

### 服务访问
- 后端API: http://localhost:8000
- 前端应用: http://localhost:3000

### 常用命令
- 后台运行: `docker-compose up -d`
- 停止服务: `docker-compose down`
- 查看日志: `docker-compose logs -f`

## 🔧 开发环境

### 后端启动
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

### 前端启动
```bash
cd frontend
npm install
npm start
```

## 📝 其他补充

### 环境变量
| 变量名 | 说明 |
|--------|------|
| OPENAI_API_KEY | OpenAI API密钥 |
| EMBEDDING_MODEL | 嵌入模型名称 (默认: BAAI/bge-m3) |

### 项目结构
```
llm-customer-service/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── rag_chain.py
│   │   ├── config.py
│   │   ├── logging.conf
│   ├── requirements.txt
│   ├── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
