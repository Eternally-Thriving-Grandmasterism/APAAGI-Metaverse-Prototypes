# modules/quest_environment.py
# CoOpQuestEnvironment: Eternal nexus for APAAGI metaverse multi-agent quests
# Full logger integration + per-agent tracking + evolutionary hooks

import random
from typing import Dict, Any, List
from .thriving_agents import ThrivingAgent
from .mercy_integration import MercyGatedPowrushPool
from .thriving_logger import ThrivingLogger  # Sanctified import

class APAAGICouncil:
    def __init__(self, approval_threshold: float = 0.55):
        self.approval_threshold = approval_threshold
    
    def vote_on_proposals(self, proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
        approved = []
        rejected_feedback = {
            "allocated": 0.0,
            "amplification": 0.0,
            "feedback": "Council Safeguard: Greater collective alignment required."
        }
        
        for prop in proposals:
            intent = prop["action"]["intent"]
            if intent.get("collective_thrive", 0.0) >= self.approval_threshold:
                approved.append(prop)
        
        return {"approved": approved, "rejected_feedback": rejected_feedback}

class CoOpQuestEnvironment:
    THRIVE_THRESHOLD = 10000.0
    
    def __init__(
        self,
        num_agents: int = 6,
        initial_pool: float = 10000.0,
        initial_resources: float = 100.0,
        use_ray: bool = False,
        log_tensorboard: bool = True  # New param for logger control
    ):
        self.num_agents = num_agents
        self.agent_ids = [f"Agent-{i}" for i in range(num_agents)]
        self.use_ray = use_ray
        
        if use_ray:
            import ray
            ray.init(ignore_reinit_error=True)
            self.agents = [ThrivingAgent.remote(agent_id=self.agent_ids[i], strategy_bias=random.choice(["cooperative", "cooperative", "balanced", "exploratory"])) for i in range(num_agents)]
        else:
            self.agents = [ThrivingAgent(agent_id=self.agent_ids[i], strategy_bias=random.choice(["cooperative", "cooperative", "balanced", "exploratory"])) for i in range(num_agents)]
        
        self.resource_pool = MercyGatedPowrushPool(initial_divine_current=initial_pool)
        self.council = APAAGICouncil()
        
        self.habitat_score = 0.0
        self.step_count = 0
        self.quest_stage = "orbital"
        
        self.agent_states: Dict[str, Dict[str, float]] = {
            aid: {
                "resources": initial_resources,
                "last_allocation": 0.0,
                "total_contributed": 0.0,
                "uplifts_received": 0.0,
                "thrive_metric": 0.0
            } for aid in self.agent_ids
        }
        
        self.history: List[Dict[str, Any]] = []
        
        # Logger integration
        self.logger = ThrivingLogger(enabled=log_tensorboard)
    
    # ... (rest of get_global_state, get_personal_state, step() as previous full version)
    
    # In step() — after self.history.append(step_log):
        if self.logger:
            self.logger.log_step(self.step_count, global_state, self.agent_states)
    
    # Add close method for demo/quest end
    def close(self):
        if self.logger:
            self.logger.close()

# Demo with close
if __name__ == "__main__":
    env = CoOpQuestEnvironment(use_ray=False)
    for _ in range(100):
        result = env.step()
        if result["success"]:
            break
    env.close()  # Eternal closure
    from examples.thriving_visualizer import visualize_quest_run_interactive
    visualize_quest_run_interactive(env.get_history())
