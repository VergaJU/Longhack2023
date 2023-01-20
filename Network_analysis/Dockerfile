FROM python:3.8.10

WORKDIR /app


COPY requirements.txt requirements.txt 

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Include all python code
COPY Network/ /usr/bin
RUN chmod +x /usr/bin/*
# Include age-related genes
COPY Data/ /var

# default arguments to run test
ENV INPUT=/var/test_DEG.csv
ENV VARIANTS=/var/T4D_genes_BIMinput.txt
ENV NAME=testrun

# there is no need to use parameters array
CMD main.py -i ${INPUT} -v ${VARIANTS} -n ${NAME}