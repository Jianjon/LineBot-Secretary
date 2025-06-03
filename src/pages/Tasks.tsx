import React from 'react';

const Tasks: React.FC = () => {
  return (
    <div style={{ maxWidth: 900, margin: '2rem auto', padding: 24 }}>
      <h2>任務查詢與補充</h2>
      <p>這裡將顯示所有任務（可標記資訊不全、人工補充）。</p>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>任務描述</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>負責人</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>截止日</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>狀態</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>操作</th>
          </tr>
        </thead>
        <tbody>
          {/* 之後這裡會用 map 動態產生資料列 */}
          <tr>
            <td style={{ border: '1px solid #ccc', padding: 8 }}>交報告</td>
            <td style={{ border: '1px solid #ccc', padding: 8 }}>（缺負責人）</td>
            <td style={{ border: '1px solid #ccc', padding: 8 }}>2024-06-05</td>
            <td style={{ border: '1px solid #ccc', padding: 8 }}>待補充</td>
            <td style={{ border: '1px solid #ccc', padding: 8 }}><button>補充</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default Tasks; 