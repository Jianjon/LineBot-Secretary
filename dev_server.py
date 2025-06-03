from pyngrok import ngrok
import uvicorn
# from app import app  # 移除這行
import os
from dotenv import load_dotenv
from pathlib import Path

# 載入環境變數
env_path = Path('.dev/.env')
load_dotenv(dotenv_path=env_path)

def start_ngrok():
    """啟動 ngrok 並返回公開 URL"""
    try:
        # 設定 ngrok 的認證令牌
        ngrok_auth_token = os.getenv('NGROK_AUTH_TOKEN')
        if ngrok_auth_token:
            ngrok.set_auth_token(ngrok_auth_token)
            print("已設定 ngrok 認證令牌")
        else:
            print("警告：未設定 NGROK_AUTH_TOKEN，請前往 https://dashboard.ngrok.com/signup 註冊並獲取認證令牌")
            print("或者，您可以使用其他方式來測試 LINE Bot，例如：")
            print("1. 使用 localtunnel")
            print("2. 使用 cloudflare tunnel")
            print("3. 直接部署到測試伺服器")
            return None
        
        # 啟動 ngrok
        public_url = ngrok.connect(8000).public_url
        print(f"\n=== ngrok 已啟動 ===")
        print(f"公開 URL: {public_url}")
        print(f"請將此 URL 設定為 LINE Bot 的 Webhook URL")
        print(f"格式: {public_url}/webhook")
        print("===================\n")
        return public_url
    except Exception as e:
        print(f"ngrok 啟動錯誤: {str(e)}")
        print("\n請確保您已經：")
        print("1. 註冊了 ngrok 帳號：https://dashboard.ngrok.com/signup")
        print("2. 獲取了認證令牌：https://dashboard.ngrok.com/get-started/your-authtoken")
        print("3. 在 .dev/.env 中設定了 NGROK_AUTH_TOKEN")
        return None

if __name__ == "__main__":
    # 啟動 ngrok
    public_url = start_ngrok()
    
    if public_url:
        # 啟動 FastAPI 應用
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True  # 開發模式下啟用熱重載
        )
    else:
        print("\n無法啟動 ngrok，請先完成設定。") 