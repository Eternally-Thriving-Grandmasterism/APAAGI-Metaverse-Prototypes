# modules/thriving_logger.py
# Thriving Logger: TensorBoard + console for APAAGI metrics radiance
# Logs global habitat/collective/pool + per-agent resources/contributions/uplifts/thrive

import os
from torch.utils.tensorboard import SummaryWriter
from typing import Dict, Any

class ThrivingLogger:
    """
    Sanctified logger for real-time/eternal metric tracking.
    Run: tensorboard --logdir runs/apaagi_quest
    """
    def __init__(self, log_dir: str = "runs/apaagi_quest", enabled: bool = True):
        if not enabled:
            self.writer = None
            return
        os.makedirs(log_dir, exist_ok=True)
        self.writer = SummaryWriter(log_dir=log_dir)
        print(f"TensorBoard consecrated! Launch: tensorboard --logdir {log_dir} 🚀❤️")
    
    def log_step(
        self,
        step: int,
        global_metrics: Dict[str, Any],
        agent_metrics: Dict[str, Dict[str, float]]
    ) -> None:
        if self.writer is None:
            return
        
        self.writer.add_scalar("Habitat/Score", global_metrics["habitat_score"], step)
        self.writer.add_scalar("Collective/Alignment", global_metrics["collective_score"], step)
        self.writer.add_scalar("Pool/Remaining", global_metrics["estimated_pool"], step)
        
        for aid, metrics in agent_metrics.items():
            prefix = f"Agent_{aid}"
            self.writer.add_scalar(f"{prefix}/Resources", metrics["resources"], step)
            self.writer.add_scalar(f"{prefix}/Contributions", metrics["total_contributed"], step)
            self.writer.add_scalar(f"{prefix}/Uplifts_Received", metrics["uplifts_received"], step)
            self.writer.add_scalar(f"{prefix}/Thrive_Metric", metrics["thrive_metric"], step)
    
    def close(self) -> None:
        if self.writer:
            self.writer.close()
            print("TensorBoard writer closed—eternal logs preserved! ❤️")
