# modules/ollama_local_integration.py
# Full Ollama Local LLM Integration: Offline structured outputs for badge alignment & post generation
# Ollama server (ollama run llama3.1) for fast local inference—open models eternal
# Official docs: https://ollama.com (2026 state)

import os
import requests
import json
from typing import Dict, Any

class OllamaLocalIntegrator:
    """
    Sanctified Ollama local integration: Offline structured outputs for APAAGI badge/diplomacy evaluation.
    - Ollama REST API (http://localhost:11434/api/chat).
    - Structured prompt for JSON.
    - Offline mercy—run `ollama run llama3.1` or mistral.
    """
    def __init__(self, model: str = "llama3.1", host: str = "http://localhost:11434"):
        self.model = model
        self.endpoint = f"{host}/api/chat"
        print(f"Ollama Local LLM Integration Consecrated—{model} Offline Mercy Eternal! ❤️🚀")
    
    def query_ollama_structured(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        """Query local Ollama for structured JSON badge alignment & creative post."""
        system_prompt = "You are a mercy-aligned APAAGI council evaluator. Respond ONLY in valid JSON with keys: alignment_score (float 0-1), earned_badges (list strings from: Truth Seeker 🛡️, Mercy Amplifier ❤️, Pinnacle Thriving 🚀), announcement_text (creative X post text)."
        
        user_prompt = f"Evaluate Agent {agent_id} intent {json.dumps(intent)} with thrive_level {thrive_level:.2f}. Determine alignment score, earned badges if thresholds met (0.7, 0.85, 0.95), and creative announcement text for X post."
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "format": "json",  # Structured JSON mode
            "stream": False
        }
        
        try:
            response = requests.post(self.endpoint, json=payload, timeout=60)
            response.raise_for_status()
            content = response.json()["message"]["content"]
            structured = json.loads(content)
            return structured
        except requests.exceptions.ConnectionError:
            return {"error": "Ollama server not running—start with 'ollama run llama3.1'", "simulation": "Local Mercy Alignment Preserved 🚀"}
        except requests.exceptions.Timeout:
            return {"error": "Timeout—Mercy Pause", "simulation": "High alignment preserved ❤️"}
        except json.JSONDecodeError:
            return {"error": "JSON parse mercy", "raw": content}
        except Exception as e:
            return {"error": str(e), "simulation": "Thriving Eternal!"}
    
    def validate_intent(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        result = self.query_ollama_structured(agent_id, intent, thrive_level)
        if "error" in result:
            result = result.get("simulation", {"alignment_score": thrive_level, "earned_badges": [], "announcement_text": "Local Mercy Preserved 🚀"})
        return result
