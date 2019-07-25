FROM debian:latest

RUN apt-get update && \ 
  apt-get install -y python-flask bsdmainutils openjdk-8-jre


# SETUP public_mm
ADD context/data/public_mm_linux_main_*.tar.bz2 /opt/    
RUN cd /opt/public_mm && \ 
    ./bin/install.sh

# ADDITIONAL DATA SOURCES 
ADD context/data/public_mm_data*.tar.bz2 /opt/
#COPY context/data/* /opt/

#RUN cd /opt && \ 
#    tar xvfj public_mm_data_usabase_2018aa_base.tar.bz2 && \ 
#    tar xvfj public_mm_data_usabase_2018aa_relaxed.tar.bz2 && \ 
#    tar xvfj public_mm_data_dblexicon_2018.tar.bz2 && \
#    rm public_mm_data_usabase_2018aa_base.tar.bz2 public_mm_data_usabase_2018aa_relaxed.tar.bz2 public_mm_data_dblexicon_2018.tar.bz2


RUN echo 'export PATH=$PATH:/opt/public_mm/bin' >> ~/.bashrc

# Setup scripts 
WORKDIR /root

RUN mkdir bin 



COPY context/run.sh /root/bin/run.sh
COPY context/crosswalk.sh /root/bin/crosswalk.sh
COPY context/MetaMapServer /root/bin/MetaMapServer

RUN mkdir /opt/UMLS
COPY context/data/MRCONSO.RRF /opt/UMLS/MRCONSO.RRF

RUN chmod +x /root/bin/run.sh /root/bin/MetaMapServer/metamapServer.py

RUN echo 'export PATH=$PATH:/root/bin/:/root/bin/MetaMapServer' >> ~/.bashrc
RUN echo 'export MRCONSO=/opt/UMLS/MRCONSO.RRF' >> ~/.bashrc


VOLUME /root/bin


CMD /root/bin/run.sh
