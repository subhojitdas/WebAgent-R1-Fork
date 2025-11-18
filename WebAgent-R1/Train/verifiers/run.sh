#!/bin/bash

source ../setup_vars.sh

CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7" ACCELERATE_LOG_LEVEL=info NCCL_TIMEOUT=7200 NCCL_BLOCKING_WAIT=1 NCCL_ASYNC_ERROR_HANDLING=1 accelerate launch --config_file recipes/accelerate_configs/zero2.yaml --num_processes=8 script.py

