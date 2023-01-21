FROM python:3.8.10

WORKDIR /app


COPY requirements.txt requirements.txt 

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Include all python code
RUN mkdir Data
COPY Data/ Data/
RUN mkdir assets
COPY assets/ assets/
COPY Procfile .

COPY __init__.py .
COPY main.py .

# default arguments to run test
ENV NETWORK=Data/network_jnode.json
ENV DATA=Data/scored_genes.csv

ENV DASH_DEBUG_MODE True
EXPOSE 8050

# there is no need to use parameters array
CMD python main.py -i ${NETWORK} -d ${DATA}