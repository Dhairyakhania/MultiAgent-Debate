import random
import os

def set_global_seed(seed: int | None):
    if seed is None:
        return

    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
