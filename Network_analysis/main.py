import argparse
import functions as fun

parser = argparse.ArgumentParser(description="Network analysis for iNET from AGen")
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument("-i", "--input_genes",
                           help="csv containing list of DE genes and LogFC")
args = parser.parse_args()


define = fun.network_analysis(genes="data/DGE.csv")
define.fetch_network()