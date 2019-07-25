#!/bin/bash

source /root/.bashrc

skrmedpostctl start
wsdserverctl start
python /root/bin/MetaMapServer/metamapServer.py
