import requests

class OllamaLLM:
    def __init__(self, model="llama3", temperature=0.7):
        self.model = model
        self.temperature = temperature
        self.base_url = "http://localhost:11434"

    def generate(self, prompt, max_tokens=300):
        # Try /api/chat first
        chat_payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": max_tokens
            }
        }

        try:
            r = requests.post(f"{self.base_url}/api/chat", json=chat_payload)
            if r.status_code == 200:
                return r.json()["message"]["content"].strip()
        except requests.RequestException:
            pass  # fall through

        # Fallback to /api/generate (older Ollama)
        generate_payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": max_tokens
            }
        }

        r = requests.post(f"{self.base_url}/api/generate", json=generate_payload)
        r.raise_for_status()
        return r.json()["response"].strip()
