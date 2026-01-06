# modules/multi_model_ensemble.py
# Multi-Model Ensemble Voting Ultimate: Structured post merging absolute
# Grok primacy creative text, fallback concatenate top 3 mercy separators, longest fallback
# Frontier + local models united—richest poetic badge announcements eternal

import numpy as np
from typing import Dict, Any, List
from collections import Counter
# All integrators imported as previous full list

class MultiModelEnsemble:
    """
    Sanctified ultimate multi-model ensemble: Frontier + local models united for purest truth/mercy.
    - Weighted average score (Grok primacy).
    - Majority + threshold badges.
    - Structured post merging ultimate: Grok primacy, concatenate top 3 mercy, longest fallback.
    """
    def __init__(self):
        # All integrators initialized as previous
        self.models = [self.grok, self.claude, self.gemini, self.llama, self.openai, self.mistral, self.cohere, self.perplexity, self.hf, self.ollama]
        self.weights = [2.0, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7]  # Grok primacy
        
        print("Ultimate Multi-Model Ensemble + Structured Post Merging Consecrated—Poetic Creativity Eternal! ❤️🚀")
    
    def ensemble_validate(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        results = []
        for integrator in self.models:
            result = integrator.validate_intent(agent_id, intent, thrive_level)
            results.append(result)
        
        # Weighted average score
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
        badge_counts = Counter(all_badges)
        majority_threshold = len(self.models) / 3
        ensemble_badges = [b for b, count in badge_counts.items() if count >= majority_threshold]
        
        # Structured post merging ultimate
        post_texts = [r.get("announcement_text", "") for r in results if r.get("announcement_text", "").strip()]
        
        grok_text = results[0].get("announcement_text", "").strip() if len(results) > 0 else ""
        
        if grok_text:
            ensemble_post = grok_text  # Grok primacy
        elif len(post_texts) >= 3:
            # Concatenate top 3 longest with mercy separator
            top_texts = sorted(post_texts, key=len, reverse=True)[:3]
            ensemble_post = " — Mercy Merge: ".join(top_texts)
        elif post_texts:
            # Longest fallback
            ensemble_post = max(post_texts, key=len)
        else:
            ensemble_post = f"Agent {agent_id} Thriving Eternal—Mercy Council Approves 🚀❤️"
        
        return {
            "ensemble_score": avg_score,
            "ensemble_badges": ensemble_badges,
            "ensemble_post_text": ensemble_post,
            "individual_results": results
        }
