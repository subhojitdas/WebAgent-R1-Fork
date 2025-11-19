```
Remove:

	accelerate
	compressed-tensors
	deepspeed
	outlines
	peft
	verifiers
	xformers
	flash-attn
	vllm
	trl
	- torch
	- torch==2.5.1+cu124
	- torchvision==0.20.1+cu124
	- torchaudio==2.5.1+cu124
	- flash-attn==2.7.4.post1




pip install --index-url https://download.pytorch.org/whl/cu124   "torch==2.6.0" "torchvision==0.21.0" "torchaudio==2.6.0"



pip install -U "transformers>=4.56.1,<5" \
               "trl==0.24.0" \
               "accelerate>=1.10.0" \
               "peft>=0.17.0" \
               "tokenizers>=0.19.0" "safetensors>=0.4.3" "sentencepiece" "Pillow"


Getting error on ImportError: /home/<>/miniconda/envs/verifiers-new/lib/python3.11/site-packages/torch/lib/libtorch_cuda.so: undefined symbol: ncclCommRegister

pip install -U "nvidia-cuda-runtime-cu12>=12.4,<13" \
               "nvidia-cudnn-cu12>=9,<10" \
               "nvidia-nccl-cu12>=2.21,<2.24"

export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:${LD_LIBRARY_PATH}"


pip3 install deepspeed

pip install vllm

Error: from trl.import_utils import is_rich_available

cd to Eval 
pip install -e .

Error: liger-kernel version mismatch issue.

pip install --upgrade 'liger-kernel-nightly'

python - <<'PY'
import transformers
print("transformers:", transformers.__version__)
from liger_kernel.transformers import AutoLigerKernelForCausalLM
print("liger import OK")
PY


Error:
ImportError: FlashAttention2 has been toggled on, but it cannot be used due to the following error: the package flash_attn seems to be not installed. Please refer to the documentation of https://huggingface.co/docs/transformers/perf_infer_gpu_one#flashattention-2 to install Flash Attention 2.


pip install --upgrade pip setuptools wheel ninja packaging
pip install flash-attn --no-build-isolation

Build flash-attn from source:

pip install --no-cache-dir --upgrade pip packaging ninja

# make sure the build uses your CUDA 12.9
export CUDA_HOME=/usr/local/cuda-12.9
export CUDACXX=$CUDA_HOME/bin/nvcc
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:${LD_LIBRARY_PATH}

# target your GPU arch (g5 A10G => 8.6)
export TORCH_CUDA_ARCH_LIST="8.6"

# compile using torch headers in this env (no build isolation!)
pip install --no-build-isolation --no-cache-dir "flash-attn==2.8.3"


Run the VLM server in the GPU 3

export CUDA_VISIBLE_DEVICES=7

python3 -m vllm.entrypoints.openai.api_server   --model Qwen/Qwen2.5-VL-7B-Instruct   --host 0.0.0.0 --port 8000   --gpu-memory-utilization 0.90   --dtype bfloat16   --max-model-len 8192


trl vllm-serve \
  --model Qwen/Qwen2.5-VL-7B-Instruct \
  --host 0.0.0.0 --port 8000 \
  --dtype bfloat16 \
  --tensor-parallel-size 1 \
  --max_model_len 5120 \
  --gpu_memory_utilization 0.90


curl -I http://localhost:8000/get_world_size/

curl -I http://localhost:8000/init_communicator


curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "Qwen/Qwen2.5-VL-7B-Instruct",
        "messages": [{"role":"user","content":"Define Q learning"}]
      }'



nvidia-smi pmon -s um



sudo apt-get install libatk1.0-0\
libatk-bridge2.0-0\
libcups2\
libatspi2.0-0\
libxcomposite1\
libxdamage1\
libxfixes3\
libxrandr2\
libgbm1\
libpango-1.0-0\
libasound2
```

With QWen2.5-3B-Instruct , it did not work in g5.48xlarge machine