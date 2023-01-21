#!/usr/local/bin/python
import argparse
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import build_net
import centrality
import eval_genes
import eval_variants
import integrate_score
import fetch_drugs

parser = argparse.ArgumentParser(description="Network analysis for iNET from AGen")
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument("-i", "--input_genes",
                           help="csv containing list of DE genes and LogFC")
requiredNamed.add_argument("-v", "--variants",
                           help="txt containing list of genes with variants")
requiredNamed.add_argument("-n", "--name",
                           help="sample name")
# GeneName, logFC
args = parser.parse_args()


#genes="Data/test_DEG.csv"
#variants="Data/T4D_genes_BIMinput.txt"
genes = args.input_genes
variants = args.variants
name = args.name
disease="/var/sarcopenia_disgenet.csv"
age="/var/aging_atlas.csv"
string_db="/var/string_v11-high_conf.csv"

# Score genes by correlation with aging and disease
scored_genes = eval_genes.compare_genes(genes=genes, age=age,disease=disease)
scored_genes = scored_genes.get_scores()
score_vars = eval_variants.compare_vars(scored_genes, variants)
scored_genes = score_vars.score_vars()

# Build network
net = build_net.build_network(genes=genes, string_db=string_db)
network = net.create()

# Score centrality
score_centrality = centrality.centrality(network=network, genes=genes)
score_centrality = score_centrality.integrate_expression()

# Include all scores

integrate= integrate_score.integrate(scored_genes,score_centrality)
scored_genes = integrate.integrate_score()

# fetch drugs

fetch = fetch_drugs.fetch_drugs(network,scored_genes)
scored_genes=fetch.fetch_interactions()

filename = name+"_scored_genes.csv"
scored_genes.to_csv(filename,index_label="GeneName")

# Assign scores to nodes
scored_genes = scored_genes.to_dict("index")
nx.set_node_attributes(network, scored_genes)

# export network


network_js = nx.cytoscape_data(network)
filename = name+"_network_jnode.json"

with open(filename, 'w') as outfile:
    json.dump(network_js, outfile)

network_js = nx.cytoscape_data(network)

with open('Data/network_jnode.json', 'w') as outfile:
    json.dump(network_js, outfile)

# Plot graph, select color of the nod if age or disease related
#f = plt.figure()
<<<<<<< HEAD
#nx.draw_kamada_kawai(network, node_size=list(node_weight),node_color=is_age, width=0.2, alpha=0.7)
=======
#nx.draw_kamada_kawai(network, node_size=list(node_weight),node_color=is_disease, width=0.2, alpha=0.7)
>>>>>>> network_viz
#plt.show()
#f.savefig("graph.png")
