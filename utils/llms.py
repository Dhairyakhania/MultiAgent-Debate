import requests

class OllamaLLM:
    def __init__(self, model="mistral", temperature=0.7):
        self.model = model
        self.temperature = temperature
        self.base_url = "http://localhost:11434"

    def generate(self, prompt, max_tokens=350):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": max_tokens,
                "repeat_penalty": 1.2
            }
        }

        r = requests.post(f"{self.base_url}/api/chat", json=payload)
        if r.status_code == 200:
            return r.json()["message"]["content"].strip()

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": max_tokens,
                "repeat_penalty": 1.2
            }
        }

        r = requests.post(f"{self.base_url}/api/generate", json=payload)
        r.raise_for_status()
        return r.json()["response"].strip()
