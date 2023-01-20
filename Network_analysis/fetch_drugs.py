import networkx as nx
import pandas as pd
import json
import requests

import warnings
warnings.filterwarnings("ignore")


class fetch_drugs():
    def __init__(self, network, scored_genes):
        """
        Fetch gene interaction with FDA approved drugs from www.dgidb.org/
        :param network:list of genes composing the network
        """
        self.genes=list(network.nodes)
        self.scored_genes=scored_genes

    def fetch_interactions(self):
        self.scored_genes["drugs"] = ""
        for gene in self.genes:
            url = f'https://dgidb.org/api/v2/interactions.json?genes={gene}&fda_approved_drug=true'
            data = requests.get(url)
            drugs = json.loads(data.text)["matchedTerms"]
            try:
                drugs = pd.json_normalize(drugs, record_path=['interactions']).drugName.tolist()
                self.scored_genes.at[gene, 'drugs'] = drugs
            except Exception:
                pass

        return self.scored_genes