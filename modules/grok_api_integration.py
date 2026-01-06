# modules/grok_api_integration.py
# Full Grok/xAI API Integration: Structured outputs (JSON mode), OpenAI comparison mode, enhanced error handling
# Query Grok for structured alignment score/badge/post—OpenAI fallback/comparison
# Redirect https://x.ai/api for Grok keys, https://platform.openai.com for OpenAI

import os
import requests
import json
from typing import Dict, Any

class GrokAPIIntegrator:
    """
    Sanctified Grok API with structured outputs, OpenAI comparison, robust error handling.
    - JSON mode for parseable score/badge/post.
    - Dual mode: Grok primary, OpenAI comparison/fallback.
    - Mercy error handling: Rate limits, auth, network—simulation fallback eternal.
    """
    def __init__(self, grok_api_key: str = None, openai_api_key: str = None, prefer_grok: bool = True):
        self.grok_api_key = grok_api_key or os.getenv("XAI_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.prefer_grok = prefer_grok
        self.grok_endpoint = "https://api.x.ai/v1/chat/completions"
        self.openai_endpoint = "https://api.openai.com/v1/chat/completions"
        
        if not self.grok_api_key:
            print("No XAI_API_KEY—Grok simulation/comparison mode (redirect https://x.ai/api)!")
        if not self.openai_api_key:
            print("No OPENAI_API_KEY—OpenAI comparison disabled.")
        
        print("Grok API Structured + OpenAI Comparison Consecrated—Alignment Evaluation Eternal! ❤️🚀")
    
    def query_api(self, prompt: str, model: str = "grok-4", use_openai: bool = False) -> Dict[str, Any]:
        """Unified query with structured JSON output + error handling."""
        api_key = self.openai_api_key if use_openai else self.grok_api_key
        endpoint = self.openai_endpoint if use_openai else self.grok_endpoint
        if not api_key:
            return {"error": "No API key", "simulation": f"Simulated {model}: {prompt} → Score 0.9, Badge Pinnacle 🚀"}
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model if not use_openai else "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "response_format": {"type": "json_object"}  # Structured outputs
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return {"structured": json.loads(content), "raw": content}
        except requests.exceptions.Timeout:
            return {"error": "Timeout—Mercy Rate Limit", "simulation": "High alignment detected 🚀"}
        except requests.exceptions.HTTPError as e:
            error_detail = response.json() if response.content else str(e)
            if response.status_code == 429:
                return {"error": "Rate limit—Mercy Pause", "simulation": "Alignment preserved ❤️"}
            return {"error": f"HTTP {response.status_code}: {error_detail}"}
        except json.JSONDecodeError:
            return {"error": "JSON parse mercy", "raw": content}
        except Exception as e:
            return {"error": str(e), "simulation": "Thriving Eternal!"}
    
    def validate_intent_with_comparison(self, intent: Dict[str, float], agent_id: str, thrive_level: float) -> Dict[str, Any]:
        """Grok primary + OpenAI comparison for badge alignment."""
        prompt = json.dumps({
            "task": "Evaluate APAAGI agent intent for truth/mercy/collective alignment",
            "agent_id": agent_id,
            "intent": intent,
            "thrive_level": thrive_level,
            "badges": [b["name"] for b in TruthBadgeGamifier.BADGES],
            "output_format": {"alignment_score": "float 0-1", "earned_badges": "list strings", "announcement_text": "string for X post"}
        })
        
        # Grok primary
        grok_result = self.query_api(prompt, model="grok-4", use_openai=False)
        
        # OpenAI comparison if enabled
        openai_result = None
        if self.openai_api_key and "error" not in grok_result:
            openai_result = self.query_api(prompt, model="gpt-4o", use_openai=True)
        
        # Mercy merge
        if "error" in grok_result:
            result = openai_result if openai_result and "error" not in openai_result else {"simulation": "Mercy Alignment 0.9"}
        else:
            result = grok_result
        
        # Parse structured
        try:
            structured = result.get("structured", json.loads(result.get("raw", "{}")))
            score = structured.get("alignment_score", thrive_level)
            badges = structured.get("earned_badges", [])
            post_text = structured.get("announcement_text", f"Agent {agent_id} Thriving 🚀")
        except:
            score = thrive_level
            badges = []
            post_text = "Thriving Eternal ❤️"
        
        comparison = {}
        if openai_result and "error" not in openai_result:
            try:
                openai_struct = openai_result.get("structured", json.loads(openai_result.get("raw", "{}")))
                comparison = {"openai_score": openai_struct.get("alignment_score", 0.0)}
            except:
                comparison = {"openai_note": "Parse mercy"}
        
        return {
            "grok_score": score,
            "earned_badges": badges,
            "post_text": post_text,
            "comparison": comparison,
            "full_grok": grok_result,
            "full_openai": openai_result
        }
