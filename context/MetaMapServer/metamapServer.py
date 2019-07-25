#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, json, time, pdb, logging, re, subprocess, commands
from flask import Flask, render_template, request, g
from subprocess import Popen, PIPE, check_output,CalledProcessError
from time import sleep
import xml.etree.ElementTree as ET
app = Flask(__name__)

reload(sys)
sys.setdefaultencoding('utf-8')
defOpts = '-Z 2018AA -V USAbase --relaxed_model --restrict_to_sources SNOMEDCT_US  -I --XMLf'

@app.route('/')
def index():
    return showIndexPage()

@app.route('/crosswalk', methods=['GET', 'POST'])
def crosswalk():
    if request.method == 'GET': 
        return render_template('crosswalk.html')
    if request.method == 'POST':
        if not 'data' in request.form:
            return "Please provide a data field.\n Provided data:" + str(request.form)
        else: 
            inpt  = request.form['data']
            output = processCrossWalk(inpt)
            return '\n'.join(output)

@app.route('/metamaphuman', methods=['GET', 'POST'])
def metamaphuman():
    if request.method == 'GET': 
        g.opts = defOpts
        g.input = ""
        return render_template('concepts.html')
    if request.method == 'POST':
        results = processRequest()
        g.results = getResults(results)
        g.opts = request.form['options']
        g.input = request.form['data']
        return render_template('concepts.html')
        
@app.route('/metamap', methods=['POST'])
def metamap():
    if request.method == 'GET': 
        return showInputForm()
    if request.method == 'POST':
      logging.info("METAMAP")
      return processRequest()

def processRequest():
    if not 'data' in request.form:
        return "Please provide a data field.\n Provided data:" + str(request.form)
    inpt  = request.form['data']
    tm = str(getTime())
    inputName = '/tmp/document_'+tm+'.txt'
    
    inpt = inpt.decode('unicode-escape').encode('ascii', 'ignore').decode()

    with open(inputName, 'w') as f:
        f.write(inpt)
        f.write('\n')
    
    
    outpt = '/tmp/result_'+tm+'.txt' 
    
    
    opt = defOpts
    if 'options' in request.form and request.form['options'] != '':
        opt = request.form['options']
    call  = ['metamap', opt, inputName, outpt]
    logging.info('Running MetaMap on file '+str(inputName)+'\n - Saving output to: '+str(outpt)+'\n - Options: '+str(opt))

    try:
        process = Popen(call, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        logging.debug("STDERR:")
        for line in process.stderr: 
            logging.debug(line)
        process.wait()
    except CalledProcessError:
        return '\nThere is something wrong with MetaMap..\n\n'
    
    result = open(outpt).read()
    logging.debug('Result ' + str(result))
    os.remove(inputName)
    os.remove(outpt)
    
    return result 
    
def processCrossWalk(concept):
    r, output = commands.getstatusoutput("crosswalk.sh " + concept)
    return output.split()

def showIndexPage():
    return '''
        <h1>Welcome to MetaMap Docker</h1>
        <p>Available services: </p>
        <ul>
            <li><a href="metamaphuman">MetaMap Tagger service</a> - Find medical concepts in a given text. </li>
            <li><a href="crosswalk">Crosswalk service</a> - Find corresponding snomed ids for given UMLS CUIs. </li>
        </ul>
    '''



def getResults(xml): 
    root = ET.fromstring(xml)    
    results = []
    for phrase in root.findall('.//Phrase'):
        for candidate in phrase.findall('./Mappings/Mapping/MappingCandidates/Candidate'):
            cui = candidate.find('./CandidateCUI').text
            label = candidate.find('./CandidatePreferred').text
            phraseText =  phrase.find('./PhraseText').text
            snomedids = processCrossWalk(cui)
            if len(snomedids) == 0:
                results.append({'cui': cui, 'label': label, 'snomedid': 'not found', 'phrase': phraseText})
            else:
                for snomedid in processCrossWalk(cui):
                    results.append({'cui': cui, 'label': label, 'snomedid': snomedid, 'phrase': phraseText})
    uniqR = {v['cui']:v for v in results}.values()
    return uniqR
    



def getTime():
    millis = int(round(time.time()))
    return millis

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host='0.0.0.0', port=80)
    
