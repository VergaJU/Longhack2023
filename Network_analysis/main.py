import argparse
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import build_net
import centrality
import eval_genes

parser = argparse.ArgumentParser(description="Network analysis for iNET from AGen")
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument("-i", "--input_genes",
                           help="csv containing list of DE genes and LogFC")
requiredNamed.add_argument("-d", "--disease",
                           help="csv containing list of disease associated genes")
args = parser.parse_args()


genes="Data/DGE.csv"
disease="Data/sarcopenia_disgenet.csv"
age="Data/aging_atlas.csv"
string_db="Data/string_v11-high_conf.csv"

# Score genes by correlation with aging and disease
scored_genes = eval_genes.compare_genes(genes=genes, age=age,disease=disease)
scored_genes = scored_genes.get_scores()

# Build network
net = build_net.build_network(genes=genes, string_db=string_db)
network = net.create()

# Score centrality
score_centrality = centrality.centrality(network=network, genes=genes)
score_centrality = score_centrality.integrate_expression()

# Include all scores
scored_genes = pd.concat([scored_genes, score_centrality.rename('centrality')], axis=1, join="outer")
scored_genes = scored_genes.dropna(axis=0)

scored_genes["score"] = (scored_genes["score"] + scored_genes["centrality"])/2
scored_genes = scored_genes.drop(columns=["centrality"])
scored_genes.to_csv("Data/scored_genes.csv")

# Assign scores to nodes
scored_genes = scored_genes.to_dict("index")
nx.set_node_attributes(network, scored_genes)

# plotting functions
node_weight = list(nx.get_node_attributes(network, 'score').values())
node_weight = np.array(node_weight)*50

age_dict = {"Not Age related":0, "Age related": 1}
is_age = list(nx.get_node_attributes(network, 'is_age').values())
is_age = [age_dict.get(item, item) for item in is_age]

disease_dict = {"Not Disease related":0, "Disease related": 1}
is_disease = list(nx.get_node_attributes(network, 'is_disease').values())
is_disease = [disease_dict.get(item, item) for item in is_disease]

# Plot graph, select color of the nod if age or disease related
f = plt.figure()
nx.draw_kamada_kawai(network, node_size=list(node_weight),node_color=is_disease, width=0.2, alpha=0.7)
plt.show()
#f.savefig("graph.png")
