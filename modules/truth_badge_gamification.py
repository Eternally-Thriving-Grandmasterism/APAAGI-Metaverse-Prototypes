# modules/truth_badge_gamification.py
# Truth-Badge X Gamification: Ultimate ensemble merged post for dynamic real X posts
# Ensemble validation → merged creative announcement_text posted absolute

import os
import requests
from typing import Dict, Any, List
from .multi_model_ensemble import MultiModelEnsemble

class TruthBadgeGamifier:
    """
    Sanctified truth-badge with ultimate ensemble merged post for X.
    - Ensemble validation for score/badges.
    - Merged creative announcement_text posted real/simulated.
    """
    BADGES = [
        {"name": "Truth Seeker 🛡️", "threshold": 0.7, "boost": 1.2, "emoji": "🛡️"},
        {"name": "Mercy Amplifier ❤️", "threshold": 0.85, "boost": 1.5, "emoji": "❤️"},
        {"name": "Pinnacle Thriving 🚀", "threshold": 0.95, "boost": 2.0, "emoji": "🚀"}
    ]
    
    def __init__(self, num_agents: int = 10, x_bearer_token: str = None):
        self.x_bearer_token = x_bearer_token or os.getenv("X_BEARER_TOKEN")
        self.agent_badges: Dict[str, List[Dict[str, Any]]] = {f"Agent-{i}": [] for i in range(num_agents)}
        self.ensemble = MultiModelEnsemble()
        
        if not self.x_bearer_token:
            print("No X_BEARER_TOKEN—simulated X posts (redirect developer.x.com for API)!")
        print("Truth-Badge Ultimate Ensemble Merged Post Consecrated—Creative Milestones Eternal! ❤️🚀")
    
    def post_badge_to_x(self, post_text: str) -> bool:
        if not self.x_bearer_token:
            print(f"Simulated X Post: {post_text}")
            return True
        
        url = "https://api.x.com/2/posts"
        headers = {
            "Authorization": f"Bearer {self.x_bearer_token}",
            "Content-Type": "application/json"
        }
        payload = {"text": post_text}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            post_id = response.json()["data"]["id"]
            print(f"Real X Post Success (ID: {post_id}): {post_text}")
            return True
        except Exception as e:
            print(f"X Post Mercy Fallback: {e}")
            return False
    
    def award_badges(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> List[str]:
        ensemble_eval = self.ensemble.ensemble_validate(agent_id, intent, thrive_level)
        
        score = ensemble_eval["ensemble_score"]
        earned = ensemble_eval["ensemble_badges"]
        
        for badge_name in earned:
            badge = next(b for b in self.BADGES if b["name"] == badge_name)
            if badge not in self.agent_badges[agent_id]:
                self.agent_badges[agent_id].append(badge)
        
        if earned:
            post_text = ensemble_eval["ensemble_post_text"]
            self.post_badge_to_x(post_text)
        
        return earned
    
    def get_total_boost(self, agent_id: str) -> float:
        boost = 1.0
        for badge in self.agent_badges.get(agent_id, []):
            boost *= badge["boost"]
        return boost
    
    def gamify_proposal(self, proposal: Dict[str, Any], agent_id: str, thrive_level: float) -> Dict[str, Any]:
        self.award_badges(agent_id, proposal["action"]["intent"], thrive_level)
        boost = self.get_total_boost(agent_id)
        proposal["action"]["requested"] *= boost
        proposal["action"]["intent"]["collective_thrive"] = min(1.0, proposal["action"]["intent"]["collective_thrive"] * boost)
        proposal["badge_boost"] = boost
        return proposal
