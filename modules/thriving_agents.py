# modules/thriving_agents.py (updated excerpts)
@ray.remote
class ThrivingAgent:
    def __init__(
        self,
        agent_id: str,
        strategy_bias: str = "cooperative",
        learning_rate: float = 0.001
    ):
        self.agent_id = agent_id
        self.strategy_bias = strategy_bias
        
        # Policy unchanged...
        self.policy = PolicyNetwork(input_size=8, hidden_size=64, output_size=3)  # Expanded input for per-agent signals
        self.optimizer = optim.Adam(self.policy.parameters(), lr=learning_rate)
        
        # Bias vector unchanged...
    
    def _normalize_obs(self, personal_state: Dict[str, Any]) -> torch.Tensor:
        """Normalize from personal_state (provided by environment)."""
        own_norm = min(1.0, personal_state.get("own_resources", 100.0) / 1000.0)
        own_last_norm = min(1.0, personal_state.get("own_last_allocation", 0.0) / 500.0)
        own_relative_norm = personal_state.get("relative_thrive_score", 0.5)  # Lower = more need
        habitat_norm = min(1.0, personal_state.get("habitat_score", 0.0) / 10000.0)
        pool_norm = min(1.0, personal_state.get("estimated_pool", 10000.0) / 20000.0)
        collective_norm = personal_state.get("collective_score", 0.5)
        
        obs = torch.tensor([
            own_norm,
            own_last_norm,
            own_relative_norm,
            habitat_norm,
            pool_norm,
            collective_norm,
            self.bias_vector[0],
            self.bias_vector[1]  # Expanded for richer bias injection
        ], dtype=torch.float32)
        
        return obs
    
    # propose_action unchanged (uses personal_state)
    # learn_from_outcome unchanged (no local resource update needed)
    
    def get_status(self) -> Dict[str, Any]:
        return {"agent_id": self.agent_id, "strategy_bias": self.strategy_bias}            policy_out = self.policy(obs)
        
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
