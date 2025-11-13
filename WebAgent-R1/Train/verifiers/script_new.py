# script.py
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3,4,5,6,7"
os.environ.setdefault("ACCELERATE_LOG_LEVEL", "info")
# os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True,max_split_size_mb:64")
# Tell Accelerate to use DeepSpeed + your config file:
# os.environ["ACCELERATE_USE_DEEPSPEED"] = "true"
# os.environ["ACCELERATE_CONFIG_FILE"] = "recipes/accelerate_configs/zero3.yaml"

import multiprocessing as mp
if mp.get_start_method(allow_none=True) != "spawn":
    mp.set_start_method("spawn", force=True)

from accelerate import notebook_launcher, DeepSpeedPlugin  # safe (light import, no CUDA init)

def worker():

    # All heavy imports happen *inside* the worker:
    from accelerate import Accelerator
    import torch

    grad_accum = 1

    ds_plugin = DeepSpeedPlugin(
        zero_stage=3,                     # from zero_stage: 3
        offload_optimizer_device="none",  # offload_optimizer_device: none
        offload_param_device="none",      # offload_param_device: none
        zero3_init_flag=True,             # zero3_init_flag: true
        zero3_save_16bit_model=True,      # zero3_save_16bit_model: true
        gradient_accumulation_steps=grad_accum
    )

    import verifiers as vf
    from verifiers.trainers import GRPOEnvTrainer
    from verifiers.utils import get_default_grpo_config
    from verifiers.envs.webarena_env import WebArenaEnv

    # mixed_precision: bf16
    acc = Accelerator(
        mixed_precision="bf16",
        deepspeed_plugin=ds_plugin
    )

    acc.print(f"[rank {acc.process_index}/{acc.num_processes}] device={acc.device}")

    model_name = "Qwen/Qwen2.5-3B-Instruct"
    model, tokenizer = vf.get_model_and_tokenizer(model_name)

    TASK = "webarena-lite"
    vf_env = WebArenaEnv(dataset=TASK, max_steps=15, n_contexts=4)

    dataset = vf_env.get_dataset()
    eval_dataset = vf_env.get_eval_dataset()
    rubric = vf_env.get_rubric()

    training_args = get_default_grpo_config(
        run_name=f"{TASK}_GRPO/Standard/" + model_name.split("/")[-1].lower(),
        num_gpus=8,
    )

    trainer = GRPOEnvTrainer(
        model=model,
        processing_class=tokenizer,
        reward_funcs=rubric,
        env=vf_env,
        args=training_args,
        train_dataset=dataset,
    )

    trainer.train()
    acc.print("done.")

if __name__ == "__main__":
    # Note: nothing above this line should import torch or your model code.
    notebook_launcher(worker, num_processes=8)
