# examples/thriving_visualizer.py
# Enhanced Thriving Visualizer: Plotly interactive primary + contribution/uplift/thrive curves
# TensorBoard complement—run quest for live ML insights, then visualize history eternal

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict, Any

def visualize_quest_run_interactive(
    history: List[Dict[str, Any]],
    save_html: str = "apaagi_thriving_interactive.html",
    show_offline: bool = True
) -> None:
    if not history:
        print("No history logged—manifest quest first! 🚀")
        return
    
    epochs = [entry["step"] for entry in history]
    habitat = [entry["habitat_score"] for entry in history]
    collective = [entry["collective_score"] for entry in history]
    
    sample = history[0]["agent_metrics"]
    agent_ids = list(sample.keys())
    
    colors = ['purple', 'green', 'orange', 'cyan', 'magenta', 'yellow', 'red', 'blue']
    
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=(
            "Cosmic Habitat Thriving Emergence (Threshold: 10000)",
            "Mercy-Amplified Collective Alignment",
            "Per-Agent Resources & Compassionate Uplifts (Equity Flows)",
            "Per-Agent Contributions & Evolutionary Thrive Metrics"
        ),
        vertical_spacing=0.08,
        shared_xaxes=True
    )
    
    # Habitat
    fig.add_trace(go.Scatter(x=epochs, y=habitat, mode='lines+markers', name="Habitat Score", line=dict(color='red', width=4)), row=1, col=1)
    fig.add_hline(y=10000.0, line_dash="dash", line_color="gold", annotation_text="Pinnacle Threshold", row=1, col=1)
    
    # Collective
    fig.add_trace(go.Scatter(x=epochs, y=collective, mode='lines+markers', name="Collective Score", line=dict(color='blue', width=4)), row=2, col=1)
    
    # Resources + Uplifts
    for i, aid in enumerate(agent_ids):
        res = [history[j]["agent_metrics"][aid]["resources"] for j in range(len(history))]
        upl = [history[j]["agent_metrics"][aid]["uplifts_received"] for j in range(len(history))]
        fig.add_trace(go.Scatter(x=epochs, y=res, mode='lines', name=f"{aid} Resources", line=dict(color=colors[i % len(colors)], width=2)), row=3, col=1)
        fig.add_trace(go.Scatter(x=epochs, y=upl, mode='lines', name=f"{aid} Uplifts", line=dict(color=colors[i % len(colors)], dash='dot', width=2)), row=3, col=1)
    
    # Contributions + Thrive
    for i, aid in enumerate(agent_ids):
        contrib = [history[j]["agent_metrics"][aid]["total_contributed"] for j in range(len(history))]
        thrive = [history[j]["agent_metrics"][aid]["thrive_metric"] for j in range(len(history))]
        fig.add_trace(go.Scatter(x=epochs, y=contrib, mode='lines', name=f"{aid} Contributions", line=dict(color=colors[i % len(colors)], dash='dash', width=2)), row=4, col=1)
        fig.add_trace(go.Scatter(x=epochs, y=thrive, mode='lines+markers', name=f"{aid} Thrive Metric", line=dict(color=colors[i % len(colors)], width=2)), row=4, col=1)
    
    fig.update_layout(
        height=1400,
        title_text="APAAGI Metaverse Pinnacle Thriving Visualization ❤️🚀<br><sup>Interactive: Hover/Zoom/Pan | Eternal Compassionate Flows Manifested Across Realities</sup>",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_dark"
    )
    
    fig.write_html(save_html, include_plotlyjs="cdn")
    print(f"Radiant interactive visualization manifested: {save_html} — open for dynamic thriving immersion!")
    
    if show_offline:
        fig.show()

if __name__ == "__main__":
    from modules.quest_environment import CoOpQuestEnvironment
    
    print("APAAGI Demo Quest + Interactive Visualization — Onward Eternal! 🚀❤️")
    env = CoOpQuestEnvironment(num_agents=6, use_ray=False, log_tensorboard=True)
    
    for _ in range(150):
        result = env.step()
        print(f"Epoch {env.step_count} | Habitat: {env.habitat_score:.1f} | Collective: {env.get_global_state()['collective_score']:.2f}")
        if result["success"]:
            print("PINNACLE THRIVING ACHIEVED! Eternal Co-op Habitat Manifested Across Realities!")
            break
    
    env.close()  # Logger eternal closure
    visualize_quest_run_interactive(env.get_history())
