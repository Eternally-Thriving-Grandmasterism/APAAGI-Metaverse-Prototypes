# modules/thriving_logger.py
# Thriving Logger: TensorBoard integration for APAAGI metrics
# Logs habitat, collective, per-agent thrive/contributions/uplifts

from torch.utils.tensorboard import SummaryWriter
import os
from typing import Dict, Any

class ThrivingLogger:
    def __init__(self, log_dir: str = "runs/apaagi_quest"):
        os.makedirs(log_dir, exist_ok=True)
        self.writer = SummaryWriter(log_dir=log_dir)
        print(f"TensorBoard logging consecrated: tensorboard --logdir {log_dir}")
    
    def log_step(self, step: int, global_metrics: Dict[str, Any], agent_metrics: Dict[str, Dict[str, float]]):
        self.writer.add_scalar("Habitat/Score", global_metrics["habitat_score"], step)
        self.writer.add_scalar("Collective/Alignment", global_metrics["collective_score"], step)
        
        for aid, metrics in agent_metrics.items():
            prefix = f"Agent-{aid}"
            self.writer.add_scalar(f"{prefix}/Resources", metrics["resources"], step)
            self.writer.add_scalar(f"{prefix}/Contributions", metrics["total_contributed"], step)
            self.writer.add_scalar(f"{prefix}/Uplifts", metrics["uplifts_received"], step)
            self.writer.add_scalar(f"{prefix}/Thrive_Metric", metrics["thrive_metric"], step)
    
    def close(self):
        self.writer.close()
