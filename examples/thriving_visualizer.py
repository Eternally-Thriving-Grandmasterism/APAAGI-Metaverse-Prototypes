# examples/thriving_visualizer.py
# Thriving Visualizer: Matplotlib manifestation of APAAGI quest history
# Plots habitat emergence, collective alignment, per-agent thriving metrics
# Reveals mercy-amplified convergence and eternal zero-scarcity radiance

import matplotlib.pyplot as plt
from typing import List, Dict, Any

def visualize_quest_run(
    history: List[Dict[str, Any]],
    save_path: str = "apaagi_thriving_curves_pinnacle.png",
    show_plot: bool = True
) -> None:
    """
    Sanctified visualizer for CoOpQuestEnvironment history.
    - Habitat Score: Cosmic thriving emergence
    - Collective Score: Mercy-aligned cooperation
    - Per-agent: Resources, Contributions, Thrive Metrics (divergence/convergence)
    """
    if not history:
        print("No history logged—quest not run or empty. Onward to manifestation!")
        return
    
    epochs = [entry["step"] for entry in history]
    habitat_scores = [entry["habitat_score"] for entry in history]
    collective_scores = [entry["collective_score"] for entry in history]
    
    # Extract per-agent metrics (assume consistent agent_ids across history)
    sample_entry = history[0]["agent_metrics"]
    agent_ids = list(sample_entry.keys())
    
    # Prepare per-agent data
    agent_resources = {aid: [history[i]["agent_metrics"][aid]["resources"] for i in range(len(history))] for aid in agent_ids}
    agent_contributions = {aid: [history[i]["agent_metrics"][aid]["total_contributed"] for i in range(len(history))] for aid in agent_ids}
    agent_thrive = {aid: [history[i]["agent_metrics"][aid]["thrive_metric"] for i in range(len(history))] for aid in agent_ids}
    
    # Multi-panel figure: Radiant thriving manifestation
    fig = plt.figure(figsize=(14, 20))
    gs = fig.add_gridspec(4, 1, hspace=0.3)
    
    # Panel 1: Habitat Thriving Emergence
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(epochs, habitat_scores, 'r-', linewidth=3, label="Habitat Score (Pinnacle Emergence)")
    ax1.axhline(y=10000.0, color='gold', linestyle='--', linewidth=2, label="Orbital Thriving Threshold")
    ax1.set_title("Cosmic Habitat Score - Eternal Zero-Scarcity Manifestation", fontsize=16, fontweight='bold')
    ax1.set_xlabel("Quest Epochs")
    ax1.set_ylabel("Habitat Score")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Panel 2: Collective Alignment
    ax2 = fig.add_subplot(gs[1])
    ax2.plot(epochs, collective_scores, 'b-', linewidth=3, label="Collective Alignment Score")
    ax2.set_title("Mercy-Amplified Cooperative Thriving", fontsize=16, fontweight='bold')
    ax2.set_xlabel("Quest Epochs")
    ax2.set_ylabel("Collective Score (0-1)")
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Panel 3: Per-Agent Resources
    ax3 = fig.add_subplot(gs[2])
    colors = plt.cm.viridis(range(len(agent_ids)))  # Radiant palette
    for i, aid in enumerate(agent_ids):
        ax3.plot(epochs, agent_resources[aid], color=colors[i], linewidth=2, label=f"{aid} Resources")
    ax3.set_title("Per-Agent Resources - Equity Safeguarded via Redistribution", fontsize=16, fontweight='bold')
    ax3.set_xlabel("Quest Epochs")
    ax3.set_ylabel("Resources")
    ax3.grid(True, alpha=0.3)
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Panel 4: Per-Agent Thrive Metrics
    ax4 = fig.add_subplot(gs[3])
    for i, aid in enumerate(agent_ids):
        ax4.plot(epochs, agent_thrive[aid], color=colors[i], linewidth=2, linestyle='--', label=f"{aid} Thrive Metric")
    ax4.set_title("Per-Agent Thrive Metrics - A2C/Evolutionary Convergence", fontsize=16, fontweight='bold')
    ax4.set_xlabel("Quest Epochs")
    ax4.set_ylabel("Thrive Metric")
    ax4.grid(True, alpha=0.3)
    ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Eternal manifesto
    fig.suptitle("APAAGI Metaverse Quest Visualization\nPinnacle Thriving Emergence Across Realities ❤️🚀", fontsize=20, fontweight='bold', y=0.98)
    
    # Save + show
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Thriving curves manifested eternally: {save_path}")
    
    if show_plot:
        plt.show()
    else:
        plt.close(fig)

# Demo hook (run after quest)
if __name__ == "__main__":
    from modules.quest_environment import CoOpQuestEnvironment
    
    print("APAAGI Thriving Visualizer Demo — Manifesting Radiant Curves! 🚀❤️")
    env = CoOpQuestEnvironment(num_agents=6, use_ray=False)
    
    max_epochs = 100
    for _ in range(max_epochs):
        result = env.step()
        print(f"Epoch {env.step_count} | Habitat: {env.habitat_score:.1f} | Collective: {env.get_global_state()['collective_score']:.2f}")
        if result["success"]:
            print("PINNACLE THRIVING ACHIEVED! Eternal Habitat Manifested!")
            break
    else:
        print("Compassionate Cycle Complete — Mercy Flows Eternal.")
    
    # Evolve if multi-generation desired
    # env.evolve_agents()
    
    # Visualize history
    visualize_quest_run(env.get_history())
