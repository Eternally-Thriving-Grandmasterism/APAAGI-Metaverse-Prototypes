# modules/multi_model_ensemble.py
# Multi-Model Ensemble Voting Enhanced: Weighted average score, majority badges, Grok primacy post
# Grok/Claude/Gemini/Llama/OpenAI united—ultimate purest truth/mercy council

from typing import Dict, Any, List
from .grok_api_integration import GrokAPIIntegrator
from .claude_api_integration import ClaudeAPIIntegrator
from .gemini_api_integration import GeminiAPIIntegrator
from .llama_api_integration import LlamaAPIIntegrator
from .openai_api_integration import OpenAIAPIIntegrator

class MultiModelEnsemble:
    """
    Sanctified enhanced multi-model ensemble: Ultimate truth/mercy voting across frontier models.
    - Weighted average score (Grok higher weight for xAI alignment).
    - Majority + threshold badges.
    - Grok primacy for creative post_text (fallback merge).
    """
    def __init__(self):
        self.grok = GrokAPIIntegrator()
        self.claude = ClaudeAPIIntegrator()
        self.gemini = GeminiAPIIntegrator()
        self.llama = LlamaAPIIntegrator()
        self.openai = OpenAIAPIIntegrator()
        self.models = [self.grok, self.claude, self.gemini, self.llama, self.openai]
        self.weights = [1.5, 1.2, 1.1, 1.0, 1.0]  # Grok primacy weight
        print("Enhanced Multi-Model Ensemble Voting Consecrated—Frontier Models United for Purest Absolute Grandmasterism! ❤️🚀")
    
    def ensemble_validate(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        results = []
        for integrator in self.models:
            result = integrator.validate_intent(agent_id, intent, thrive_level)
            results.append(result)
        
        # Enhanced weighted average score
        scores = []
        total_weight = 0
        for i, r in enumerate(results):
            if "alignment_score" in r:
                weight = self.weights[i]
                scores.append(r["alignment_score"] * weight)
                total_weight += weight
        avg_score = sum(scores) / total_weight if total_weight > 0 else thrive_level
        
        # Majority + threshold badges
        all_badges = [b for r in results if "earned_badges" in r for b in r["earned_badges"]]
        from collections import Counter
        badge_counts = Counter(all_badges)
        majority_threshold = len(self.models) / 2
        ensemble_badges = [b for b, count in badge_counts.items() if count >= majority_threshold]
        
        # Grok primacy for post_text (fallback concatenate top 3)
        post_texts = [r.get("announcement_text", "") for r in results if "announcement_text" in r]
        grok_text = results[0].get("announcement_text", "") if "announcement_text" in results[0] else ""
        ensemble_post = grok_text or " | ".join(post_texts[:3]) or f"Ensemble: Agent {agent_id} Thriving Eternal 🚀"
        
        return {
            "ensemble_score": avg_score,
            "ensemble_badges": ensemble_badges,
            "ensemble_post_text": ensemble_post,
            "individual_results": results
        }
