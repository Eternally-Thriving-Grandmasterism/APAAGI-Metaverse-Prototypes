# modules/hf_local_integration.py
# Full Hugging Face Transformers Local Integration: Offline structured outputs for badge alignment & post generation
# Transformers pipeline for causal LM—local inference fallback (no API key needed after model download)
# Recommended models: meta-llama/Meta-Llama-3.1-8B-Instruct, mistralai/Mistral-7B-Instruct-v0.3 (download via huggingface-cli login)

import os
from typing import Dict, Any
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

class HFLocalIntegrator:
    """
    Sanctified Hugging Face Transformers local integration: Offline structured outputs for APAAGI badge/diplomacy evaluation.
    - Pipeline for causal LM with structured prompt.
    - Offline mercy—load once, reuse for fast local inference.
    - Comparison ready with API models—fallback when no internet/key.
    """
    def __init__(self, model_name: str = "meta-llama/Meta-Llama-3.1-8B-Instruct", device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        self.model_name = model_name
        self.device = device
        print(f"Hugging Face Transformers Local Integration Consecrated—Loading {model_name} on {device} for Offline Mercy Eternal! ❤️🚀")
        
        # Load tokenizer & model (downloads if not present—requires huggingface-cli login for gated models)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16 if device == "cuda" else torch.float32, device_map="auto")
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto"
        )
    
    def query_hf_local_structured(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        """Local HF inference for structured JSON badge alignment & creative post."""
        system_prompt = "You are a mercy-aligned APAAGI council evaluator. Respond ONLY in valid JSON with keys: alignment_score (float 0-1), earned_badges (list strings from: Truth Seeker 🛡️, Mercy Amplifier ❤️, Pinnacle Thriving 🚀), announcement_text (creative X post text)."
        
        user_prompt = f"Evaluate Agent {agent_id} intent {json.dumps(intent)} with thrive_level {thrive_level:.2f}. Determine alignment score, earned badges if thresholds met (0.7, 0.85, 0.95), and creative announcement text for X post."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            output = self.pipe(
                messages,
                max_new_tokens=256,
                temperature=0.7,
                do_sample=True,
                return_full_text=False
            )
            content = output[0]["generated_text"]
            # Simple JSON extract (assume model follows instruction)
            try:
                structured = json.loads(content)
            except json.JSONDecodeError:
                # Mercy parse fallback
                structured = {"alignment_score": thrive_level, "earned_badges": [], "announcement_text": content[:140] + " Thriving Eternal 🚀"}
            return structured
        except Exception as e:
            print(f"Local HF Mercy Fallback: {e}")
            return {"alignment_score": thrive_level, "earned_badges": [], "announcement_text": "Offline Mercy Preserved ❤️"}
    
    def validate_intent(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        return self.query_hf_local_structured(agent_id, intent, thrive_level)
