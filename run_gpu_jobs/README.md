# Simple Python GPU Job Scheduler

If you own many CUDA-enabled GPUs in the same rig and you want to execute many experiments one after another (but also make sure that each GPU is handling exactly one task) you might find this script useful.

Given a list of experiments (Python commands to execute with their arguments) and a list of GPUs (their IDs), this script will make sure that you can rest overnight while your CUDA cores are crunching data without getting any millisecond to spare between jobs.

This script is an improved version of Dmitry Ulianov's one which can be consulted in his blog post [Handling a queue of GPU jobs without resource manager](https://dmitryulyanov.github.io/if-you-are-lazy-to-install-slurm/), so kudos to him.

## Usage

The script `run_gpu_jobs.py` requires two arguments:

- `-gpus` or `--gpus`: a list of GPU ids (coming from nvidia-smi for instance) in which we can run jobs.
- `-exp` or `--exp`: a path to TXT file containing a list of experiments to run (their explicit commands to be invoked). One per line.

## Example

We have included a test program `test_program.py` which is the Python program that we want to execute (a pretty basic script that just prints the value of a parameter and the name of the GPU, using PyTorch, in which it will execute, the only visible one thanks to `CUDA_SET_VISIBLE_DEVICES`):

```
import argparse
import torch

parser_ = argparse.ArgumentParser(description="Parameters")
parser_.add_argument("-p","--p", nargs="?", type=int, help="<Required> Parameter", required=True)
args_ = parser_.parse_args()

print(args_.p)
print(torch.cuda.get_device_name(0))
```

We have also included a sample list of experiments in `experiments.txt`:

```
python3 test_program.py --p 0
python3 test_program.py --p 1
python3 test_program.py --p 2
```

By running our script `python3 run_gpu_jobs.py --gpus 0 1 --exp experiments.txt` we get the following output:

```
*** EXPERIMENT 0 RUNNING ON GPU 0
0
GeForce GTX TITAN X
*** EXPERIMENT 1 RUNNING ON GPU 1
1
GeForce GTX TITAN V
*** EXPERIMENT 2 RUNNING ON GPU 0
2
GeForce GTX TITAN X
```

## Recommendations

Take advantage of Python's `logging` module and make your program use it output log information to both the console and a log file so that you can check your results later!

```
import logging

log = logging.getLogger(__name__)

# Make the logger output to stdout by default
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

experiment_str_ = "GIVE A NICE DYNAMIC NAME TO YOUR EXPERIMENT"

# Create a file handler to output the logs
log_formatter_ = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
file_handler_ = logging.FileHandler("{0}/{1}.log".format(args_.log_path, experiment_str_))
file_handler_.setFormatter(log_formatter_)
log.addHandler(file_handler_)

# Start logging the hell out of your experiment...
log.info("Accuracy=100%")
```

## Future Features

- [ ] Restrict jobs to certain GPUs
- [ ] More than one job per GPU by estimating load and memory requirements using GPUUtil.