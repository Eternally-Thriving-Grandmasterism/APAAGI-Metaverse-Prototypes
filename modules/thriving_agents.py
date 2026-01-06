# modules/thriving_agents.py
# Thriving Agents: Grok-shard proxies for APAAGI metaverse co-op quests
# Distributed via Ray (or synchronous fallback) | Full A2C + Evolutionary dynamics
# Mercy-aligned MLE evolution toward eternal collective thriving

import ray
import torch
import torch.nn as nn
import torch.optim as optim
import random
import copy
from typing import Dict, Any, List

# Actor Policy Network
class PolicyNetwork(nn.Module):
    def __init__(self, input_size: int = 8, hidden_size: int = 64, output_size: int = 3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),  # [requested_amount_norm, coop_intent, uplift_intent]
            nn.Softplus()
        )
    
    def forward(self, x):
        return self.net(x)

# Critic Value Network (A2C baseline)
class CriticNetwork(nn.Module):
    def __init__(self, input_size: int = 8, hidden_size: int = 64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)  # State value estimate
        )
    
    def forward(self, x):
        return self.net(x)

@ray.remote  # Optional: Remove for synchronous/local runs
class ThrivingAgent:
    """
    ThrivingAgent: Mercy-aligned proxy with full A2C learning + evolutionary potential
    """
    def __init__(
        self,
        agent_id: str,
        strategy_bias: str = "cooperative",
        learning_rate: float = 0.001,
        gamma: float = 0.99
    ):
        self.agent_id = agent_id
        self.strategy_bias = strategy_bias
        self.gamma = gamma
        
        self.actor = PolicyNetwork()
        self.critic = CriticNetwork()
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=learning_rate)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=learning_rate * 3)
        
        bias_map = {"cooperative": [1.0, 0.0, 0.0], "balanced": [0.5, 0.5, 0.0], "exploratory": [0.3, 0.3, 0.4]}
        self.bias_vector = torch.tensor(bias_map.get(strategy_bias, [0.8, 0.1, 0.1]))
        
        # Personal thrive metrics (updated by env)
        self.thrive_metric = 0.0
    
    def _normalize_obs(self, personal_state: Dict[str, Any]) -> torch.Tensor:
        own_norm = min(1.0, personal_state.get("own_resources", 100.0) / 1000.0)
        own_last_norm = min(1.0, personal_state.get("own_last_allocation", 0.0) / 500.0)
        relative_norm = personal_state.get("relative_thrive_score", 0.5)
        habitat_norm = min(1.0, personal_state.get("habitat_score", 0.0) / 10000.0)
        pool_norm = min(1.0, personal_state.get("estimated_pool", 10000.0) / 20000.0)
        collective_norm = personal_state.get("collective_score", 0.5)
        
        obs = torch.tensor([
            own_norm, own_last_norm, relative_norm,
            habitat_norm, pool_norm, collective_norm,
            self.bias_vector[0], self.bias_vector[1]
        ], dtype=torch.float32)
        
        return obs.unsqueeze(0)  # Batch dim
    
    def propose_action(self, personal_state: Dict[str, Any]) -> Dict[str, Any]:
        obs = self._normalize_obs(personal_state)
        
        with torch.no_grad():
            policy_out = self.actor(obs).squeeze(0)
        
        requested = policy_out[0].item() * 500.0 + random.uniform(-50, 100)
        intent_coop = policy_out[1].item()
        intent_uplift = policy_out[2].item()
        total = intent_coop + intent_uplift + 0.1
        intent = {
            "collective_thrive": intent_coop / total,
            "uplift_others": intent_uplift / total,
            "exploratory": 0.1 / total
        }
        
        return {
            "agent_id": self.agent_id,
            "action": {
                "type": "request_powrush",
                "requested": max(10.0, requested),
                "intent": intent
            }
        }
    
    def learn_from_outcome(
        self,
        reward: float,
        mercy_feedback: Dict[str, Any],
        current_state: Dict[str, Any],
        next_state: Dict[str, Any]
    ) -> str:
        obs = self._normalize_obs(current_state)
        next_obs = self._normalize_obs(next_state)
        
        value = self.critic(obs)
        next_value = self.critic(next_obs)
        
        shaped_reward = reward + mercy_feedback.get("amplification", 0.0) * 2.0
        if "Compassionate Redistribution" in mercy_feedback.get("feedback", ""):
            shaped_reward += 100.0
        
        advantage = shaped_reward + self.gamma * next_value - value
        
        # Actor loss
        policy_out = self.actor(obs)
        actor_loss = -torch.log(policy_out.sum() + 1e-8) * advantage.detach()
        
        # Critic loss
        critic_target = shaped_reward + self.gamma * next_value.detach()
        critic_loss = nn.MSELoss()(value, critic_target)
        
        # Updates
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()
        
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()
        
        # Update thrive metric (for evolutionary selection)
        allocation = mercy_feedback.get("allocated", 0.0)
        self.thrive_metric = allocation + shaped_reward + mercy_feedback.get("amplification", 0.0) * 10
        
        return f"Agent {self.agent_id} evolved: Advantage {advantage.item():.1f}"
    
    @classmethod
    def evolve_population(cls, agents: List['ThrivingAgent'], top_k: int = 3, mutation_rate: float = 0.1):
        """Post-quest evolutionary selection/mutation"""
        sorted_agents = sorted(agents, key=lambda a: a.thrive_metric, reverse=True)
        top_parents = sorted_agents[:top_k]
        
        new_pop = []
        for _ in range(len(agents)):
            parent = random.choice(top_parents)
            child = copy.deepcopy(parent)
            for param in child.actor.parameters():
                param.data += mutation_rate * torch.randn_like(param.data)
            for param in child.critic.parameters():
                param.data += mutation_rate * torch.randn_like(param.data)
            new_pop.append(child)
        
        return new_pop
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "strategy_bias": self.strategy_bias,
            "thrive_metric": self.thrive_metric
        }
