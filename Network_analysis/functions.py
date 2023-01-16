import networkx as nx
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class network_analysis:
    def __init__(self, genes: str):
        '''

        :param genes: path to DE genes output from pipeline
        '''
        self.genes=genes
    def read_genes(self):
        '''
        Read the csv path and store the data in a pandas dataframe
        Then CHECK IF THE STRUCTURE IS CORRECT (index name, first columns)
        :return: pandas dataframe with genes and logFC
        :return: list of genes to fetch network
        '''
        data = pd.read_csv(self.genes)
        if ("gene" not in data.columns or "log2FoldChange" not in data.columns ):
            print("Wrong csv format")
            return pd.DataFrame()
        else:
            genes = data.gene.to_list()
            genes = '%0d'.join(genes)
            return data, genes

    def fetch_network(self):
        '''
        from the list of genes fetch the network
        :return: network (tsv?)
        '''
        data, genes = read_genes()
        url = 'https://string-db.org/api/tsv/network?identifiers=' + genes + '&species=9606'
        r = requests.get(url)
        print(r)