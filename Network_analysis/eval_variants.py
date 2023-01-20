import pandas as pd

class compare_vars:
    def __init__(self, genes, variants: str):
        """
        Input the scored genes and a list of genes with significant variants
        :param genes: pd.DataFram with already scored genes from disease and aging
        :param vars: list of genes with significant variants
        """
        self.genes = genes
        self.variants = variants

    def load_data(self):
        """
        Load data
        :return: Dataframe with scored genes and list of mutated genes
        """
        scored_genes = self.genes
        variants = pd.read_csv(self.variants, header=None)[0].to_list()
        return scored_genes, variants


    def score_vars(self):
        """
        Score variants only if the variant is in a age AND disease related gene
        :return: updated dataframe
        """
        scored_genes,variants=self.load_data()
        for var in variants:
            if var in scored_genes.index:
                if (scored_genes.loc[var]["is_age"] == "Age related" and scored_genes.loc[var]["is_disease"] == "Disease related"):
                    scored_genes.at[var,'score'] = scored_genes.loc[var]["score"] + 1
                    scored_genes.at[var, 'is_variant'] = "Variant related to Age AND Disease"
                else:
                    scored_genes.at[var, 'is_variant'] = "Variant NOT related to Age AND Disease"
            else:
                pass

        scored_genes["is_variant"] = scored_genes["is_variant"].fillna("No variants")
        return scored_genes

