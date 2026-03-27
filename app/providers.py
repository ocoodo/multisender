from abc import ABC, abstractmethod
from pathlib import Path
import json
import httpx


class BaseProvider(ABC):
    @abstractmethod
    async def send(self, text: str) -> bool:
        pass


class TelegramProvider(BaseProvider):
    name = 'telegram'
    
    def __init__(self, token: str, chat_id: str):
        self.chat_id = chat_id
        self.api_url = f'https://api.telegram.org/bot{token}/sendMessage'
        
    async def send(self, text: str) -> bool:
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.api_url, json=payload)
                if response.status_code != 200:
                    data = response.json()
                    print(f"Error: {data}")
                    return False
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False
            

class Multisender:
    def __init__(self):
        self.config_path = Path(__file__).resolve().parent.parent / 'config.json'
        self._load_config()
        self._load_providers()
    
    def _load_config(self):
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
    
    def _load_providers(self):
        self.providers = []
        for provider, config in self.config.get('providers', {}).items():
            if provider == 'telegram':
                token, chat_id = config['token'], config['chat_id']
                self.providers.append(TelegramProvider(
                    token=token,
                    chat_id=chat_id
                ))
                continue
    
    async def send_all(self, text: str):
        results = {}
        for provider in self.providers:
            result = await provider.send(text)
            results[provider.name] = result
        return results
