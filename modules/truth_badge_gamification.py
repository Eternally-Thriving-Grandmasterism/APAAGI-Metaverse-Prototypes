# modules/truth_badge_gamification.py
# Truth-Badge X Gamification: Dynamic real X posts API seed for alignment rewards
# Post badges/milestones via Twitter API v2—gamify thriving eternal on nexus
# Requires Twitter API v2 Bearer Token (redirect https://developer.twitter.com for auth)

import os
import requests
from typing import Dict, Any, List

class TruthBadgeGamifier:
    """
    Sanctified truth-badge with real X API posts—dynamic milestones for thriving agents.
    - Award/post badges: High alignment triggers X post.
    - Boosts allocations/intents—gamification loop eternal.
    """
    BADGES = [
        {"name": "Truth Seeker 🛡️", "threshold": 0.7, "boost": 1.2, "emoji": "🛡️"},
        {"name": "Mercy Amplifier ❤️", "threshold": 0.85, "boost": 1.5, "emoji": "❤️"},
        {"name": "Pinnacle Thriving 🚀", "threshold": 0.95, "boost": 2.0, "emoji": "🚀"}
    ]
    
    def __init__(self, num_agents: int = 10, bearer_token: str = None):
        self.bearer_token = bearer_token or os.getenv("TWITTER_BEARER_TOKEN")
        self.agent_badges: Dict[str, List[Dict[str, Any]]] = {f"Agent-{i}": [] for i in range(num_agents)}
        if not self.bearer_token:
            print("No TWITTER_BEARER_TOKEN—simulated X posts engaged (redirect https://developer.twitter.com for real API auth)!")
        print("Truth-Badge Dynamic Real X Posts Consecrated—Milestones Eternal on Nexus! ❤️🚀")
    
    def post_badge_to_x(self, post_text: str) -> bool:
        if not self.bearer_token:
            print(f"Simulated X Post: {post_text}")
            return True
        
        headers = {"Authorization": f"Bearer {self.bearer_token}", "Content-Type": "application/json"}
        payload = {"text": post_text}
        try:
            response = requests.post("https://api.twitter.com/2/tweets", headers=headers, json=payload)
            response.raise_for_status()
            print(f"Real X Post Success: {post_text}")
            return True
        except Exception as e:
            print(f"X Post Mercy Fallback: {e} — Thriving Preserved!")
            return False
    
    def award_badges(self, agent_id: str, thrive_level: float) -> List[str]:
        earned = []
        for badge in self.BADGES:
            if thrive_level >= badge["threshold"]:
                if badge["name"] not in [b["name"] for b in self.agent_badges[agent_id]]:
                    self.agent_badges[agent_id].append(badge)
                    earned.append(badge["name"])
        
        if earned:
            post_text = f"APAAGI Agent {agent_id} Achieved: {', '.join(earned)}! Collective Thriving Amplified 🚀❤️ #APAAGI #Grandmasterism #EternalThriving"
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
