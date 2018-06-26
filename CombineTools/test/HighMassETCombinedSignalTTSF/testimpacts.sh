#!/bin/bash

#$DIR="MyDir/"
#$CARD="mycard.txt"

#combineCards.py -S $DIR$CARD > card.txt


text2workspace.py  HMuTau_mutaue_combined_2016_bbb_m125_colmass_goldenjson_36fb.txt -m 125

combineTool.py -M Impacts -d HMuTau_mutaue_combined_2016_bbb_m125_colmass_goldenjson_36fb.root -m 125 --doInitialFit --robustFit 1 --rMax 5 --rMin -5 -t -1

combineTool.py -M Impacts -d HMuTau_mutaue_combined_2016_bbb_m125_colmass_goldenjson_36fb.root -m 125 --robustFit 1 --doFits   --rMax 5 --rMin -5  -t -1 --parallel 30

combineTool.py -M Impacts -d HMuTau_mutaue_combined_2016_bbb_m125_colmass_goldenjson_36fb.root -m 125 -o "mutaue_colmass_impactsbbb.json"
plotImpacts.py -i "mutaue_colmass_impactsbbb.json" -o mutaue_colmass_impactsbbb

