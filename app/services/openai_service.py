from openai import OpenAI
import os
from typing import Optional, Dict, Any

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def analyze_message(message: str) -> Optional[Dict[str, Any]]:
    """
    分析訊息是否包含任務，並提取相關資訊
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一個任務分析專家，負責從對話中識別出任務相關資訊。"},
                {"role": "user", "content": f"請分析以下訊息是否包含任務，如果是，請提取：任務描述、負責人、截止日期、優先級。如果不是任務，請回覆 null。\n\n訊息：{message}"}
            ],
            functions=[{
                "name": "extract_task",
                "description": "提取任務相關資訊",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "is_task": {"type": "boolean"},
                        "description": {"type": "string"},
                        "assignee": {"type": "string"},
                        "due_date": {"type": "string"},
                        "priority": {"type": "string", "enum": ["高", "中", "低"]}
                    },
                    "required": ["is_task"]
                }
            }],
            function_call={"name": "extract_task"}
        )
        
        result = response.choices[0].message.function_call.arguments
        return eval(result) if result else None
        
    except Exception as e:
        print(f"Error analyzing message: {e}")
        return None

def generate_task_summary(tasks: list) -> str:
    """
    生成任務摘要報告
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一個專業的專案管理助手，負責生成任務摘要報告。"},
                {"role": "user", "content": f"請根據以下任務列表生成一份摘要報告：\n\n{tasks}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "無法生成摘要報告" 