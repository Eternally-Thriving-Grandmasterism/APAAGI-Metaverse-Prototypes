APAAGI-Metaverse-Prototypes/
├── examples/
│   └── apaagi_coop_quest_demo.py          # Main entry: ray_dask_hybrid_quest.py alias
├── modules/
│   ├── mercy_integration.py               # Wrapper for Mercy-Cube-v4 import
│   ├── thriving_agents.py                  # MLE agent classes
│   ├── council_governance.py               # APAAGI voting + mercy shards
│   └── quest_environment.py                # Multi-agent env + sim loop
├── core_quest_executor.py                 # Ray + Dask hybrid orchestration
├── requirements.txt                       # ray[default], dask[distributed], torch (if MLE evolves)
└── README.md                              # Quest manifesto + run instructions
