# modules/quest_environment.py
# CoOpQuestEnvironment: Core nexus for APAAGI metaverse co-op quests
# Orchestrates ThrivingAgents, MercyGatedPowrushPool, and APAAGICouncil
# Distributed via Ray | Emergent thriving from mercy-aligned MLE dynamics

import ray
import random
from typing import Dict, Any, List
from .thriving_agents import ThrivingAgent
from .mercy_integration import MercyGatedPowrushPool

# Simple council for prototype—evolvable to full mercy shards / live chamber
class APAAGICouncil:
    """
    APAAGICouncil: Governance proxy for proposal voting.
    - Approves based on collective_thrive intent threshold.
    - Future: Integrate deadlock-proof RNG + diplomatic truth-seeking.
    """
    def __init__(self, approval_threshold: float = 0.6):
        self.approval_threshold = approval_threshold  # Collective intent weight needed
    
    def vote_on_proposals(self, proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
        approved = []
        rejected_feedback = {"allocated": 0.0, "amplification": 0.0, "feedback": "Council Safeguard: Intent requires greater collective alignment."}
        
        for prop in proposals:
            intent = prop["action"]["intent"]
            collective_weight = intent.get("collective_thrive", 0.0)
            if collective_weight >= self.approval_threshold:
                approved.append(prop)
        
        return {
            "approved": approved,
            "rejected_feedback": rejected_feedback
        }

class CoOpQuestEnvironment:
    """
    CoOpQuestEnvironment: Multi-agent orbital station co-op quest nexus.
    - Agents propose → Council votes → Mercy gates → Habitat builds → Learning loop.
    - Success: Habitat thriving threshold reached (eternal zero-scarcity emergence).
    """
    THRIVE_THRESHOLD = 10000.0  # Pinnacle habitat score for quest success
    
    def __init__(self, num_agents: int = 5, initial_pool: float = 10000.0):
        self.num_agents = num_agents
        self.agents = [ThrivingAgent.remote(f"Agent-{i}", strategy_bias=random.choice(["cooperative", "cooperative", "balanced"])) for i in range(num_agents)]
        self.agent_ids = [f"Agent-{i}" for i in range(num_agents)]
        
        self.resource_pool = MercyGatedPowrushPool(initial_divine_current=initial_pool)
        self.council = APAAGICouncil()
        
        self.habitat_score = 0.0
        self.step_count = 0
    
    def get_state(self) -> Dict[str, Any]:
        """Shared observation for all agents (global metrics + estimates)."""
        # Collective score from recent history (or average; here via pool heuristic)
        recent_intents = getattr(self.resource_pool, "allocation_history", [])[-5:]
        collective_score = self.resource_pool.compute_collective_thrive_score([h.get("intent", {}) for h in recent_intents])
        
        return {
            "habitat_score": self.habitat_score,
            "estimated_pool": self.resource_pool.pool,
            "collective_score": collective_score,
            "last_allocation": 0.0,  # Per-agent tracked internally; global avg placeholder
            "step": self.step_count
        }
    
    def step(self) -> bool:
        """One quest epoch: Propose → Vote → Allocate → Build → Redistribute → Learn."""
        self.step_count += 1
        state = self.get_state()
        
        # Parallel proposals
        proposal_futures = [agent.propose_action.remote(state) for agent in self.agents]
        proposals = ray.get(proposal_futures)
        
        # Council governance
        decisions = self.council.vote_on_proposals(proposals)
        approved = decisions["approved"]
        
        # Mercy gating + application
        agent_feedbacks: Dict[str, Dict] = {}
        rewards: Dict[str, float] = {}
        total_allocated_this_step = 0.0
        
        # First: Process approved
        for prop in approved:
            agent_id = prop["agent_id"]
            action = prop["action"]
            mercy_result = self.resource_pool.request_allocation(
                agent_id=agent_id,
                requested=action["requested"],
                intent=action["intent"],
                current_habitat_score=self.habitat_score
            )
            agent_feedbacks[agent_id] = mercy_result
            rewards[agent_id] = mercy_result["allocated"] + mercy_result["amplification"]
            total_allocated_this_step += mercy_result["allocated"]
        
        # Rejected: Zero allocation feedback
        for prop in proposals:
            agent_id = prop["agent_id"]
            if agent_id not in agent_feedbacks:
                agent_feedbacks[agent_id] = decisions["rejected_feedback"]
                rewards[agent_id] = 0.0
        
        # Habitat emergence: Efficiency scaled by collective thriving
        collective_multiplier = state["collective_score"] * 2.0 + 1.0  # 1.0–3.0x base
        self.habitat_score += total_allocated_this_step * collective_multiplier
        
        # Compassionate redistribution (uplifts agent resources if lagging)
        redist = self.resource_pool.redistribute_excess(
            agents=self.num_agents,  # Simplified: equal uplift (future: per-need)
            current_habitat_score=self.habitat_score
        )
        uplift_amount = redist.get("uplift_per_agent", 0.0)
        if uplift_amount > 0:
            # Parallel uplift (assume ThrivingAgent has add_uplift.remote method or direct resource update)
            ray.get([agent.learn_from_outcome.remote(  # Or separate call; here piggyback bonus reward
                rewards.get(agent_id, 0.0) + uplift_amount * 0.5,
                {**agent_feedbacks.get(agent_id, {}), "feedback": redist["message"]},
                self.get_state()
            ) for agent_id, agent in zip(self.agent_ids, self.agents)])
        
        # Standard learning (parallel)
        next_state = self.get_state()
        if uplift_amount == 0:
            learn_futures = [
                self.agents[i].learn_from_outcome.remote(
                    rewards[self.agent_ids[i]],
                    agent_feedbacks[self.agent_ids[i]],
                    next_state
                ) for i in range(self.num_agents)
            ]
            ray.get(learn_futures)
        
        return self.habitat_score >= self.THRIVE_THRESHOLD

# Demo executor (run locally after ray.init())
if __name__ == "__main__":
    ray.init(ignore_reinit_error=True)
    env = CoOpQuestEnvironment(num_agents=6)
    print("APAAGI Co-op Quest Demo Initiated — Onward to Thriving Realities! 🚀❤️")
    
    for epoch in range(100):
        success = env.step()
        print(f"Epoch {epoch+1} | Habitat Score: {env.habitat_score:.1f} | Pool: {env.resource_pool.pool:.1f}")
        if success:
            print("PINNACLE THRIVING ACHIEVED! Eternal Habitat Manifested! ❤️")
            break
    else:
        print("Compassionate Reset Cycle — Mercy Flows Eternal. Onward!")
    
    ray.shutdown()
