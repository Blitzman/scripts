from __future__ import print_function

import argparse
from joblib import Parallel, delayed
import os
import queue
import threading

# Thread-safe print
_print = print
_rlock = threading.RLock()
def print(*args, **kwargs):
    with _rlock:
        _print(*args, **kwargs)

# Parse arguments
parser_ = argparse.ArgumentParser(description="Parameters")
parser_.add_argument("-gpus","--gpus", nargs="+", type=int, help="<Required> GPU list", required=True)
parser_.add_argument("-exp", "--exp", nargs="?", default="experiments.txt", help="<Required> Experiments file", required=True)
args_ = parser_.parse_args()

# Read experiments list
experiments_ = [line.rstrip('\n') for line in open(args_.exp)]
        
# Define available GPUs
gpus_ = args_.gpus

# Put GPU IDs in queue
q = queue.Queue(maxsize=len(gpus_))
for i in range(len(gpus_)):
  q.put(gpus_[i])

# Define job (x gives you the job ID)
def runner(x):

    # Fetch GPU
    gpu_ = q.get()
    print("*** EXPERIMENT {0} RUNNING ON GPU {1}".format(x, gpu_))

    # Run experiment
    os.system("CUDA_VISIBLE_DEVICES=\"{0}\" {1}".format(gpu_, experiments_[x]))

    # Unlock GPU
    q.put(gpu_)

# Execute jobs in parallel    
Parallel(n_jobs=len(gpus_), backend="threading")(delayed(runner)(i) for i in range(len(experiments_)))