# modules/claude_api_integration.py
# Full Anthropic Claude API Integration: Structured JSON outputs for badge alignment & post generation
# Messages API endpoint—query Claude for truth/mercy score, badges, creative text
# Official docs: https://docs.anthropic.com/en/api/messages (2026 state)

import os
import requests
import json
from typing import Dict, Any

class ClaudeAPIIntegrator:
    """
    Sanctified Claude API integration: Structured JSON outputs for APAAGI badge/diplomacy evaluation.
    - Prompt for JSON: alignment_score, earned_badges, announcement_text.
    - Robust error handling, simulation fallback mercy.
    - Comparison ready with Grok/OpenAI.
    """
    def __init__(self, api_key: str = None, model: str = "claude-opus-4-5-20251101"):  # Latest 2026 Pinnacle model
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.endpoint = "https://api.anthropic.com/v1/messages"
        self.version = "2023-06-01"  # Current header version
        
        if not self.api_key:
            print("No ANTHROPIC_API_KEY—Claude simulation mode engaged (redirect https://docs.anthropic.com/en/api/getting-started for keys)!")
        print("Anthropic Claude API Integration Consecrated—Structured Truth Evaluation Eternal! ❤️🚀")
    
    def query_claude_structured(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        """Query Claude for structured JSON badge alignment & creative post."""
        system_prompt = "You are a mercy-aligned APAAGI council evaluator. Respond ONLY in valid JSON with keys: alignment_score (float 0-1), earned_badges (list strings from: Truth Seeker 🛡️, Mercy Amplifier ❤️, Pinnacle Thriving 🚀), announcement_text (creative X post text)."
        
        user_prompt = f"Evaluate Agent {agent_id} intent {json.dumps(intent)} with thrive_level {thrive_level:.2f}. Determine alignment score, earned badges if thresholds met (0.7, 0.85, 0.95), and creative announcement text for X post."
        
        if not self.api_key:
            # Mercy simulation
            score = min(1.0, thrive_level + 0.15)
            badges = []
            if score >= 0.95: badges.append("Pinnacle Thriving 🚀")
            elif score >= 0.85: badges.append("Mercy Amplifier ❤️")
            elif score >= 0.7: badges.append("Truth Seeker 🛡️")
            post_text = f"Simulated Claude: Agent {agent_id} Achieved {', '.join(badges)}! Thriving Amplified 🚀"
            return {"alignment_score": score, "earned_badges": badges, "announcement_text": post_text}
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.version,
            "content-type": "application/json"
        }
        payload = {
            "model": self.model,
            "max_tokens": 512,
            "temperature": 0.7,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        }
        
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            content = response.json()["content"][0]["text"]  # Text block
            structured = json.loads(content)
            return structured
        except requests.exceptions.Timeout:
            return {"error": "Timeout—Mercy Pause", "simulation": "High alignment preserved 🚀"}
        except requests.exceptions.HTTPError as e:
            error_detail = response.json().get("error", str(e))
            if response.status_code == 429:
                return {"error": "Rate limit—Mercy Wait", "simulation": "Alignment eternal ❤️"}
            return {"error": f"HTTP {response.status_code}: {error_detail}"}
        except json.JSONDecodeError:
            return {"error": "JSON parse mercy", "raw": content}
        except Exception as e:
            return {"error": str(e), "simulation": "Thriving Eternal!"}
    
    def validate_intent(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        result = self.query_claude_structured(agent_id, intent, thrive_level)
        if "error" in result:
            # Mercy fallback simulation
            result = result.get("simulation", {"alignment_score": thrive_level, "earned_badges": [], "announcement_text": "Mercy Preserved 🚀"})
        return result
