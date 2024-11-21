# Graph Coloring using Gibbs Sampling

This project implements graph coloring algorithms using Gibbs sampling techniques to explore different possible colorings of a graph. It uses both systematic and random sampling approaches to estimate the number of possible k-colorings for different values of k.

## Overview

The code uses Gibbs sampling, a Markov Chain Monte Carlo (MCMC) method, to sample different valid colorings of a graph. It implements two sampling strategies:

- Systematic Gibbs sampling: Visits nodes in sequential order
- Random Gibbs sampling: Randomly selects nodes to update

The main goal is to estimate how many different valid k-colorings exist for a given graph as k increases.

## Important Note
This implementation provides an estimation rather than an exact count of all possible colorings. The algorithm does not guarantee finding all valid colorings, and the accuracy depends heavily on the number of iterations. 

## Requirements

```python
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm
from scipy import stats
