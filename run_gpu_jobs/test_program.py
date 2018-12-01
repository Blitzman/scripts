import argparse
import torch

parser_ = argparse.ArgumentParser(description="Parameters")
parser_.add_argument("-p","--p", nargs="?", type=int, help="<Required> Parameter", required=True)
args_ = parser_.parse_args()

print(args_.p)
print(torch.cuda.get_device_name(0))