import os
import sys

DUCKY_ROOT = sys.prefix
DUCKY_POND = os.path.join(DUCKY_ROOT, "pond")
DUCKY_NEST = os.path.join(DUCKY_ROOT, "nest")

os.makedirs(DUCKY_POND, exist_ok=True)
os.makedirs(DUCKY_NEST, exist_ok=True)