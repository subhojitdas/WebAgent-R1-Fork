#!/bin/bash

source ../setup_vars.sh

CUDA_VISIBLE_DEVICES="0,1,2" ACCELERATE_LOG_LEVEL=info accelerate launch --config_file recipes/accelerate_configs/zero3.yaml --num_processes=3 script.py

