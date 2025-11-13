# script.py
import subprocess
import sys
import os

if __name__ == "__main__":
    cmd = [
        "accelerate", "launch",
        "--config_file", "recipes/accelerate_configs/zero3.yaml",
        "--num_processes", "8",
        "script.py"  # separate file with your actual training code
    ]

    env = {
        **os.environ,
        "CUDA_VISIBLE_DEVICES": "0,1,2,3,4,5,6,7",
        "ACCELERATE_LOG_LEVEL": "info",
    }

    subprocess.run(cmd, env=env)