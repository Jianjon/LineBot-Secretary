import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Message {
  id?: string;
  timestamp: string;
  user_id: string;
  content: string;
  ai_result?: any;
}

const Messages: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/messages')
      .then(res => setMessages(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div style={{ maxWidth: 900, margin: '2rem auto', padding: 24 }}>
      <h2>訊息查詢</h2>
      {loading ? <p>載入中...</p> : null}
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>時間</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>用戶</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>內容</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>AI 標記</th>
          </tr>
        </thead>
        <tbody>
          {messages.map(msg => (
            <tr key={msg.id || msg.timestamp + msg.user_id}>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>{msg.timestamp}</td>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>{msg.user_id}</td>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>{msg.content}</td>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>{msg.ai_result ? (msg.ai_result.is_task ? '任務' : '一般訊息') : ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Messages; 