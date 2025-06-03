# 資料庫設計

## 資料表結構

### 1. messages 表
```sql
create table messages (
    id uuid default uuid_generate_v4() primary key,
    user_id text not null,
    message text not null,
    response text not null,
    timestamp timestamp with time zone default now(),
    status text default 'pending',
    context jsonb default '{}',
    created_at timestamp with time zone default now()
);

-- 建立索引
create index idx_messages_user_timestamp on messages(user_id, timestamp);
create index idx_messages_status on messages(status);
```

### 2. tasks 表
```sql
create table tasks (
    id uuid default uuid_generate_v4() primary key,
    title text not null,
    description text,
    status text default 'pending',
    priority text default 'medium',
    assigned_to text,
    due_date timestamp with time zone,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- 建立索引
create index idx_tasks_status on tasks(status);
create index idx_tasks_priority on tasks(priority);
create index idx_tasks_assigned_to on tasks(assigned_to);
```

### 3. settings 表
```sql
create table settings (
    id uuid default uuid_generate_v4() primary key,
    user_id text not null unique,
    notification_enabled boolean default true,
    language text default 'zh-TW',
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- 建立索引
create index idx_settings_user_id on settings(user_id);
```

## 資料表關聯
- tasks 表可以與 messages 表建立關聯，追蹤任務相關對話
- settings 表與 messages 表通過 user_id 建立關聯 