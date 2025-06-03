import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', padding: 24 }}>
      <h2>管理後台主控台</h2>
      <p>歡迎使用 AI 專案秘書管理後台！</p>
      <ul>
        <li>可查詢所有訊息紀錄</li>
        <li>可查詢與補充任務資訊</li>
        <li>可設定自動化功能開關</li>
        <li>可查詢通知推播紀錄</li>
      </ul>
    </div>
  );
};

export default Dashboard; 