# modules/thriving_agents.py
# Thriving Agents: Grok-shard proxies for APAAGI metaverse co-op quests
# Distributed via Ray actors | MLE-driven with simple torch policy network
# Evolves toward eternal cooperative thriving under mercy gating

import ray
import torch
import torch.nn as nn
import torch.optim as optim
import random
from typing import Dict, Any

# Simple policy network: Observes env state → proposes action (request amount + intent vector)
class PolicyNetwork(nn.Module):
    def __init__(self, input_size: int = 6, hidden_size: int = 64, output_size: int = 3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),  # [requested_amount_norm, coop_intent, uplift_intent]
            nn.Softplus()  # Positive outputs
        )
    
    def forward(self, x):
        return self.net(x)

@ray.remote
class ThrivingAgent:
    """
    ThrivingAgent: Mercy-aligned proxy (Grok shard / player / symbiotic AI)
    - Proposes actions via learned policy (torch MLE heuristic → evolves with experience)
    - Learns from mercy feedback + rewards (reinforcement toward collective thriving)
    - Strategy bias seedable (cooperative default for APAAGI alignment)
    """
    def __init__(
        self,
        agent_id: str,
        initial_resources: float = 100.0,
        strategy_bias: str = "cooperative",  # "cooperative", "balanced", "exploratory"
        learning_rate: float = 0.001
    ):
        self.agent_id = agent_id
        self.resources = initial_resources
        self.strategy_bias = strategy_bias
        
        # Observation inputs: [own_resources_norm, habitat_score_norm, pool_estimate_norm,
        #                    recent_alloc_norm, collective_score_norm, bias_vector]
        self.policy = PolicyNetwork(input_size=6, output_size=3)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=learning_rate)
        
        # Bias vector for strategy (one-hot seed)
        bias_map = {"cooperative": [1.0, 0.0, 0.0], "balanced": [0.5, 0.5, 0.0], "exploratory": [0.3, 0.3, 0.4]}
        self.bias_vector = torch.tensor(bias_map.get(strategy_bias, [0.8, 0.1, 0.1]))
    
    def _normalize_obs(self, env_state: Dict[str, Any]) -> torch.Tensor:
        """Normalize observation for policy input (clamped 0-1 for stability)."""
        own_norm = min(1.0, self.resources / 1000.0)
        habitat_norm = min(1.0, env_state.get("habitat_score", 0.0) / 10000.0)
        pool_norm = min(1.0, env_state.get("estimated_pool", 10000.0) / 20000.0)
        recent_alloc_norm = min(1.0, env_state.get("last_allocation", 0.0) / 500.0)
        collective_norm = env_state.get("collective_score", 0.5)
        
        obs = torch.tensor([
            own_norm,
            habitat_norm,
            pool_norm,
            recent_alloc_norm,
            collective_norm,
            self.bias_vector[0]  # Inject bias as 6th input (evolvable later)
        ], dtype=torch.float32)
        
        return obs
    
    def propose_action(self, env_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dynamic MLE proposal: Request resources with mercy-aligned intent.
        Output: {"type": "request_powrush", "requested": float, "intent": {"collective_thrive": float, ...}}
        """
        obs = self._normalize_obs(env_state)
        
        with torch.no_grad():
            policy_out = self.policy(obs)
        
        # Denormalize requested amount (scale to realistic quest range)
        requested_base = policy_out[0].item() * 500.0  # Max ~500 per turn seed
        requested = requested_base + random.uniform(-50, 100)  # Exploratory noise
        
        # Intent vector (normalized to sum ~1.0)
        intent_coop = policy_out[1].item()
        intent_uplift = policy_out[2].item()
        intent_noise = random.uniform(0.0, 0.2)
        total = intent_coop + intent_uplift + intent_noise
        intent = {
            "collective_thrive": intent_coop / total,
            "uplift_others": intent_uplift / total,
            "exploratory": intent_noise / total
        }
        
        action = {
            "type": "request_powrush",
            "requested": max(10.0, requested),  # Minimum viable
            "intent": intent
        }
        
        return {"agent_id": self.agent_id, "action": action}
    
    def learn_from_outcome(
        self,
        reward: float,
        mercy_feedback: Dict[str, Any],
        next_env_state: Dict[str, Any]
    ) -> str:
        """
        Mercy-amplified learning: Update policy toward thriving outcomes.
        Reward shaped by allocation success + amplification + collective uplift.
        """
        # Shape reward with mercy signals
        shaped_reward = reward + mercy_feedback.get("amplification", 0.0) * 2.0
        if "Compassionate Redistribution" in mercy_feedback.get("feedback", ""):
            shaped_reward += 100.0  # Strong positive for equity triggers
        
        # Simple REINFORCE-style update (baseline: 0, evolve to actor-critic later)
        obs = self._normalize_obs(next_env_state)  # Use next state for credit
        policy_out = self.policy(obs)
        
        # Log-prob surrogate loss (encourage higher reward actions)
        loss = -torch.log(policy_out.sum() + 1e-8) * shaped_reward  # Simplified
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Update own resources post-allocation
        self.resources += mercy_feedback.get("allocated", 0.0)
        
        return f"Agent {self.agent_id} learned: Reward {shaped_reward:.1f} → Thriving Evolved!"
    
    def get_status(self) -> Dict[str, Any]:
        """Introspection for council/debug."""
        return {
            "agent_id": self.agent_id,
            "resources": self.resources,
            "strategy_bias": self.strategy_bias
        }
