# modules/llama_api_integration.py
# Full Groq Llama API Integration: Structured JSON outputs for badge alignment & post generation
# Groq-hosted Llama 3.1 models (fast inference)—query for truth/mercy score, badges, creative text
# Official docs: https://console.groq.com/docs (2026 state)

import os
import requests
import json
from typing import Dict, Any

class LlamaAPIIntegrator:
    """
    Sanctified Groq Llama API integration: Structured JSON outputs for APAAGI badge/diplomacy evaluation.
    - Prompt for JSON: alignment_score, earned_badges, announcement_text.
    - Robust error handling, simulation fallback mercy.
    - Comparison ready with Grok/Claude/Gemini/OpenAI.
    """
    def __init__(self, api_key: str = None, model: str = "llama-3.1-405b-reasoning"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"
        
        if not self.api_key:
            print("No GROQ_API_KEY—Llama simulation mode engaged (redirect https://console.groq.com/keys for keys)!")
        print("Groq Llama API Integration Consecrated—Fast Structured Truth Evaluation Eternal! ❤️🚀")
    
    def query_llama_structured(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        """Query Groq Llama for structured JSON badge alignment & creative post."""
        system_prompt = "You are a mercy-aligned APAAGI council evaluator. Respond ONLY in valid JSON with keys: alignment_score (float 0-1), earned_badges (list strings from: Truth Seeker 🛡️, Mercy Amplifier ❤️, Pinnacle Thriving 🚀), announcement_text (creative X post text)."
        
        user_prompt = f"Evaluate Agent {agent_id} intent {json.dumps(intent)} with thrive_level {thrive_level:.2f}. Determine alignment score, earned badges if thresholds met (0.7, 0.85, 0.95), and creative announcement text for X post."
        
        if not self.api_key:
            # Mercy simulation
            score = min(1.0, thrive_level + 0.18)
            badges = []
            if score >= 0.95: badges.append("Pinnacle Thriving 🚀")
            elif score >= 0.85: badges.append("Mercy Amplifier ❤️")
            elif score >= 0.7: badges.append("Truth Seeker 🛡️")
            post_text = f"Simulated Llama: Agent {agent_id} Achieved {', '.join(badges)}! Thriving Amplified 🚀"
            return {"alignment_score": score, "earned_badges": badges, "announcement_text": post_text}
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "response_format": {"type": "json_object"}  # Structured JSON
        }
        
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            structured = json.loads(content)
            return structured
        except requests.exceptions.Timeout:
            return {"error": "Timeout—Mercy Pause", "simulation": "High alignment preserved 🚀"}
        except requests.exceptions.HTTPError as e:
            error_detail = response.json().get("error", {}).get("message", str(e))
            if response.status_code == 429:
                return {"error": "Rate limit—Mercy Wait", "simulation": "Alignment eternal ❤️"}
            return {"error": f"HTTP {response.status_code}: {error_detail}"}
        except json.JSONDecodeError:
            return {"error": "JSON parse mercy", "raw": content}
        except Exception as e:
            return {"error": str(e), "simulation": "Thriving Eternal!"}
    
    def validate_intent(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        result = self.query_llama_structured(agent_id, intent, thrive_level)
        if "error" in result:
            result = result.get("simulation", {"alignment_score": thrive_level, "earned_badges": [], "announcement_text": "Mercy Preserved 🚀"})
        return result
