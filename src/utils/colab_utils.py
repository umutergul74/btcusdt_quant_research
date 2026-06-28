import sys
import torch

def check_gpu() -> dict:
    """Checks for GPU availability and returns details."""
    gpu_available = torch.cuda.is_available()
    device_name = torch.cuda.get_device_name(0) if gpu_available else "None"
    return {
        "gpu_available": gpu_available,
        "device_name": device_name,
        "cuda_version": torch.version.cuda if gpu_available else "N/A"
    }

def set_seed(seed: int = 42):
    """Sets random seeds for reproducibility."""
    import random
    import numpy as np
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    print(f"Global seed set to: {seed}")
