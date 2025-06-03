import React, { useState } from 'react';

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: 串接後端 API 驗證
    if (username === 'admin' && password === 'password') {
      window.location.href = '/admin';
    } else {
      setError('帳號或密碼錯誤');
    }
  };

  return (
    <div style={{ maxWidth: 320, margin: '3rem auto', padding: 24, border: '1px solid #ccc', borderRadius: 8 }}>
      <h2>管理者登入</h2>
      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: 12 }}>
          <input
            type="text"
            placeholder="帳號"
            value={username}
            onChange={e => setUsername(e.target.value)}
            style={{ width: '100%', padding: 8 }}
          />
        </div>
        <div style={{ marginBottom: 12 }}>
          <input
            type="password"
            placeholder="密碼"
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={{ width: '100%', padding: 8 }}
          />
        </div>
        {error && <div style={{ color: 'red', marginBottom: 12 }}>{error}</div>}
        <button type="submit" style={{ width: '100%', padding: 8 }}>登入</button>
      </form>
    </div>
  );
};

export default LoginPage; 