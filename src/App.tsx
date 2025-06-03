import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import Messages from './pages/Messages';
import Tasks from './pages/Tasks';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <div>
        <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
          <Link to="/admin" style={{ marginRight: 16 }}>主控台</Link>
          <Link to="/admin/messages" style={{ marginRight: 16 }}>訊息查詢</Link>
          <Link to="/admin/tasks" style={{ marginRight: 16 }}>任務查詢</Link>
          <Link to="/admin/settings">功能設定</Link>
        </nav>
        <Routes>
          <Route path="/admin/login" element={<LoginPage />} />
          <Route path="/admin/messages" element={<Messages />} />
          <Route path="/admin/tasks" element={<Tasks />} />
          <Route path="/admin/settings" element={<Settings />} />
          <Route path="/admin" element={<Dashboard />} />
          <Route path="*" element={<Navigate to="/admin/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
