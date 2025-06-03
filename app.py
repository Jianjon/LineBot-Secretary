from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import json
import logging
from datetime import datetime, timedelta
import asyncio
from typing import Dict, Optional
import openai
from supabase import create_client, Client
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 FastAPI
app = FastAPI()

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 LINE Bot
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 初始化 OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# 初始化 Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# 用戶上下文快取
user_contexts: Dict[str, Dict] = {}

# 系統提示詞
SYSTEM_PROMPT = """你是一個專案管理助手，負責：
1. 理解用戶的任務需求
2. 管理專案進度
3. 提供週報摘要
4. 回答專案相關問題

請用繁體中文回覆，保持專業且友善的語氣。

支援的指令：
/help - 顯示幫助訊息
/tasks - 查看任務列表
/report - 生成週報
/settings - 查看設定
/status - 查看專案狀態"""

# 相關性判斷提示詞
RELEVANCE_PROMPT = """請判斷以下訊息是否與專案管理、任務追蹤、進度報告等相關。
請只回答 'yes' 或 'no'。

相關的內容包括：
- 任務新增、修改、查詢
- 專案進度追蹤
- 週報生成
- 任務提醒
- 專案相關問題諮詢
- 指令操作（/help, /tasks 等）

不相關的內容包括：
- 一般聊天
- 私人問題
- 與專案無關的詢問
- 其他非工作相關話題"""

async def get_user_settings(user_id: str) -> dict:
    """獲取用戶設定"""
    try:
        response = await supabase.table("settings").select("*").eq("user_id", user_id).execute()
        if response.data:
            return response.data[0]
        return {"notification_enabled": True, "language": "zh-TW"}
    except Exception as e:
        logger.error(f"Error getting user settings: {e}")
        return {"notification_enabled": True, "language": "zh-TW"}

async def is_relevant_message(message: str) -> bool:
    """判斷訊息是否與專案管理相關"""
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": RELEVANCE_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.3,
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip().lower()
        return result == 'yes'
    except Exception as e:
        logger.error(f"Error checking message relevance: {e}")
        return True  # 發生錯誤時預設為相關，避免遺漏重要訊息

async def handle_command(message: str, user_id: str) -> Optional[dict]:
    """處理指令"""
    commands = {
        '/help': lambda: {"type": "success", "content": "📋 可用指令：\n/tasks - 查看任務列表\n/report - 生成週報\n/settings - 查看設定\n/status - 查看專案狀態"},
        '/tasks': lambda: get_user_tasks(),
        '/report': lambda: generate_weekly_report(),
        '/settings': lambda: get_user_settings(user_id),
        '/status': lambda: get_project_status()
    }
    
    if message in commands:
        try:
            return await commands[message]()
        except Exception as e:
            logger.error(f"Error handling command {message}: {e}")
            return {"type": "error", "content": f"執行指令 {message} 時發生錯誤"}
    
    return None

async def get_project_status() -> dict:
    """獲取專案狀態"""
    try:
        tasks = await get_user_tasks()
        total = len(tasks)
        completed = sum(1 for task in tasks if task['status'] == 'completed')
        pending = sum(1 for task in tasks if task['status'] == 'pending')
        
        return {
            "type": "success",
            "content": f"📊 專案狀態\n\n總任務數：{total}\n已完成：{completed}\n進行中：{pending}\n完成率：{(completed/total*100 if total > 0 else 0):.1f}%"
        }
    except Exception as e:
        logger.error(f"Error getting project status: {e}")
        return {"type": "error", "content": "獲取專案狀態時發生錯誤"}

