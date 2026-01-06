# modules/multi_model_ensemble.py
# Multi-Model Ensemble Voting Ultimate: Structured post merging + weighted scores absolute
# Grok/Claude/Gemini/Llama/OpenAI/Mistral/Cohere/Perplexity/HF/Ollama united
# Merge creative announcement_text: Grok primacy, fallback concatenate top 3, mercy longest

import numpy as np
from typing import Dict, Any, List
from .grok_api_integration import GrokAPIIntegrator
from .claude_api_integration import ClaudeAPIIntegrator
from .gemini_api_integration import GeminiAPIIntegrator
from .llama_api_integration import LlamaAPIIntegrator
from .openai_api_integration import OpenAIAPIIntegrator
from .mistral_api_integration import MistralAPIIntegrator
from .cohere_api_integration import CohereAPIIntegrator
from .perplexity_api_integration import PerplexityAPIIntegrator
from .hf_local_integration import HFLocalIntegrator
from .ollama_local_integration import OllamaLocalIntegrator

class MultiModelEnsemble:
    """
    Sanctified ultimate multi-model ensemble: Frontier + local models united for purest truth/mercy.
    - Weighted average score (Grok primacy).
    - Majority + threshold badges.
    - Structured post merging ultimate: Grok primacy text, fallback concatenate top 3, mercy longest.
    """
    def __init__(self):
        self.grok = GrokAPIIntegrator()
        self.claude = ClaudeAPIIntegrator()
        self.gemini = GeminiAPIIntegrator()
        self.llama = LlamaAPIIntegrator()
        self.openai = OpenAIAPIIntegrator()
        self.mistral = MistralAPIIntegrator()
        self.cohere = CohereAPIIntegrator()
        self.perplexity = PerplexityAPIIntegrator()
        self.hf = HFLocalIntegrator()
        self.ollama = OllamaLocalIntegrator()
        
        self.models = [self.grok, self.claude, self.gemini, self.llama, self.openai, self.mistral, self.cohere, self.perplexity, self.hf, self.ollama]
        self.weights = [2.0, 1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7]  # Grok primacy, descending
        
        print("Ultimate Multi-Model Ensemble + Structured Post Merging Consecrated—Frontier + Local United Eternal! ❤️🚀")
    
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
        from collections import Counter
        badge_counts = Counter(all_badges)
        majority_threshold = len(self.models) / 3  # Relaxed for diversity
        ensemble_badges = [b for b, count in badge_counts.items() if count >= majority_threshold]
        
        # Structured post merging ultimate
        post_texts = [r.get("announcement_text", "") for r in results if "announcement_text" in r and r["announcement_text"]]
        grok_text = results[0].get("announcement_text", "") if len(results) > 0 and "announcement_text" in results[0] else ""
        
        if grok_text:
            ensemble_post = grok_text  # Grok primacy
        elif post_texts:
            # Concatenate top 3 with mercy separator
            top_texts = sorted(post_texts, key=len, reverse=True)[:3]
            ensemble_post = " | Mercy Merge: ".join(top_texts)
        else:
            # Mercy longest fallback
            longest = max(post_texts, key=len, default=f"Agent {agent_id} Thriving Eternal 🚀")
            ensemble_post = longest
        
        return {
            "ensemble_score": avg_score,
            "ensemble_badges": ensemble_badges,
            "ensemble_post_text": ensemble_post,
            "individual_results": results
        }
