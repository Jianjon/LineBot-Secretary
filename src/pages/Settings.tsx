import React, { useState } from 'react';

const Settings: React.FC = () => {
  const [autoWeekly, setAutoWeekly] = useState(true);
  const [autoAsk, setAutoAsk] = useState(false);
  const [autoAssign, setAutoAssign] = useState(false);

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', padding: 24 }}>
      <h2>功能設定</h2>
      <div style={{ marginBottom: 16 }}>
        <label>
          <input type="checkbox" checked={autoWeekly} onChange={e => setAutoWeekly(e.target.checked)} />
          自動週報推播
        </label>
      </div>
      <div style={{ marginBottom: 16 }}>
        <label>
          <input type="checkbox" checked={autoAsk} onChange={e => setAutoAsk(e.target.checked)} />
          自動私訊補問
        </label>
      </div>
      <div style={{ marginBottom: 16 }}>
        <label>
          <input type="checkbox" checked={autoAssign} onChange={e => setAutoAssign(e.target.checked)} />
          任務自動分派
        </label>
      </div>
      <button style={{ padding: 8, width: 120 }}>儲存設定</button>
    </div>
  );
};

export default Settings; 