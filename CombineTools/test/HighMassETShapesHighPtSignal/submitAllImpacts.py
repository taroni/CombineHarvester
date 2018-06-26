import os

masses=['200', '300', '450', '450_HM', '600', '750', '900']
startdir = os.path.abspath(os.getcwd())

for mass in masses:
    sh = """#!/bin/bash
            export W_DIR="""+startdir+"""
            export CFG="""+startdir+"""/computeBlindImpacts_"""+mass+""".py
            cd $W_DIR
            eval `scram runtime -sh`
            python $CFG
            exit
    """
    #scrive script
    sh_file = open("impacts-"+mass+".sh","w")
    sh_file.write(sh)
    sh_file.close()

    #sottomette script
    os.popen("chmod a+x impacts-"+mass+".sh")
    os.popen("bsub -q cmscaf1nd impacts-"+mass+".sh" )
    
