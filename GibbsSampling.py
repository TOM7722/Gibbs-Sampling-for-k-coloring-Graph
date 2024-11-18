import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm


def gibbs_balayage_random(G, num_colors, n):
    count = {}
    totalColorSet = set(range(num_colors))

    for i in tqdm(range(n), desc=f"k={num_colors}", leave=True):

        j = random.choice(list(G.nodes()))

        colorSet = set()
        for neighbor in G.neighbors(j):
            colorSet.add(G.nodes[neighbor]['color'])

        available_colors = totalColorSet - colorSet

        if available_colors:
            G.nodes[j]['color'] = random.choice(list(available_colors))

        couleurs_string = ''.join(str(G.nodes[node]['color'])
                                  for node in sorted(G.nodes()))
        count[couleurs_string] = count.get(couleurs_string, 0) + 1

    return count

def gibbs_balayage_systemique(G, num_colors, n):
    count = {}
    totalColorSet = set(range(num_colors))
    for i in tqdm(range(n), desc=f"k={num_colors}", leave=True):
        for j in range(1,G.number_of_nodes() + 1):
            colorSet = set()
            for neighbor in G.neighbors(j):
                colorSet.add(G.nodes[neighbor]['color'])

            available_colors = totalColorSet - colorSet

            if available_colors:
                G.nodes[j]['color'] = random.choice(list(available_colors))

            couleurs_string = ''.join(str(G.nodes[node]['color'])
                                      for node in sorted(G.nodes()))
            count[couleurs_string] = count.get(couleurs_string, 0) + 1

    return count

def execute_gibbs_for_k(G, k, n):
    G_copy = G.copy()
    return k, gibbs_balayage_systemique(G_copy, k, n)

def k_coloring(k_start, k_end, iteration):
    count = Parallel(n_jobs=-1)(
        delayed(execute_gibbs_for_k)(
            G,
            k,
            iteration * 2**(k - k_start + 1)
        ) for k in range(k_start, k_end)
    )

    results = {k: len(colorings) for k, colorings in dict(count).items()}
    return results

def plot_graph(G):
    plt.figure(figsize=(10, 10))
    nx.draw(G, with_labels=True)
    plt.show()


G = nx.Graph()

G.add_edges_from([(1, 2), (1, 4), (1, 5), (3, 5), (4, 5)])

num_colors = 4

initial_coloring = {
    1: 1,
    2: 0,
    3: 0,
    4: 0,
    5: 2
}

for node, color in initial_coloring.items():
    G.nodes[node]['color'] = color

plot_graph(G)

results = k_coloring(4, 12, 2000)

df = pd.DataFrame(list(results.items()), columns=['k', 'Nombre de coloriages'])

plt.figure(figsize=(10, 6))
plt.bar(df['k'], df['Nombre de coloriages'], color='b', alpha=0.6)
plt.xlabel('Nombre de couleurs (k)')
plt.ylabel('Nombre de coloriages différents')
plt.title('Nombre de coloriages différents par nombre de couleurs')

for i, v in enumerate(df['Nombre de coloriages']):
    plt.text(df['k'][i], v, str(v), ha='center', va='bottom')

plt.xticks(df['k'])
plt.show()
