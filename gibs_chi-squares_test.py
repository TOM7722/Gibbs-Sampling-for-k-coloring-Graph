import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
from scipy import stats


def chi_squared_test(counts):
    observed = np.array(list(counts.values()))
    expected = np.full_like(observed, fill_value=np.mean(observed), dtype=float)
    chi2_stat, p_value = stats.chisquare(observed, f_exp=expected)
    return chi2_stat, p_value


def gibbs_balayage_random(G, num_colors, n):
    count = {}
    totalColorSet = set(range(num_colors))

    for i in range(n):

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


def gibbs_balayage_systemique(G, num_colors, n, burn_in):
    count = {}
    totalColorSet = set(range(num_colors))
    for i in range(n):
        for j in range(1,G.number_of_nodes() + 1):
            colorSet = set()
            for neighbor in G.neighbors(j):
                colorSet.add(G.nodes[neighbor]['color'])

            available_colors = totalColorSet - colorSet

            if available_colors:
                G.nodes[j]['color'] = random.choice(list(available_colors))

        if i >= burn_in:
            couleurs_string = ''.join(str(G.nodes[node]['color'])
                                      for node in sorted(G.nodes()))
            count[couleurs_string] = count.get(couleurs_string, 0) + 1

    return count

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

count = gibbs_balayage_systemique(G, num_colors, int(216_000), int(0))
df = pd.DataFrame(list(count.items()), columns=['Couleurs', 'Compte'])
df.to_csv('gibbs.csv', index = False)

chi2_stat, p_value = chi_squared_test(count)
print(f"Statistique du chi-deux : {chi2_stat}")
print(f"P-valeur : {p_value}")


plt.figure(figsize=(10, 6))
plt.scatter(range(len(df)), df['Compte'], color='b', alpha=0.6, s=10)
plt.xlabel('Index (hidden)')
plt.ylabel('Compte')

plt.show()