async def analyze_message(message: str, user_id: str, context: Optional[Dict] = None) -> dict:
    """分析用戶訊息"""
    try:
        # 檢查是否為指令
        command_result = await handle_command(message, user_id)
        if command_result:
            return command_result
        
        # 判斷訊息相關性
        is_relevant = await is_relevant_message(message)
        if not is_relevant:
            return {
                "type": "irrelevant",
                "content": "抱歉，我主要負責專案管理相關事務。如果您有任務管理、進度追蹤等需求，我很樂意為您服務。"
            }
        
        # 獲取用戶設定
        settings = await get_user_settings(user_id)
        
        # 準備上下文
        if context is None:
            context = {}
        
        # 調用 OpenAI API
        response = await openai.ChatCompletion.acreate(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        
        if not result:
            return {"type": "error", "content": "抱歉，我無法理解，請再試一次。"}
        
        return {"type": "success", "content": result}
    except Exception as e:
        logger.error(f"Error analyzing message: {e}")
        return {"type": "error", "content": "抱歉，發生錯誤，請稍後再試。"}

async def log_message(user_id: str, message: str, response: str, status: str = "processed", context: Optional[Dict] = None):
    """記錄訊息"""
    try:
        await supabase.table("messages").insert({
            "user_id": user_id,
            "message": message,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "context": context or {}
        }).execute()
    except Exception as e:
        logger.error(f"Error logging message: {e}")

async def check_tasks_due():
    """檢查即將到期的任務"""
    try:
        # 獲取所有未完成的任務
        response = await supabase.table("tasks").select("*").eq("status", "pending").execute()
        tasks = response.data
        
        for task in tasks:
            if task.get("due_date"):
                due_date = datetime.fromisoformat(task["due_date"])
                if due_date - datetime.now() < timedelta(days=1):
                    # 發送提醒
                    await line_bot_api.push_message(
                        task["assigned_to"],
                        TextSendMessage(text=f"提醒：任務「{task['title']}」即將在24小時內到期！")
                    )
    except Exception as e:
        logger.error(f"Error checking tasks due: {e}")

async def generate_weekly_report():
    """生成週報"""
    try:
        # 獲取過去一週的任務
        last_week = datetime.now() - timedelta(days=7)
        response = await supabase.table("tasks").select("*").gte("created_at", last_week.isoformat()).execute()
        tasks = response.data
        
        # 生成週報
        report = "📊 本週專案進度報告\n\n"
        report += f"總任務數：{len(tasks)}\n"
        completed = sum(1 for task in tasks if task["status"] == "completed")
        report += f"已完成：{completed}\n"
        report += f"進行中：{len(tasks) - completed}\n\n"
        
        # 發送週報
        await line_bot_api.broadcast(TextSendMessage(text=report))
    except Exception as e:
        logger.error(f"Error generating weekly report: {e}")

@app.post("/webhook")
async def line_webhook(request: Request):
    """處理 LINE Webhook"""
    try:
        signature = request.headers["X-Line-Signature"]
        body = await request.body()
        
        try:
            handler.handle(body.decode(), signature)
        except InvalidSignatureError:
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@handler.add(MessageEvent, message=TextMessage)
async def handle_message(event):
    """處理文字訊息"""
    try:
        user_id = event.source.user_id
        message = event.message.text
        
        # 獲取用戶上下文
        context = user_contexts.get(user_id, {})
        
        # 分析訊息
        result = await analyze_message(message, user_id, context)
        
        # 更新上下文
        user_contexts[user_id] = {
            "last_message": message,
            "last_response": result["content"],
            "timestamp": datetime.now().isoformat()
        }
        
        # 記錄訊息
        await log_message(user_id, message, result["content"], "processed", context)
        
        # 回覆訊息
        await line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result["content"])
        )
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="抱歉，發生錯誤，請稍後再試。")
        )

# 定時任務
@app.on_event("startup")
async def startup_event():
    """啟動定時任務"""
    asyncio.create_task(run_scheduled_tasks())

async def run_scheduled_tasks():
    """執行定時任務"""
    while True:
        try:
            # 檢查任務到期
            await check_tasks_due()
            
            # 每週一早上9點生成週報
            now = datetime.now()
            if now.weekday() == 0 and now.hour == 9:
                await generate_weekly_report()
            
            # 每小時執行一次
            await asyncio.sleep(3600)
        except Exception as e:
            logger.error(f"Error in scheduled tasks: {e}")
            await asyncio.sleep(60)  # 發生錯誤時等待1分鐘後重試

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 