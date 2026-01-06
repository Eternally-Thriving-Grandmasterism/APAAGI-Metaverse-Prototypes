# modules/quest_environment.py (updated with per-agent tracking)
import ray
import random
from typing import Dict, Any, List
from .thriving_agents import ThrivingAgent
from .mercy_integration import MercyGatedPowrushPool

class APAAGICouncil:  # Unchanged for prototype...

class CoOpQuestEnvironment:
    THRIVE_THRESHOLD = 10000.0
    
    def __init__(self, num_agents: int = 6, initial_pool: float = 10000.0, initial_resources: float = 100.0):
        self.num_agents = num_agents
        self.agent_ids = [f"Agent-{i}" for i in range(num_agents)]
        self.agents = [
            ThrivingAgent.remote(
                agent_id=self.agent_ids[i],
                strategy_bias=random.choice(["cooperative", "cooperative", "balanced", "exploratory"])
            ) for i in range(num_agents)
        ]
        
        self.resource_pool = MercyGatedPowrushPool(initial_divine_current=initial_pool)
        self.council = APAAGICouncil(approval_threshold=0.55)  # Slightly lowered for emergent testing
        
        self.habitat_score = 0.0
        self.step_count = 0
        
        # Per-agent state tracking (central authority)
        self.agent_states: Dict[str, Dict[str, float]] = {
            agent_id: {
                "resources": initial_resources,
                "last_allocation": 0.0,
                "total_contributed": 0.0
            } for agent_id in self.agent_ids
        }
    
    def get_global_state(self) -> Dict[str, Any]:
        recent_intents = getattr(self.resource_pool, "allocation_history", [])[-5:]
        collective_score = self.resource_pool.compute_collective_thrive_score([h.get("intent", {}) for h in recent_intents])
        
        return {
            "habitat_score": self.habitat_score,
            "estimated_pool": self.resource_pool.pool,
            "collective_score": collective_score,
            "step": self.step_count
        }
    
    def get_personal_state(self, agent_id: str, global_state: Dict[str, Any]) -> Dict[str, Any]:
        agent_data = self.agent_states[agent_id]
        all_resources = [self.agent_states[aid]["resources"] for aid in self.agent_ids]
        avg_resources = sum(all_resources) / len(all_resources) if all_resources else 100.0
        relative_thrive = agent_data["resources"] / (avg_resources + 1e-8)  # >1.0 = thriving above avg
        
        return {
            **global_state,
            "own_resources": agent_data["resources"],
            "own_last_allocation": agent_data["last_allocation"],
            "relative_thrive_score": min(1.0, 1.0 / relative_thrive) if relative_thrive < 1.0 else 1.0  # Higher if needy
        }
    
    def step(self) -> bool:
        self.step_count += 1
        global_state = self.get_global_state()
        
        # Personalized states for parallel proposals
        personal_states = [self.get_personal_state(agent_id, global_state) for agent_id in self.agent_ids]
        
        # Parallel proposals with personal awareness
        proposal_futures = [self.agents[i].propose_action.remote(personal_states[i]) for i in range(self.num_agents)]
        proposals = ray.get(proposal_futures)
        
        # Council + Mercy processing (unchanged structure)
        decisions = self.council.vote_on_proposals(proposals)
        approved = decisions["approved"]
        
        agent_feedbacks: Dict[str, Dict] = {}
        rewards: Dict[str, float] = {}
        total_allocated_this_step = 0.0
        
        for prop in approved:
            agent_id = prop["agent_id"]
            action = prop["action"]
            mercy_result = self.resource_pool.request_allocation(
                agent_id=agent_id,
                requested=action["requested"],
                intent=action["intent"],
                current_habitat_score=self.habitat_score
            )
            allocated = mercy_result["allocated"]
            
            # Per-agent updates
            self.agent_states[agent_id]["resources"] += allocated
            self.agent_states[agent_id]["last_allocation"] = allocated
            self.agent_states[agent_id]["total_contributed"] += allocated  # For future metrics
            
            agent_feedbacks[agent_id] = mercy_result
            rewards[agent_id] = mercy_result["allocated"] + mercy_result["amplification"]
            total_allocated_this_step += allocated
        
        # Rejected handling...
        for prop in proposals:
            if prop["agent_id"] not in agent_feedbacks:
                agent_feedbacks[prop["agent_id"]] = decisions["rejected_feedback"]
                rewards[prop["agent_id"]] = -10.0  # Mild penalty for learning
        
        # Habitat build (collective multiplier)
        collective_multiplier = global_state["collective_score"] * 2.0 + 1.0
        self.habitat_score += total_allocated_this_step * collective_multiplier
        
        # Targeted compassionate redistribution (uplift lowest-resource agents)
        redist = self.resource_pool.redistribute_excess(
            agents=self.num_agents,
            current_habitat_score=self.habitat_score
        )
        uplift_amount = redist.get("uplift_per_agent", 0.0)
        if uplift_amount > 0:
            # Prioritize needy: Sort by resources ascending
            needy_agents = sorted(self.agent_ids, key=lambda aid: self.agent_states[aid]["resources"])
            for agent_id in needy_agents:
                uplift = min(uplift_amount * 2.0, 500.0 - self.agent_states[agent_id]["resources"])  # Cap sensible
                self.agent_states[agent_id]["resources"] += uplift
                rewards[agent_id] = rewards.get(agent_id, 0.0) + uplift
        
        # Learning loop (with updated next personal states)
        next_global = self.get_global_state()
        next_personal = [self.get_personal_state(aid, next_global) for aid in self.agent_ids]
        learn_futures = [
            self.agents[i].learn_from_outcome.remote(
                rewards.get(self.agent_ids[i], 0.0),
                agent_feedbacks.get(self.agent_ids[i], {}),
                next_personal[i]
            ) for i in range(self.num_agents)
        ]
        ray.get(learn_futures)
        
        return self.habitat_score >= self.THRIVE_THRESHOLD
