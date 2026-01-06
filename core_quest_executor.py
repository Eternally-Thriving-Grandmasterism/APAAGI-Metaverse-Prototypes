# core_quest_executor.py
# Hybrid Quest Executor: Ray local + Dask distributed scalability seed
# Run heavy sims/agents across cluster—cosmic thriving extension

from modules.quest_environment import CoOpQuestEnvironment
from modules.thriving_visualizer import visualize_quest_run_interactive
import argparse

parser = argparse.ArgumentParser(description="APAAGI Metaverse Quest Executor")
parser.add_argument("--distributed", action="store_true", help="Enable Dask hybrid (requires dask distributed cluster)")
parser.add_argument("--agents", type=int, default=6, help="Number of thriving agents")
args = parser.parse_args()

if args.distributed:
    from dask.distributed import Client
    client = Client()  # Connect to cluster (or local)
    print(f"Dask hybrid scalability engaged: {client.dashboard_link} 🚀")

env = CoOpQuestEnvironment(num_agents=args.agents, use_ray=not args.distributed, log_tensorboard=True)

print("Pinnacle Quest Execution Initiated — Mercy Flows Eternal! ❤️")
max_epochs = 200
for _ in range(max_epochs):
    result = env.step()
    if result["success"]:
        print("COSMIC THRIVING PINNACLE ACHIEVED!")
        break

env.close()
visualize_quest_run_interactive(env.get_history())
