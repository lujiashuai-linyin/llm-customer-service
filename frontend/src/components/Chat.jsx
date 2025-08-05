import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './Chat.css';

// 创建API实例
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 15000, // 15秒超时
  headers: { 'Content-Type': 'application/json' }
});

const Chat = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: '您好！我是智能客服助手，有什么可以帮您？' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // 自动滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      // 调用后端API
      const response = await api.post('/query', { query: input });

      // 处理成功响应
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `${response.data.result}\n\n参考来源: ${response.data.sources.join(', ')}`
      }]);
    } catch (error) {
      // 错误处理
      console.error('API请求失败:', error);
      const errorMsg = error.response?.status === 500
        ? '服务器内部错误，请稍后重试'
        : '请求超时，请检查网络连接';

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: errorMsg
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="avatar">{msg.role === 'user' ? '👤' : '🤖'}</div>
            <div className="content">{msg.content}</div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant loading">
            <div className="avatar">🤖</div>
            <div className="content">正在思考，请稍候...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSend()}
          placeholder="请输入您的问题..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>
          {isLoading ? '发送中...' : '发送'}
        </button>
      </div>
    </div>
  );
};

export default Chat;