# LINE Bot 專案管理助手

這是一個基於 LINE Bot 的專案管理助手，使用 OpenAI GPT-4 提供智能對話和任務管理功能。

## 功能特點
- 智能任務管理
- 自動週報生成
- 任務到期提醒
- 專案進度追蹤
- 多語言支援
- 個人化設定

## 系統需求
- Python 3.8+
- LINE Bot 帳號
- OpenAI API 金鑰
- Supabase 資料庫

## 安裝步驟

### 克隆專案
```bash
git clone [專案網址]
cd [專案目錄]
```

### 安裝依賴
```bash
pip install -r requirements.txt
```

### 設定環境變數
在專案根目錄建立 `.env` 檔案：
```env
LINE_CHANNEL_ACCESS_TOKEN=你的LINE頻道存取權杖
LINE_CHANNEL_SECRET=你的LINE頻道密鑰
OPENAI_API_KEY=你的OpenAI API金鑰
SUPABASE_URL=你的Supabase URL
SUPABASE_KEY=你的Supabase金鑰
```

### 啟動服務
```bash
python app.py
```

## 使用說明

### 基本指令
- `/help` - 顯示幫助訊息
- `/tasks` - 查看任務列表
- `/report` - 生成週報
- `/settings` - 查看設定
- `/status` - 查看專案狀態

### 自然語言互動
- 新增任務：「新增一個任務：完成週報」
- 查詢進度：「目前的專案進度如何？」
- 更新狀態：「將任務A標記為已完成」

## 專案結構
```
.
├── app.py              # 主程式
├── requirements.txt    # 依賴套件
└── docs/              # 文件
    └── database.md    # 資料庫設計文件
```

## 開發說明

### 資料庫設計
詳細的資料庫結構請參考 `docs/database.md`。

### 錯誤處理
- 所有錯誤都會被記錄到日誌中
- 用戶會收到友善的錯誤提示
- 系統會自動重試失敗的操作

### 安全性
- 所有敏感資訊都存儲在環境變數中
- 使用 HTTPS 進行通訊
- 實作 LINE 簽名驗證

## 注意事項
- 請確保所有 API 金鑰都已正確設定
- 建議使用 virtualenv 進行開發
- 建議將 `.env` 檔案加入 `.gitignore`

## 貢獻
歡迎提議和貢獻！