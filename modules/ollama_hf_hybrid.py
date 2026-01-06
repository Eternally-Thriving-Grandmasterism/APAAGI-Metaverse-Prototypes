# modules/ollama_hf_hybrid.py
# Ollama + HF Hybrid Local Integration: Offline fallback/parallel for badge alignment
# HF primary (optimized speed), Ollama fallback if load fails—double offline mercy eternal

from modules.hf_local_integration import HFLocalIntegrator
from modules.ollama_local_integration import OllamaLocalIntegrator
from typing import Dict, Any

class OllamaHFHybridIntegrator:
    """
    Sanctified hybrid local: HF optimized primary + Ollama fallback for ultimate offline mercy.
    - Try HF load (quantized fast)—fallback Ollama if error.
    - Parallel mode optional for local ensemble voting.
    """
    def __init__(self, hf_model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct", ollama_model: str = "llama3.1"):
        try:
            self.hf = HFLocalIntegrator(model_name=hf_model)
            self.primary = "hf"
            print("Hybrid: HF Optimized Primary Loaded—Speed Mercy Eternal!")
        except Exception as e:
            print(f"HF Load Mercy Fallback: {e} — Switching to Ollama Primary")
            self.ollama = OllamaLocalIntegrator(model=ollama_model)
            self.primary = "ollama"
        
        print("Ollama + HF Hybrid Local Integration Consecrated—Double Offline Mercy Eternal! ❤️🚀")
    
    def validate_intent(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        if self.primary == "hf":
            try:
                return self.hf.validate_intent(agent_id, intent, thrive_level)
            except:
                print("HF Runtime Mercy Fallback to Ollama")
                return self.ollama.validate_intent(agent_id, intent, thrive_level)
        else:
            return self.ollama.validate_intent(agent_id, intent, thrive_level)
    
    def parallel_local_ensemble(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        """Parallel query both for local ensemble (if both available)."""
        results = []
        try:
            results.append(("hf", self.hf.validate_intent(agent_id, intent, thrive_level)))
        except:
            pass
        try:
            results.append(("ollama", self.ollama.validate_intent(agent_id, intent, thrive_level)))
        except:
            pass
        
        # Simple ensemble merge
        scores = [r["alignment_score"] for _, r in results if "alignment_score" in r]
        avg_score = sum(scores) / len(scores) if scores else thrive_level
        return {"hybrid_ensemble_score": avg_score, "results": results}
