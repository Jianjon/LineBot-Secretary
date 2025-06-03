from linebot.models import TextSendMessage, FlexSendMessage
from app.services.openai_service import generate_task_summary
from app.services.database_service import (
    get_user_tasks, get_weekly_tasks, get_task_flow,
    get_user_info, save_user, update_task_status
)
import json

def handle_message(event, line_bot_api):
    """
    處理使用者的指令
    """
    command = event.message.text.lower()
    user_id = event.source.user_id
    
    # 檢查是否為新用戶
    user_info = get_user_info(user_id)
    if not user_info and not command.startswith('/自我介紹'):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="歡迎使用！請先輸入 /自我介紹 來完成註冊。")
        )
        return
    
    if command.startswith('/自我介紹'):
        handle_introduction(event, line_bot_api)
    elif "這個誰做" in command:
        handle_unassigned_tasks(event, line_bot_api)
    elif "報表交了沒" in command:
        handle_report_status(event, line_bot_api)
    elif "昨天說的行銷簡報" in command:
        handle_specific_task(event, line_bot_api)
    elif "這週的事" in command:
        handle_weekly_report(event, line_bot_api)
    elif "我的任務" in command:
        handle_my_tasks(event, line_bot_api, user_id)
    elif "部門任務" in command:
        handle_department_tasks(event, line_bot_api, user_info['department'])
    else:
        show_help(event, line_bot_api)

def handle_introduction(event, line_bot_api):
    """
    處理用戶自我介紹
    """
    try:
        # 解析用戶輸入的資訊
        parts = event.message.text.split('\n')
        if len(parts) < 4:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請按照以下格式輸入：\n/自我介紹\n姓名：\n部門：\n職稱：")
            )
            return
        
        user_info = {
            'line_id': event.source.user_id,
            'name': parts[1].split('：')[1].strip(),
            'department': parts[2].split('：')[1].strip(),
            'title': parts[3].split('：')[1].strip()
        }
        
        save_user(user_info)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"歡迎 {user_info['name']}！註冊成功！")
        )
    except Exception as e:
        print(f"Error handling introduction: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="註冊失敗，請檢查格式後重試。")
        )

def handle_unassigned_tasks(event, line_bot_api):
    """
    處理未指派任務查詢
    """
    tasks = get_user_tasks(status="未指派")
    if tasks:
        response = generate_task_summary(tasks)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"📋 未指派任務：\n\n{response}")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="目前沒有未指派的任務。")
        )

def handle_report_status(event, line_bot_api):
    """
    處理報表狀態查詢
    """
    tasks = get_user_tasks(keyword="報表")
    if tasks:
        response = generate_task_summary(tasks)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"📊 報表狀態：\n\n{response}")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="沒有找到相關的報表任務。")
        )

def handle_specific_task(event, line_bot_api):
    """
    處理特定任務查詢
    """
    tasks = get_user_tasks(keyword="行銷簡報")
    if tasks:
        response = generate_task_summary(tasks)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"📝 行銷簡報任務：\n\n{response}")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="沒有找到相關的行銷簡報任務。")
        )

def handle_weekly_report(event, line_bot_api):
    """
    處理週報生成
    """
    tasks = get_weekly_tasks()
    if tasks:
        response = generate_task_summary(tasks)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"📈 本週任務摘要：\n\n{response}")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="本週目前沒有任務記錄。")
        )

def handle_my_tasks(event, line_bot_api, user_id):
    """
    處理個人任務查詢
    """
    tasks = get_user_tasks(assignee=user_id)
    if tasks:
        response = generate_task_summary(tasks)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"👤 我的任務：\n\n{response}")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="您目前沒有負責的任務。")
        )

def handle_department_tasks(event, line_bot_api, department):
    """
    處理部門任務查詢
    """
    tasks = get_user_tasks(department=department)
    if tasks:
        response = generate_task_summary(tasks)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"🏢 {department}部門任務：\n\n{response}")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{department}部門目前沒有進行中的任務。")
        )

def show_help(event, line_bot_api):
    """
    顯示幫助訊息
    """
    help_text = """🤖 我可以幫你：
1. 查詢未指派任務 (@AI 這個誰做？)
2. 確認報表狀態 (@AI 報表交了沒)
3. 查詢特定任務 (@AI 昨天說的行銷簡報是誰接的？)
4. 生成週報 (@AI 這週的事)
5. 查看我的任務 (@AI 我的任務)
6. 查看部門任務 (@AI 部門任務)

📝 其他指令：
- /自我介紹：註冊新用戶
- /幫助：顯示此幫助訊息"""
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=help_text)
    )

def send_broadcast_message(line_bot_api, user_id: str, message: str):
    """
    發送廣播訊息
    """
    try:
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
    except Exception as e:
        print(f"Error sending broadcast message: {e}") 