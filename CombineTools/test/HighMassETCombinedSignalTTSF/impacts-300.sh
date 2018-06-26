#!/bin/bash
            export W_DIR=/afs/cern.ch/work/t/taroni/private/CombineForHighMass/CMSSW_8_1_0/src/CombineHarvester/CombineTools/test/HighMassETCombinedSignalTTSF
            export CFG=/afs/cern.ch/work/t/taroni/private/CombineForHighMass/CMSSW_8_1_0/src/CombineHarvester/CombineTools/test/HighMassETCombinedSignalTTSF/computeBlindImpacts_300.py
            cd $W_DIR
            eval `scram runtime -sh`
            python $CFG
            exit
    