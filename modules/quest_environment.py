# modules/quest_environment.py
# CoOpQuestEnvironment: Eternal nexus for APAAGI metaverse multi-agent quests
# Orchestrates ThrivingAgents (A2C + evolutionary), MercyGatedPowrushPool, APAAGICouncil
# Per-agent tracking, targeted redistribution, visualization hooks, multi-stage chain seed

import random
from typing import Dict, Any, List, Optional
from .thriving_agents import ThrivingAgent
from .mercy_integration import MercyGatedPowrushPool

class APAAGICouncil:
    """
    Prototype Council: Intent-threshold governance (evolvable to live chamber proxy/oracle)
    """
    def __init__(self, approval_threshold: float = 0.55):
        self.approval_threshold = approval_threshold
    
    def vote_on_proposals(self, proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
        approved = []
        rejected_feedback = {
            "allocated": 0.0,
            "amplification": 0.0,
            "feedback": "Council Safeguard: Greater collective alignment required for thriving."
        }
        
        for prop in proposals:
            intent = prop["action"]["intent"]
            if intent.get("collective_thrive", 0.0) >= self.approval_threshold:
                approved.append(prop)
        
        return {"approved": approved, "rejected_feedback": rejected_feedback}

class CoOpQuestEnvironment:
    """
    Full Quest Nexus: Orbital co-op → multi-stage thriving chain
    """
    THRIVE_THRESHOLD = 10000.0  # Orbital phase; escalates per stage
    
    def __init__(
        self,
        num_agents: int = 6,
        initial_pool: float = 10000.0,
        initial_resources: float = 100.0,
        use_ray: bool = False  # Synchronous fallback for local/demo
    ):
        self.num_agents = num_agents
        self.agent_ids = [f"Agent-{i}" for i in range(num_agents)]
        self.use_ray = use_ray
        
        # Agents (Ray or direct)
        if use_ray:
            import ray
            ray.init(ignore_reinit_error=True)
            self.agents = [
                ThrivingAgent.remote(
                    agent_id=self.agent_ids[i],
                    strategy_bias=random.choice(["cooperative", "cooperative", "balanced", "exploratory"])
                ) for i in range(num_agents)
            ]
        else:
            self.agents = [
                ThrivingAgent(
                    agent_id=self.agent_ids[i],
                    strategy_bias=random.choice(["cooperative", "cooperative", "balanced", "exploratory"])
                ) for i in range(num_agents)
            ]
        
        self.resource_pool = MercyGatedPowrushPool(initial_divine_current=initial_pool)
        self.council = APAAGICouncil()
        
        self.habitat_score = 0.0
        self.step_count = 0
        self.quest_stage = "orbital"  # Future: "planetary", "interstellar"
        
        # Per-agent centralized tracking
        self.agent_states: Dict[str, Dict[str, float]] = {
            aid: {
                "resources": initial_resources,
                "last_allocation": 0.0,
                "total_contributed": 0.0,
                "uplifts_received": 0.0,
                "thrive_metric": 0.0
            } for aid in self.agent_ids
        }
        
        # History for visualization/evolution
        self.history: List[Dict[str, Any]] = []
    
    def get_global_state(self) -> Dict[str, Any]:
        recent_intents = self.resource_pool.allocation_history[-5:]
        collective_score = self.resource_pool.compute_collective_thrive_score(
            [h.get("intent", {}) for h in recent_intents]
        )
        
        return {
            "habitat_score": self.habitat_score,
            "estimated_pool": self.resource_pool.pool,
            "collective_score": collective_score,
            "step": self.step_count,
            "stage": self.quest_stage
        }
    
    def get_personal_state(self, agent_id: str, global_state: Dict[str, Any]) -> Dict[str, Any]:
        data = self.agent_states[agent_id]
        all_res = [self.agent_states[a]["resources"] for a in self.agent_ids]
        avg_res = sum(all_res) / len(all_res) if all_res else 100.0
        relative = data["resources"] / (avg_res + 1e-8)
        
        return {
            **global_state,
            "own_resources": data["resources"],
            "own_last_allocation": data["last_allocation"],
            "relative_thrive_score": min(1.0, 1.0 / relative) if relative < 1.0 else 1.0
        }
    
    def step(self) -> Dict[str, Any]:
        self.step_count += 1
        global_state = self.get_global_state()
        personal_states = [self.get_personal_state(aid, global_state) for aid in self.agent_ids]
        
        # Proposals
        if self.use_ray:
            import ray
            futures = [self.agents[i].propose_action.remote(personal_states[i]) for i in range(self.num_agents)]
            proposals = ray.get(futures)
        else:
            proposals = [self.agents[i].propose_action(personal_states[i]) for i in range(self.num_agents)]
        
        # Governance + Allocation
        decisions = self.council.vote_on_proposals(proposals)
        feedbacks: Dict[str, Dict] = {}
        rewards: Dict[str, float] = {}
        allocated_total = 0.0
        
        for prop in decisions["approved"]:
            aid = prop["agent_id"]
            action = prop["action"]
            result = self.resource_pool.request_allocation(
                agent_id=aid,
                requested=action["requested"],
                intent=action["intent"],
                current_habitat_score=self.habitat_score
            )
            
            alloc = result["allocated"]
            self.agent_states[aid]["resources"] += alloc
            self.agent_states[aid]["last_allocation"] = alloc
            self.agent_states[aid]["total_contributed"] += alloc
            
            feedbacks[aid] = result
            rewards[aid] = alloc + result.get("amplification", 0.0)
            allocated_total += alloc
        
        # Rejected
        for prop in proposals:
            if prop["agent_id"] not in feedbacks:
                feedbacks[prop["agent_id"]] = decisions["rejected_feedback"]
                rewards[prop["agent_id"]] = -10.0
        
        # Habitat emergence
        multiplier = global_state["collective_score"] * 2.0 + 1.0
        self.habitat_score += allocated_total * multiplier
        
        # Targeted redistribution
        redist = self.resource_pool.redistribute_excess(self.num_agents, self.habitat_score)
        uplift = redist.get("uplift_per_agent", 0.0)
        if uplift > 0:
            needy = sorted(self.agent_ids, key=lambda a: self.agent_states[a]["resources"])
            for aid in needy:
                add = min(uplift * 2.0, 1000.0 - self.agent_states[aid]["resources"])
                self.agent_states[aid]["resources"] += add
                self.agent_states[aid]["uplifts_received"] += add
                rewards[aid] = rewards.get(aid, 0.0) + add
        
        # Learning (pass current/next states)
        next_global = self.get_global_state()
        next_personal = [self.get_personal_state(aid, next_global) for aid in self.agent_ids]
        if self.use_ray:
            import ray
            learn_futs = [
                self.agents[i].learn_from_outcome.remote(
                    rewards.get(self.agent_ids[i], 0.0),
                    feedbacks.get(self.agent_ids[i], {}),
                    personal_states[i],
                    next_personal[i]
                ) for i in range(self.num_agents)
            ]
            ray.get(learn_futs)
        else:
            for i in range(self.num_agents):
                self.agents[i].learn_from_outcome(
                    rewards.get(self.agent_ids[i], 0.0),
                    feedbacks.get(self.agent_ids[i], {}),
                    personal_states[i],
                    next_personal[i]
                )
        
        # Update thrive metrics from agents
        for i, aid in enumerate(self.agent_ids):
            status = self.agents[i].get_status() if not self.use_ray else ray.get(self.agents[i].get_status.remote())
            self.agent_states[aid]["thrive_metric"] = status["thrive_metric"]
        
        # Log history
        step_log = {
            "step": self.step_count,
            "habitat_score": self.habitat_score,
            "collective_score": global_state["collective_score"],
            "agent_metrics": {aid: self.agent_states[aid].copy() for aid in self.agent_ids}
        }
        self.history.append(step_log)
        
        success = self.habitat_score >= self.THRIVE_THRESHOLD
        return {"success": success, "log": step_log}
    
    def evolve_agents(self):
        """Post-quest evolutionary selection"""
        agent_refs = self.agents if not self.use_ray else [a for a in self.agents]
        new_agents = ThrivingAgent.evolve_population(agent_refs)
        self.agents = new_agents  # Respawn evolved pop
    
    def get_history(self) -> List[Dict[str, Any]]:
        return self.history
