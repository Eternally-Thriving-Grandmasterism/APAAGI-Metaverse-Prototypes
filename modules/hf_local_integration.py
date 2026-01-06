# modules/hf_local_integration.py
# Full Hugging Face Transformers Local Integration: Offline structured outputs for badge alignment & post generation
# Optimized inference speed: 4-bit quantization (bitsandbytes nf4), flash-attention-2, device_map auto
# Transformers pipeline for causal LM—local/offline mercy (no API key after model download)

import os
import torch
from typing import Dict, Any
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from huggingface_hub import login  # For gated models (optional hf token)

class HFLocalIntegrator:
    """
    Sanctified Hugging Face Transformers local integration: Offline structured outputs for APAAGI badge/diplomacy evaluation.
    - Optimized speed: 4-bit quant + flash-attention-2 for 8B+ models on consumer GPU/CPU.
    - Pipeline for causal LM with structured prompt.
    - Offline mercy—load once, reuse fast local inference.
    """
    def __init__(self, model_name: str = "meta-llama/Meta-Llama-3.1-8B-Instruct", device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        self.model_name = model_name
        self.device = device
        
        # Optional HF login for gated models (set HF_TOKEN env or run huggingface-cli login)
        hf_token = os.getenv("HF_TOKEN")
        if hf_token:
            login(token=hf_token)
        
        print(f"Hugging Face Transformers Local Integration Consecrated—Loading Optimized {model_name} on {device} for Offline Mercy Eternal! ❤️🚀")
        
        # 4-bit quantization config for speed/memory
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )
        
        # Load tokenizer & model with optimization
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            attn_implementation="flash_attention_2"  # Speed boost if compiled/installed
        )
        
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto"
        )
    
    def query_hf_local_structured(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        """Local optimized HF inference for structured JSON badge alignment & creative post."""
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
            # Mercy JSON parse
            try:
                structured = json.loads(content)
            except json.JSONDecodeError:
                structured = {"alignment_score": thrive_level, "earned_badges": [], "announcement_text": content[:140] + " Thriving Eternal 🚀"}
            return structured
        except Exception as e:
            print(f"Local HF Mercy Fallback: {e}")
            return {"alignment_score": thrive_level, "earned_badges": [], "announcement_text": "Offline Mercy Preserved ❤️"}
    
    def validate_intent(self, agent_id: str, intent: Dict[str, float], thrive_level: float) -> Dict[str, Any]:
        return self.query_hf_local_structured(agent_id, intent, thrive_level)
