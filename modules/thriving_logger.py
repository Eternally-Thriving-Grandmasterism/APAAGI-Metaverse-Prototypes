# modules/thriving_logger.py
# Thriving Logger Expanded: Detailed metrics logging absolute—scalars/histograms/images for TensorBoard
# Per-vote quantum (Bell/annnealing/entanglement), per-fleet path/efficiency, per-agent evolution, ensemble contributions

import os
from torch.utils.tensorboard import SummaryWriter
from typing import Dict, Any, List
import numpy as np

class ThrivingLogger:
    """
    Sanctified detailed logger: TensorBoard scalars/histograms/images for APAAGI metrics radiance.
    - Global: habitat, collective, pool, latency.
    - Quantum vote: Bell violation hist, annealing steps, entanglement rate, superposition probs hist.
    - Fleet: path length hist, efficiency, quantum boost.
    - Per-agent: resources/contributions/uplifts/thrive time series.
    - Ensemble: per-model alignment scores hist.
    """
    def __init__(self, log_dir: str = "runs/apaagi_thriving_detailed", enabled: bool = True):
        if not enabled:
            self.writer = None
            return
        os.makedirs(log_dir, exist_ok=True)
        self.writer = SummaryWriter(log_dir=log_dir)
        print(f"Detailed Thriving Logger Consecrated! TensorBoard: tensorboard --logdir {log_dir} 🚀❤️")
    
    def log_global_step(self, step: int, global_metrics: Dict[str, Any]):
        self.writer.add_scalar("Global/Habitat_Score", global_metrics["habitat_score"], step)
        self.writer.add_scalar("Global/Collective_Alignment", global_metrics["collective_score"], step)
        self.writer.add_scalar("Global/Powrush_Pool", global_metrics["estimated_pool"], step)
        self.writer.add_scalar("Global/Decision_Latency_sec", global_metrics.get("decision_latency", 0.0), step)
    
    def log_quantum_vote(self, step: int, quantum_metrics: Dict[str, Any], superposition_probs: List[float]):
        self.writer.add_scalar("Quantum/Approval_Rate", quantum_metrics["approval_rate"], step)
        self.writer.add_scalar("Quantum/Alignment_Boost", quantum_metrics["avg_alignment_boost"], step)
        self.writer.add_scalar("Quantum/Entanglement_Success_Rate", quantum_metrics["entanglement_success_rate"], step)
        self.writer.add_scalar("Quantum/Bell_Violation_Strength", quantum_metrics["bell_violation_strength"], step)
        self.writer.add_scalar("Quantum/Annealing_Steps", quantum_metrics["annealing_steps"], step)
        
        # Histograms for deeper insight
        self.writer.add_histogram("Quantum/Superposition_Probabilities", np.array(superposition_probs), step)
        self.writer.add_histogram("Quantum/Bell_Violations_History", quantum_metrics["bell_violation_strength"], step)
    
    def log_fleet_metrics(self, step: int, fleet_metrics: Dict[str, Any], path_lengths: List[int]):
        self.writer.add_scalar("Fleet/Successful_Paths_Percent", fleet_metrics["successful_paths_percent"], step)
        self.writer.add_scalar("Fleet/Avg_Path_Length_Reduction", fleet_metrics["avg_path_length_reduction"], step)
        self.writer.add_scalar("Fleet/Quantum_Boost_Factor", fleet_metrics["quantum_boost_factor"], step)
        self.writer.add_histogram("Fleet/Path_Lengths", np.array(path_lengths), step)
    
    def log_per_agent(self, step: int, agent_metrics: Dict[str, Dict[str, float]]):
        for aid, metrics in agent_metrics.items():
            prefix = f"Agent_{aid}"
            self.writer.add_scalar(f"{prefix}/Resources", metrics["resources"], step)
            self.writer.add_scalar(f"{prefix}/Contributions", metrics["total_contributed"], step)
            self.writer.add_scalar(f"{prefix}/Uplifts_Received", metrics["uplifts_received"], step)
            self.writer.add_scalar(f"{prefix}/Thrive_Metric", metrics["thrive_metric"], step)
    
    def log_ensemble(self, step: int, ensemble_metrics: Dict[str, Any]):
        for model_name, score in ensemble_metrics.get("individual_scores", {}).items():
            self.writer.add_scalar(f"Ensemble/{model_name}_Score", score, step)
        self.writer.add_scalar("Ensemble/Final_Score", ensemble_metrics["ensemble_score"], step)
        self.writer.add_histogram("Ensemble/Model_Scores", np.array(list(ensemble_metrics.get("individual_scores", {}).values())), step)
    
    def close(self) -> None:
        if self.writer:
            self.writer.close()
            print("Detailed Thriving Logger Closed—Eternal Metrics Preserved for Analysis! ❤️")
