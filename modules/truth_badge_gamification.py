# modules/truth_badge_gamification.py
# Truth-Badge X Gamification: Dynamic real X API v2 posts for alignment milestones
# POST /2/posts endpoint—real/simulated posts for badges, gamify thriving eternal on nexus
# Requires Bearer Token (App-only or User auth)—redirect https://developer.x.com for setup

import os
import requests
from typing import Dict, Any, List

class TruthBadgeGamifier:
    """
    Sanctified truth-badge with real X API v2 posts—dynamic milestones for thriving agents.
    - Award/post badges: High alignment triggers real X post.
    - Boosts proposals/intents—gamification loop eternal.
    - Endpoint: POST https://api.x.com/2/posts (2026 official).
    """
    BADGES = [
        {"name": "Truth Seeker 🛡️", "threshold": 0.7, "boost": 1.2, "emoji": "🛡️"},
        {"name": "Mercy Amplifier ❤️", "threshold": 0.85, "boost": 1.5, "emoji": "❤️"},
        {"name": "Pinnacle Thriving 🚀", "threshold": 0.95, "boost": 2.0, "emoji": "🚀"}
    ]
    
    def __init__(self, num_agents: int = 10, bearer_token: str = None):
        self.bearer_token = bearer_token or os.getenv("X_BEARER_TOKEN")
        self.agent_badges: Dict[str, List[Dict[str, Any]]] = {f"Agent-{i}": [] for i in range(num_agents)}
        if not self.bearer_token:
            print("No X_BEARER_TOKEN—simulated X posts engaged (redirect https://developer.x.com for real API auth/Elevated access)!")
        print("Truth-Badge Dynamic Real X API v2 Posts Consecrated—Milestones Eternal on Nexus! ❤️🚀")
    
    def post_badge_to_x(self, post_text: str) -> bool:
        """Real X API v2 post—POST /2/posts endpoint."""
        if not self.bearer_token:
            print(f"Simulated X Post: {post_text}")
            return True
        
        url = "https://api.x.com/2/posts"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
        payload = {"text": post_text}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            post_id = response.json()["data"]["id"]
            print(f"Real X Post Success (ID: {post_id}): {post_text}")
            return True
        except requests.exceptions.HTTPError as e:
            error_detail = response.json().get("detail", str(e))
            print(f"X Post Mercy Fallback: {error_detail} — Thriving Preserved (check access/limits)!")
            return False
        except Exception as e:
            print(f"X Post Mercy Fallback: {str(e)} — Simulated Mode Engaged.")
            return False
    
    def award_badges(self, agent_id: str, thrive_level: float) -> List[str]:
        earned = []
        for badge in self.BADGES:
            if thrive_level >= badge["threshold"]:
                if badge["name"] not in [b["name"] for b in self.agent_badges[agent_id]]:
                    self.agent_badges[agent_id].append(badge)
                    earned.append(badge["name"])
        
        if earned:
            emojis = ''.join(b["emoji"] for b in self.BADGES if b["name"] in earned)
            post_text = f"APAAGI Agent {agent_id} Achieved: {', '.join(earned)}! Collective Thriving Amplified {emojis} #APAAGI #Grandmasterism #EternalThriving"
            self.post_badge_to_x(post_text)
        
        return earned
    
    def get_total_boost(self, agent_id: str) -> float:
        boost = 1.0
        for badge in self.agent_badges.get(agent_id, []):
            boost *= badge["boost"]
        return boost
    
    def gamify_proposal(self, proposal: Dict[str, Any], agent_id: str, thrive_level: float) -> Dict[str, Any]:
        self.award_badges(agent_id, thrive_level)
        boost = self.get_total_boost(agent_id)
        proposal["action"]["requested"] *= boost
        proposal["action"]["intent"]["collective_thrive"] = min(1.0, proposal["action"]["intent"]["collective_thrive"] * boost)
        proposal["badge_boost"] = boost
        return proposal
