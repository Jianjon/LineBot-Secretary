# API 配置文件

## 環境變數設定

### LINE Bot API
```env
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret
```

### OpenAI API
```env
OPENAI_API_KEY=your_openai_api_key
```

### Supabase
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## API 端點說明

### LINE Webhook
- 路徑：`/webhook`
- 方法：POST
- 用途：接收 LINE 訊息事件
- 驗證：使用 LINE Signature 驗證

### 定時任務
- 每日摘要：每天早上 9:00
- 週報：每週一早上 9:30

## 資料庫結構

### users
```sql
create table users (
  id uuid primary key default uuid_generate_v4(),
  line_id text unique not null,
  name text not null,
  department text,
  title text,
  joined_at timestamp default now()
);
```

### messages
```sql
create table messages (
  id uuid primary key default uuid_generate_v4(),
  sender_id uuid references users(id),
  message_text text not null,
  gpt_summary text,
  task_id uuid references tasks(id),
  created_at timestamp default now()
);
```

### tasks
```sql
create table tasks (
  id uuid primary key default uuid_generate_v4(),
  title text not null,
  description text,
  owner_id uuid references users(id),
  deadline date,
  status text default '進行中',
  related_flow_id uuid references task_flows(id),
  created_at timestamp default now(),
  updated_at timestamp
);
```

### task_flows
```sql
create table task_flows (
  id uuid primary key default uuid_generate_v4(),
  task_id uuid references tasks(id),
  step_number int not null,
  department text,
  handler_id uuid references users(id),
  status text default '未開始',
  updated_at timestamp default now()
);
```

### task_logs
```sql
create table task_logs (
  id uuid primary key default uuid_generate_v4(),
  task_id uuid references tasks(id),
  user_id uuid references users(id),
  action text,
  note text,
  created_at timestamp default now()
);
```

## 部署流程

1. 設置環境變數
2. 建立資料庫表格
3. 部署應用程式
4. 設定 LINE Webhook URL
5. 測試基本功能

## 監控與維護

### 日誌記錄
- 應用程式日誌
- 資料庫操作日誌
- 錯誤追蹤

### 效能監控
- API 響應時間
- 資料庫查詢效能
- 記憶體使用情況

### 備份策略
- 資料庫定期備份
- 設定檔備份
- 程式碼版本控制 