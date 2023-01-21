# Visualization web-server

build the container and:

```
# test file
docker run --network host network_viz
# With you outputs from iNET network analysis
docker run --network host -e NETWORK=yournetwork -e DATA=yourscoredgenes network_viz

```