A docker image containing UMLS MetaMap and CrossMap between CUIs and SNOMED CT.

# Build Instructions: 
Sign up for an UMLS account (https://uts.nlm.nih.gov/home.html).
Then download the following files from UMLS/MetaMap Site and put them into `context/data`

    MRCONSO.RRF (https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)
    public_mm_linux_main_2018.tar.bz2 (https://metamap.nlm.nih.gov/download/public_mm_linux_main_2018.tar.bz2)
    public_mm_data_usabase_2018aa_base.tar.bz2  (https://metamap.nlm.nih.gov/download/DataSets/public_mm_data_base_2018ab_base.tar.bz2) 
    public_mm_data_dblexicon_2018.tar.bz2   (https://metamap.nlm.nih.gov/download/DataSets/public_mm_data_dblexicon_2018.tar.bz2)
    public_mm_data_usabase_2018aa_relaxed.tar.bz2 (https://metamap.nlm.nih.gov/download/DataSets/public_mm_data_base_2018ab_relaxed.tar.bz2)

Execute the following commands: 
 
    docker build --tag metamap .
    docker create -p 80:80 metamap 
    
To run the container use   

    docker start metamap

Now you can visit localhost:80 to get started. 

If using the service from a program, use post requests, e.g. with curl 

    curl -d "data=HIV" -X POST http://localhost:80/metamap
    curl -d "data=C0022885" -X POST http://localhost:80/crosswalk 
    
You can alse provide options using the `options` field.

# Image Structure 

  - /root/bin - contains the tools 
  - /opt/public_mm - contains metamap installation 
  - /opt/MRCONSO.RRF - location of the mapping file
 
 
# Environment Variables

  - MRCONSO: the location of the MRCONSO.RRF file.
