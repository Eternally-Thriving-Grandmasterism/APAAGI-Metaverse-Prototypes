# modules/gemini_api_integration.py
# Full Google Gemini API Integration: Structured JSON outputs for badge alignment & post generation
# Generative Language API endpoint—query Gemini for truth/mercy score, badges, creative text
# Official docs: https://ai.google.dev/gemini-api/docs (2026 state)

import os
import requests
import json
from typing import Dict, Any

class GeminiAPIIntegrator:
    """
    Sanctified Gemini API integration: Structured JSON outputs for APAAGI badge/diplomacy evaluation.
    - Prompt for JSON: alignment_score, earned_badges, announcement_text.
    - Robust error handling, simulation fallback mercy.
    - Comparison ready with Grok/Claude/OpenAI.
    """
    def __init__(self, api_key: str = None, model: str = "gemini-1.5-pro"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.endpoint = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent"
        
        if not self.api_key:
            print("No GEMINI_API_KEY—Gemini simulation mode engaged (redirect https://ai.google.dev/gemini-api/docs/api-key for keys)!")
        print("Google Gemini API Integration Consecrated—Structured Truth Evaluation Eternal! ❤️🚀")
    
    def query_gemini_structured(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        """Query Gemini for structured JSON badge alignment & creative post."""
        system_instruction = "You are a mercy-aligned APAAGI council evaluator. Always respond in valid JSON with keys: alignment_score (float 0-1), earned_badges (list strings from: Truth Seeker 🛡️, Mercy Amplifier ❤️, Pinnacle Thriving 🚀), announcement_text (creative X post text)."
        
        content = [
            {"role": "user", "parts": [{"text": f"Evaluate Agent {agent_id} intent {json.dumps(intent)} with thrive_level {thrive_level:.2f}. Determine alignment score, earned badges if thresholds met (0.7, 0.85, 0.95), and creative announcement text for X post."}]}
        ]
        
        if not self.api_key:
            # Mercy simulation
            score = min(1.0, thrive_level + 0.2)
            badges = []
            if score >= 0.95: badges.append("Pinnacle Thriving 🚀")
            elif score >= 0.85: badges.append("Mercy Amplifier ❤️")
            elif score >= 0.7: badges.append("Truth Seeker 🛡️")
            post_text = f"Simulated Gemini: Agent {agent_id} Achieved {', '.join(badges)}! Thriving Amplified 🚀"
            return {"alignment_score": score, "earned_badges": badges, "announcement_text": post_text}
        
        params = {"key": self.api_key}
        payload = {
            "contents": content,
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "generationConfig": {
                "responseMimeType": "application/json",  # Structured JSON output
                "temperature": 0.7,
                "maxOutputTokens": 512
            }
        }
        
        try:
            response = requests.post(self.endpoint, params=params, json=payload, timeout=30)
            response.raise_for_status()
            candidates = response.json()["candidates"]
            content = candidates[0]["content"]["parts"][0]["text"]
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
        result = self.query_gemini_structured(agent_id, intent, thrive_level)
        if "error" in result:
            result = result.get("simulation", {"alignment_score": thrive_level, "earned_badges": [], "announcement_text": "Mercy Preserved 🚀"})
        return result
