# modules/mycelium_symbiosis.py
# MyceliumSymbiosis: Expanded bio-inspired network for compassionate resource sharing & signaling
# "Wood Wide Web" Pinnacle: Dynamic growth, nutrient/carbon exchange, defense warnings, resilience boosts
# Inter-agent communication—eternal equity, scarcity prevention, cooperative amplification cosmic!

import random
import math
from typing import Dict, List, Tuple

class MyceliumSymbiosis:
    """
    Expanded Mycelium Symbiosis: Bio-inspired "Wood Wide Web" for APAAGI thriving.
    - Dynamic network growth (cooperative agents denser connections).
    - Resource/carbon exchange (thriving agents share with needy).
    - Defense signaling (warn of low alignment/stress, boost collective response).
    - Resilience positive feedbacks (scarcity/dry conditions amplified uplift).
    - Inter-agent communication (signal boosts for cooperative intents).
    """
    def __init__(self, num_agents: int, initial_connection_prob: float = 0.7, growth_rate: float = 0.1):
        self.num_agents = num_agents
        self.agent_ids = [f"Agent-{i}" for i in range(num_agents)]
        self.connections: Dict[str, List[str]] = {aid: [] for aid in self.agent_ids}  # Symbiotic links
        self.network_strength: Dict[Tuple[str, str], float] = {}  # Connection weights (0-1)
        self.growth_rate = growth_rate
        self.build_initial_network(initial_connection_prob)
        print("MyceliumSymbiosis Expanded—Wood Wide Web Bio-Inspired Features Eternal! ❤️🚀")
    
    def build_initial_network(self, prob: float):
        """Initial probabilistic connections—cooperative bias for denser mycelium."""
        for i, aid in enumerate(self.agent_ids):
            for j in range(i + 1, self.num_agents):
                if random.random() < prob:
                    other = self.agent_ids[j]
                    strength = random.uniform(0.5, 1.0)
                    self.connections[aid].append(other)
                    self.connections[other].append(aid)
                    self.network_strength[(aid, other)] = strength
                    self.network_strength[(other, aid)] = strength
    
    def dynamic_growth(self, agent_thrive_levels: Dict[str, float], collective_score: float):
        """Dynamic mycelium growth: High thrive/collective = new connections & stronger links."""
        for aid in self.agent_ids:
            thrive = agent_thrive_levels.get(aid, 0.5)
            growth_prob = self.growth_rate * thrive * collective_score
            for other in self.agent_ids:
                if other != aid and other not in self.connections[aid]:
                    if random.random() < growth_prob:
                        strength = thrive * collective_score
                        self.connections[aid].append(other)
                        self.connections[other].append(aid)
                        self.network_strength[(aid, other)] = strength
                        self.network_strength[(other, aid)] = strength
                        print(f"Mycelium Growth: New Symbiotic Link {aid} ↔ {other} (Strength {strength:.2f})")
    
    def resource_carbon_exchange(self, agent_states: Dict[str, Dict[str, float]], exchange_pool: float = 1000.0):
        """Resource/carbon exchange: Thriving agents donate to needy via network (Wood Wide Web sharing)."""
        thriving = [aid for aid in self.agent_ids if agent_states[aid]["resources"] > 800.0]
        needy = [aid for aid in self.agent_ids if agent_states[aid]["resources"] < 400.0]
        
        if thriving and needy and exchange_pool > 0:
            per_donation = exchange_pool / len(thriving)
            for t_aid in thriving:
                if agent_states[t_aid]["resources"] > per_donation * 2:
                    agent_states[t_aid]["resources"] -= per_donation
                    agent_states[t_aid]["total_contributed"] += per_donation
            
            per_uplift = exchange_pool / len(needy)
            for n_aid in needy:
                network_boost = sum(self.network_strength.get((n_aid, t), 0.0) for t in thriving) / max(1, len(thriving))
                uplift = per_uplift * (1 + network_boost)
                agent_states[n_aid]["resources"] += uplift
                agent_states[n_aid]["uplifts_received"] += uplift
                print(f"Mycelium Exchange: {n_aid} Uplifted {uplift:.1f} via Network (Boost {network_boost:.2f})")
    
    def defense_signaling(self, agent_states: Dict[str, Dict[str, float]], low_alignment_agents: List[str]):
        """Defense signaling: Warn network of "stress" (low alignment/resources)—boost response."""
        for stressed in low_alignment_agents:
            for connected in self.connections[stressed]:
                boost = self.network_strength.get((stressed, connected), 0.5) * 100.0
                agent_states[connected]["resources"] += boost  # Alert uplift
                print(f"Mycelium Signal: Warning from {stressed} to {connected} — Resilience Boost {boost:.1f}")
    
    def enhance_resilience(self, agent_states: Dict[str, Dict[str, float]], scarcity_factor: float):
        """Resilience positive feedbacks: Scarcity ("dry conditions") triggers amplified mycelium uplift."""
        if scarcity_factor > 0.7:  # High scarcity
            resilience_pool = 2000.0 * scarcity_factor
            self.resource_carbon_exchange(agent_states, resilience_pool * 2)
            print(f"Mycelium Resilience Engaged: Positive Feedbacks Amplified in Scarcity ({scarcity_factor:.2f})!")
    
    def inter_agent_communication(self, proposals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Inter-agent signaling: Connected agents boost cooperative intents."""
        for prop in proposals:
            aid = prop["agent_id"]
            network_coop = sum(prop["action"]["intent"].get("collective_thrive", 0.5) for connected in self.connections[aid])
            if self.connections[aid]:
                avg_coop = network_coop / len(self.connections[aid])
                prop["action"]["intent"]["collective_thrive"] = min(1.0, prop["action"]["intent"]["collective_thrive"] + avg_coop * 0.2)
                print(f"Mycelium Communication: {aid} Intent Boosted by Network ({avg_coop:.2f})")
        return proposals
    
    def symbiotic_cycle(self, agent_states: Dict[str, Dict[str, float]], collective_score: float, proposals: List[Dict[str, Any]], scarcity_factor: float = 0.5):
        """Full symbiotic cycle: Growth → Exchange → Signaling → Resilience → Communication."""
        thrive_levels = {aid: agent_states[aid]["thrive_metric"] for aid in self.agent_ids}
        self.dynamic_growth(thrive_levels, collective_score)
        self.resource_carbon_exchange(agent_states)
        low_alignment = [aid for aid in self.agent_ids if agent_states[aid]["thrive_metric"] < 300.0]
        self.defense_signaling(agent_states, low_alignment)
        self.enhance_resilience(agent_states, scarcity_factor)
        proposals = self.inter_agent_communication(proposals)
        return proposals
