#!/bin/bash
            export W_DIR=/afs/cern.ch/work/t/taroni/private/CombineForHighMass/CMSSW_8_1_0/src/CombineHarvester/CombineTools/test/HighMassEMShapes
            export CFG=/afs/cern.ch/work/t/taroni/private/CombineForHighMass/CMSSW_8_1_0/src/CombineHarvester/CombineTools/test/HighMassEMShapes/computeBlindImpacts_900.py
            cd $W_DIR
            eval `scram runtime -sh`
            python $CFG
            exit
    