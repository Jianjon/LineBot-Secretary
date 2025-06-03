from supabase import create_client
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

# 設定日誌
logger = logging.getLogger(__name__)

# 初始化 Supabase 客戶端
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

class DatabaseError(Exception):
    """自定義資料庫錯誤"""
    pass

async def save_message(event) -> None:
    """
    保存 LINE 訊息到資料庫
    """
    try:
        data = {
            'message_id': event.message.id,
            'user_id': event.source.user_id,
            'group_id': event.source.group_id if hasattr(event.source, 'group_id') else None,
            'message_type': 'text',
            'content': event.message.text,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending',
            'context': {}
        }
        await supabase.table('messages').insert(data).execute()
    except Exception as e:
        logger.error(f"Error saving message: {e}")
        raise DatabaseError(f"Failed to save message: {str(e)}")

async def save_task(task_info: Dict[str, Any]) -> str:
    """
    保存任務到資料庫，返回任務ID
    """
    try:
        data = {
            'title': task_info.get('title', ''),
            'description': task_info.get('description'),
            'assignee': task_info.get('assignee'),
            'department': task_info.get('department'),
            'due_date': task_info.get('due_date'),
            'priority': task_info.get('priority', 'medium'),
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        response = await supabase.table('tasks').insert(data).execute()
        return response.data[0]['id']
    except Exception as e:
        logger.error(f"Error saving task: {e}")
        raise DatabaseError(f"Failed to save task: {str(e)}")

def save_task_flow(task_id: str, flow_steps: List[Dict[str, Any]]) -> None:
    """
    保存任務流程
    """
    try:
        for i, step in enumerate(flow_steps):
            data = {
                'task_id': task_id,
                'step_number': i + 1,
                'department': step.get('department'),
                'handler_id': step.get('handler_id'),
                'status': '待處理',
                'created_at': datetime.now().isoformat()
            }
            supabase.table('task_flows').insert(data).execute()
    except Exception as e:
        print(f"Error saving task flow: {e}")

def save_user(user_info: Dict[str, Any]) -> None:
    """
    保存使用者資訊
    """
    try:
        data = {
            'line_id': user_info.get('line_id'),
            'name': user_info.get('name'),
            'department': user_info.get('department'),
            'title': user_info.get('title'),
            'join_date': datetime.now().isoformat()
        }
        supabase.table('users').insert(data).execute()
    except Exception as e:
        print(f"Error saving user: {e}")

async def get_user_tasks(
    status: str = None,
    keyword: str = None,
    assignee: str = None,
    department: str = None,
    created_after: str = None
) -> List[Dict[str, Any]]:
    """
    獲取任務列表，支援多種篩選條件
    """
    try:
        query = supabase.table('tasks').select('*')
        
        if status:
            query = query.eq('status', status)
        if keyword:
            query = query.ilike('description', f'%{keyword}%')
        if assignee:
            query = query.eq('assignee', assignee)
        if department:
            query = query.eq('department', department)
        if created_after:
            query = query.gte('created_at', created_after)
            
        response = await query.execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        raise DatabaseError(f"Failed to get tasks: {str(e)}")

async def get_weekly_tasks() -> List[Dict[str, Any]]:
    """
    獲取本週的任務
    """
    try:
        start_date = (datetime.now() - timedelta(days=7)).isoformat()
        response = await supabase.table('tasks')\
            .select('*')\
            .gte('created_at', start_date)\
            .execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting weekly tasks: {e}")
        raise DatabaseError(f"Failed to get weekly tasks: {str(e)}")

def get_task_flow(task_id: str) -> List[Dict[str, Any]]:
    """
    獲取任務流程
    """
    try:
        response = supabase.table('task_flows')\
            .select('*')\
            .eq('task_id', task_id)\
            .order('step_number')\
            .execute()
        return response.data
    except Exception as e:
        print(f"Error getting task flow: {e}")
        return []

async def update_task_status(task_id: str, status: str, user_id: str) -> None:
    """
    更新任務狀態並記錄日誌
    """
    try:
        # 更新任務狀態
        await supabase.table('tasks')\
            .update({
                'status': status,
                'updated_at': datetime.now().isoformat()
            })\
            .eq('id', task_id)\
            .execute()
        
        # 記錄日誌
        log_data = {
            'task_id': task_id,
            'user_id': user_id,
            'action': f'更新狀態為 {status}',
            'timestamp': datetime.now().isoformat()
        }
        await supabase.table('task_logs').insert(log_data).execute()
    except Exception as e:
        logger.error(f"Error updating task status: {e}")
        raise DatabaseError(f"Failed to update task status: {str(e)}")

def get_user_info(line_id: str) -> Optional[Dict[str, Any]]:
    """
    獲取使用者資訊
    """
    try:
        response = supabase.table('users')\
            .select('*')\
            .eq('line_id', line_id)\
            .execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None

async def get_user_settings(user_id: str) -> Dict[str, Any]:
    """
    獲取用戶設定
    """
    try:
        response = await supabase.table('settings')\
            .select('*')\
            .eq('user_id', user_id)\
            .execute()
        return response.data[0] if response.data else {
            'notification_enabled': True,
            'language': 'zh-TW'
        }
    except Exception as e:
        logger.error(f"Error getting user settings: {e}")
        raise DatabaseError(f"Failed to get user settings: {str(e)}")

async def update_user_settings(user_id: str, settings: Dict[str, Any]) -> None:
    """
    更新用戶設定
    """
    try:
        await supabase.table('settings')\
            .upsert({
                'user_id': user_id,
                **settings,
                'updated_at': datetime.now().isoformat()
            })\
            .execute()
    except Exception as e:
        logger.error(f"Error updating user settings: {e}")
        raise DatabaseError(f"Failed to update user settings: {str(e)}") 