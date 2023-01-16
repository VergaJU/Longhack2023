FROM ubuntu:20.04

# don't freeze pls
ENV TZ=Europe/Dublin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update --fix-missing && apt-get install -y\
    wget

#Download and install SraToolkit
RUN wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.11.3/sratoolkit.2.11.3-ubuntu64.tar.gz
# Unzip the archive
RUN tar xzvf sratoolkit.2.11.3-ubuntu64.tar.gz
ENV PATH=/sratoolkit.2.11.3-ubuntu64/bin:$PATH
RUN vdb-config --restore-defaults
RUN rm -f /root/.ncbi/user-settings.mkfg
ADD user-settings.mkfg /root/.ncbi/user-settings.mkfg
RUN rm -f sratoolkit.2.11.3-ubuntu64.tar.gz
