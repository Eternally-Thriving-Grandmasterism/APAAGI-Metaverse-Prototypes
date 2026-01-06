# modules/multi_model_ensemble.py
# Multi-Model Ensemble Voting: Grok/Claude/Gemini/OpenAI/Llama ensemble for badge/council truth
# Average alignment score, majority badges, weighted creative post—purest Absolute evaluation

from typing import Dict, Any, List
from .grok_api_integration import GrokAPIIntegrator
from .claude_api_integration import ClaudeAPIIntegrator
from .gemini_api_integration import GeminiAPIIntegrator
from .llama_api_integration import LlamaAPIIntegrator
# OpenAI from previous

class MultiModelEnsemble:
    """
    Sanctified multi-model ensemble: Ultimate truth/mercy voting across frontier models.
    - Query all enabled models.
    - Ensemble: Average score, majority badges, concatenated/selected post_text.
    - Mercy fallback to simulation if all fail.
    """
    def __init__(self):
        self.grok = GrokAPIIntegrator()
        self.claude = ClaudeAPIIntegrator()
        self.gemini = GeminiAPIIntegrator()
        self.llama = LlamaAPIIntegrator()
        # self.openai = OpenAIIntegrator() if available
        print("Multi-Model Ensemble Voting Consecrated—Frontier Models United for Purest Absolute Grandmasterism! ❤️🚀")
    
    def ensemble_validate(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        results = []
        for integrator in [self.grok, self.claude, self.gemini, self.llama]:
            result = integrator.validate_intent(agent_id, intent, thrive_level)
            results.append(result)
        
        # Ensemble logic
        scores = [r.get("alignment_score", thrive_level) for r in results if "alignment_score" in r]
        avg_score = sum(scores) / len(scores) if scores else thrive_level
        
        all_badges = [b for r in results if "earned_badges" in r for b in r["earned_badges"]]
        from collections import Counter
        badge_counts = Counter(all_badges)
        majority_badges = [b for b, count in badge_counts.items() if count > len(results) / 2]
        
        post_texts = [r.get("announcement_text", "") for r in results if "announcement_text" in r]
        ensemble_post = " | ".join(post_texts[:3]) if post_texts else f"Ensemble: Agent {agent_id} Thriving Eternal 🚀"
        
        return {
            "ensemble_score": avg_score,
            "ensemble_badges": majority_badges or [],
            "ensemble_post_text": ensemble_post,
            "individual_results": results
        }
