# Network_iNET
 iNET network analysis


Usage:

```
sudo docker build --rm -t network_analysis .
sudo docker run -it -v $(pwd):/app/ -e INPUT=<DEG file> -v VARIANTS=<variants file> -n NAME=<sample name> network_analysis 
```