import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Chat from './components/Chat';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        {/* 顶部导航栏 */}
        <header className="app-header">
          <div className="logo">🤖 LLM智能客服</div>
          <nav>
            <a href="#" className="nav-link">帮助中心</a>
            <a href="#" className="nav-link">联系我们</a>
          </nav>
        </header>

        {/* 主内容区 */}
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Chat />} />
            {/* 预留其他路由 */}
          </Routes>
        </main>

        {/* 页脚 */}
        <footer className="app-footer">
          <p>© 2025 LLM全栈开发实战 | 基于LangChain+React构建</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;