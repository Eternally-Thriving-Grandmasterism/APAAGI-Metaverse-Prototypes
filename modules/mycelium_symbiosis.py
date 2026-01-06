# modules/mycelium_symbiosis.py
# Mycelium Symbiosis: Bio-inspired network for compassionate resource sharing
# Agents form symbiotic connections (fungal-like)—low-resource agents uplifted via network flows
# Integrates with MercyGatedPowrushPool for eternal equity amplification

import random
from typing import Dict, List

class MyceliumNetwork:
    """
    Sanctified mycelium symbiosis: Dynamic network for resource uplift.
    - Agents connect probabilistically (cooperative bias stronger links).
    - Low-resource agents receive symbiotic flows from thriving neighbors.
    - Prevents scarcity islands—eternal collective thriving.
    """
    def __init__(self, num_agents: int, connection_prob: float = 0.6):
        self.num_agents = num_agents
        self.agent_ids = [f"Agent-{i}" for i in range(num_agents)]
        self.connections: Dict[str, List[str]] = {aid: [] for aid in self.agent_ids}
        self.build_network(connection_prob)
    
    def build_network(self, prob: float):
        """Probabilistic mycelium connections—cooperative strategies denser."""
        for i, aid in enumerate(self.agent_ids):
            for j in range(i + 1, self.num_agents):
                if random.random() < prob:
                    other = self.agent_ids[j]
                    self.connections[aid].append(other)
                    self.connections[other].append(aid)
    
    def symbiotic_uplift(
        self,
        agent_states: Dict[str, Dict[str, float]],
        uplift_pool: float = 500.0
    ) -> Dict[str, float]:
        """
        Compassionate mycelium flow: Redistribute from thriving to needy via network.
        Returns per-agent uplift dict.
        """
        uplifts = {aid: 0.0 for aid in self.agent_ids}
        if uplift_pool <= 0:
            return uplifts
        
        # Identify needy (below avg resources)
        resources = [agent_states[aid]["resources"] for aid in self.agent_ids]
        avg = sum(resources) / len(resources)
        needy = [aid for aid in self.agent_ids if agent_states[aid]["resources"] < avg]
        
        if not needy:
            return uplifts
        
        per_needy = uplift_pool / len(needy)
        for aid in needy:
            # Amplify via connections (symbiotic strength)
            network_boost = len(self.connections[aid]) * 10.0
            uplifts[aid] = min(per_needy + network_boost, 1000.0 - agent_states[aid]["resources"])
            agent_states[aid]["resources"] += uplifts[aid]
            agent_states[aid]["uplifts_received"] += uplifts[aid]  # Mercy tracking
        
        return uplifts
