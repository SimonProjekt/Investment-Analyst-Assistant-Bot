import os
import requests

def send_telegram_message(chat_id: int, text: str):
    telegram_api_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(telegram_api_url, json=payload, headers=headers)
    print(f"Statuskod från Telegram API: {response.status_code}, Svar: {response.text}")

def send_typing_action(chat_id: int):
    telegram_api_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendChatAction"
    payload = {
        "chat_id": chat_id,
        "action": "typing"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(telegram_api_url, json=payload, headers=headers)
    print(f"Skickade 'typing' till användare: {chat_id}, status: {response.status_code}")
