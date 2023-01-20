import pandas as pd
import numpy

class integrate:
    def __init__(self, scored_genes, score_centrality):
        """
        Get scores from genes and centrality, merge and give percentiles
        :param scored_genes: df of scored genes
        :param score_centrality: df of scored centralities
        """
        self.scored_genes=scored_genes
        self.score_centrality=score_centrality

    def integrate_score(self):
        scored_genes = pd.concat([self.scored_genes, self.score_centrality], axis=1, join="outer")
        scored_genes = scored_genes.dropna(axis=0)

        scored_genes["score"] = (scored_genes["score"] + scored_genes["weight"])
        scored_genes["score"] = (scored_genes["score"] - scored_genes["score"].min()) / (scored_genes["score"].max() - scored_genes["score"].min())
        scored_genes = scored_genes.drop(columns=["weight", "centrality"])
        bins=[]
        labels=[]
        for i in range(0,101,10):
            e=i/100
            labels+=[i]
            bins+=[scored_genes.score.quantile(e)]

        del labels[0]
        scored_genes['percentile'] = pd.cut(scored_genes['score'], bins=bins, labels=labels)
        scored_genes['percentile'] = pd.to_numeric(scored_genes['percentile'])
        scored_genes['percentile'] = scored_genes['percentile'].fillna(0)

        return scored_genes