import networkx as nx
import pandas as pd


class build_network:
    def __init__(self, genes: str, string_db:str):
        '''

        :param genes: path to DE genes output from pipeline
        '''
        self.genes=genes
        self.string_db=string_db


    def read_data(self):
        '''
        Read the csv path and store the data in a pandas dataframe
        Then CHECK IF THE STRUCTURE IS CORRECT (index name, first columns)
        :return: pandas dataframe with genes and logFC
        :return: list of genes to fetch network
        '''
        string = pd.read_csv(self.string_db, sep="\t")
        data = pd.read_csv(self.genes)
        if ("GeneName" not in data.columns or "logFC" not in data.columns ):
            print("Wrong csv format")
            return pd.DataFrame()
        else:
            genes = data.GeneName.to_list()
            return string,genes

    def fetch_network(self):
        '''
        Read string db file and import all the connections for the desired genes
        :return: pandas dataframe with connections for genes
        '''
        string, genes = self.read_data()
        # Fetch all the rows in "protein1" with the selected genes
        network1 = string.loc[string['protein1'].isin(genes)]
        # fetch all the rows from the previous network with the selected genes in "protein2"
        # This is needed to select only the interactions between selected genes
        connections = network1.loc[network1['protein2'].isin(genes)]
        return connections

    def create(self):
        '''
        from the df create the networkx object
        :return:networkx object
        '''
        connections = self.fetch_network()
        network = nx.from_pandas_edgelist(connections, "protein1", "protein2")
        return network
