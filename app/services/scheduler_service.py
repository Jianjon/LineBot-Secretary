from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from app.services.database_service import get_weekly_tasks, get_user_tasks
from app.services.openai_service import generate_task_summary
from app.services.line_service import send_broadcast_message
import os

scheduler = BackgroundScheduler()

def setup_scheduler(line_bot_api):
    """
    設置定時任務
    """
    # 每天早上 9:00 發送每日任務摘要
    scheduler.add_job(
        send_daily_summary,
        CronTrigger(hour=9, minute=0),
        args=[line_bot_api],
        id='daily_summary'
    )
    
    # 每週一早上 9:30 發送週報
    scheduler.add_job(
        send_weekly_report,
        CronTrigger(day_of_week='mon', hour=9, minute=30),
        args=[line_bot_api],
        id='weekly_report'
    )
    
    scheduler.start()

def send_daily_summary(line_bot_api):
    """
    發送每日任務摘要
    """
    try:
        # 獲取昨天的任務
        yesterday = datetime.now() - timedelta(days=1)
        tasks = get_user_tasks(created_after=yesterday.isoformat())
        
        if tasks:
            summary = generate_task_summary(tasks)
            # 發送給所有相關人員
            for task in tasks:
                if task.get('assignee'):
                    send_broadcast_message(
                        line_bot_api,
                        task['assignee'],
                        f"📊 每日任務摘要\n\n{summary}"
                    )
    except Exception as e:
        print(f"Error sending daily summary: {e}")

def send_weekly_report(line_bot_api):
    """
    發送週報
    """
    try:
        tasks = get_weekly_tasks()
        if tasks:
            summary = generate_task_summary(tasks)
            # 發送給所有部門主管
            departments = set(task.get('department') for task in tasks if task.get('department'))
            for dept in departments:
                send_broadcast_message(
                    line_bot_api,
                    f"dept_{dept}",
                    f"📈 週報摘要\n\n{summary}"
                )
    except Exception as e:
        print(f"Error sending weekly report: {e}") 