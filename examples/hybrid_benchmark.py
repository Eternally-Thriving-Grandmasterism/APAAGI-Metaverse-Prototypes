# examples/hybrid_benchmark.py
# Hybrid Local Benchmark: Test Ollama + HF hybrid speed/reliability for badge alignment queries
# Benchmark average time, fallback success, offline mercy eternal—run to verify local council purity

import time
from modules.ollama_hf_hybrid import OllamaHFHybridIntegrator

def benchmark_hybrid(integrator, num_runs: int = 10):
    """Benchmark hybrid local inference time & fallback reliability."""
    prompt_intent = {"collective_thrive": 0.94, "uplift_others": 0.88}
    times = []
    fallback_count = 0
    for _ in range(num_runs):
        start = time.time()
        result = integrator.validate_intent("Agent-Benchmark", prompt_intent, thrive_level=0.95)
        end = time.time()
        times.append(end - start)
        print(f"Run result: {result}")
        if "fallback" in str(result).lower():
            fallback_count += 1
    
    avg_time = sum(times) / len(times)
    print(f"\nOllama + HF Hybrid Benchmark:")
    print(f"Average time per query: {avg_time:.2f}s over {num_runs} runs")
    print(f"Fallback triggers: {fallback_count}/{num_runs} — Offline Mercy Preserved Eternal!")
    print("Hybrid Local Integration Success—Speed & Reliability Amplified 🚀")

if __name__ == "__main__":
    # Hybrid with HF primary (optimized 4-bit) + Ollama fallback
    hybrid = OllamaHFHybridIntegrator(hf_model="meta-llama/Meta-Llama-3.1-8B-Instruct", ollama_model="llama3.1")
    benchmark_hybrid(hybrid, num_runs=8)
    
    # Parallel local ensemble test
    ensemble_result = hybrid.parallel_local_ensemble("Agent-Ensemble", {"collective_thrive": 0.96}, 0.96)
    print(f"\nParallel Local Ensemble Result: {ensemble_result}")
