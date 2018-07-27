import os
import sys
from os import listdir
from os.path import isfile, join, isdir
import ROOT
from CombineHarvester.CombineTools.plotting import *

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

cwd = os.getcwd()
onlydirs = ['shapes_em_HighMass',
            'shapes_em_LowMass']
massPoints =[]
count =0 
for mydir in onlydirs:
    if 'LowMass' in mydir:
        massPoints=[200, 300, 450]
    else:
        massPoints=[450, 600, 750, 900]

    for mass in massPoints:
        #if count == 1 : sys.exit(0)
        print 'current dir 1', join(cwd,mydir)
        os.chdir( join(cwd,mydir))
        print 'current dir 2', os.getcwd()
        dirname = join(os.getcwd(),str(mass))
        print dirname
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        print os.getcwd()
        cmd='mv *%s* %s/' %(str(mass),str(mass))
        os.system(cmd)
        print join(cwd,mydir,str(mass))
        os.chdir(join(cwd,mydir,str(mass)))
        
        if 'le1' in mydir:
            os.system("combineTool.py -M T2W -i lfv_em_1_13TeV_%s.txt  -o lfv_em_1_13TeV.root --parallel 4 -m %s" %(str(mass)))
        else:
            os.system("ln -s ../../diffNuisances.py .")
            os.system("echo '\n\n\n'")
            os.system("echo 'fitting %s, %s GeV, 0 jet,  bkg only'" %(mydir, str(mass)))
            os.system("combine -M MaxLikelihoodFit -t -1 --expectSignal 0 lfv_em_1_13TeV.root --rMax 5.  -m %s > diagnostic_1_B_%s.txt" %(str(mass), str(mass)))
            os.system("mv combine_logger.out combine_logger_1_B.out")
            os.system("mv higgsCombineTest.MaxLikelihoodFit.mH%s.root higgsCombineTest_1_B.MaxLikelihoodFit.mH%s.root" %(str(mass), str(mass)))
            os.system("mv fitDiagnostics.root fitDiagnostics_1_B.root")
            os.system("echo '\n\n\n'")
            os.system("echo  'fitting %s, %s GeV, 1 jet,  bkg only' " %(mydir, str(mass)))
            os.system("combine -M MaxLikelihoodFit -t -1 --expectSignal 0 lfv_em_2_13TeV.root --rMax 5.  -m %s > diagnostic_2_B_%s.txt" %(str(mass),str(mass)))
            os.system("mv combine_logger.out combine_logger_2_B.out")
            os.system("mv higgsCombineTest.MaxLikelihoodFit.mH%s.root higgsCombineTest_2_B.MaxLikelihoodFit.mH%s.root" %(str(mass), str(mass)))
            os.system("mv fitDiagnostics.root fitDiagnostics_2_B.root")
            os.system("echo '\n\n\n'")
            os.system("echo 'fitting %s, %s GeV, combined,  bkg only' "%(mydir, str(mass)))
            os.system("combine -M MaxLikelihoodFit -t -1 --expectSignal 0 lfv_em_13TeV.root --rMax 5.  -m %s > diagnostic_B_%s.txt "%(str(mass),str(mass)) )
            os.system("mv combine_logger.out combine_logger_B.out")
            os.system("mv higgsCombineTest.MaxLikelihoodFit.mH%s.root higgsCombineTest_B.MaxLikelihoodFit.mH%s.root" %(str(mass), str(mass)))
            os.system("mv fitDiagnostics.root fitDiagnostics_B.root")
        
            os.system("python diffNuisances.py -a fitDiagnostics_1_B.root -g plots_1_B.root -f text > diffNuisances_B_1_%s_%s" %(mydir, str(mass)))
            os.system("python diffNuisances.py -a fitDiagnostics_2_B.root -g plots_2_B.root -f text > diffNuisances_B_2_%s_%s" %(mydir, str(mass)))
            os.system("python diffNuisances.py -a fitDiagnostics_B.root -g plots_B.root -f text > diffNuisances_B_%s_%s" %(mydir, str(mass)))
 
            os.system("echo '\n\n\n'")
            os.system("echo 'fitting %s, %s GeV, 0 jet,  sig+bkg'" %(mydir, str(mass)))
            os.system("combine -M MaxLikelihoodFit -t -1 --expectSignal 1 lfv_em_1_13TeV.root --rMax 5. -m %s > diagnostic_1_S_%s.txt" %(str(mass),str(mass)))
            os.system("mv combine_logger.out combine_logger_1_S.out")
            os.system("mv higgsCombineTest.MaxLikelihoodFit.mH%s.root higgsCombineTest_1_S.MaxLikelihoodFit.mH%s.root" %(str(mass), str(mass)))
            os.system("mv fitDiagnostics.root fitDiagnostics_1_S.root")

            os.system("echo '\n\n\n'")
            os.system("echo 'fitting %s, %s GeV, 1 jet,  sig+bkg'" %(mydir, str(mass)))
            os.system("combine -M MaxLikelihoodFit -t -1 --expectSignal 1 lfv_em_2_13TeV.root --rMax 5.  -m %s > diagnostic_2_S_%s.txt" %(str(mass), str(mass)))
            os.system("mv combine_logger.out combine_logger_2_S.out")
            os.system("mv higgsCombineTest.MaxLikelihoodFit.mH%s.root higgsCombineTest_2_S.MaxLikelihoodFit.mH%s.root" %(str(mass), str(mass)))
            os.system("mv fitDiagnostics.root fitDiagnostics_2_S.root")
            os.system("combine -M MaxLikelihoodFit -t -1 --expectSignal 1 lfv_em_13TeV.root --rMax 5.  -m %s > diagnostic_S_%s.txt"%(str(mass),str(mass)) )
         
            os.system("echo '\n\n\n'")
            os.system("echo 'fitting %s, %s GeV, combined,  sig+bkg' " %(mydir, str(mass)))
            os.system("python diffNuisances.py -a fitDiagnostics_1_S.root -g plots_1_S.root -f text > diffNuisances_S_1_%s_%s" %(mydir, str(mass)))
            os.system("python diffNuisances.py -a fitDiagnostics_2_S.root -g plots_2_S.root -f text > diffNuisances_S_2_%s_%s" %(mydir, str(mass)))
            os.system("python diffNuisances.py -a fitDiagnostics.root -g plots.root -f text > diffNuisances_S_%s_%s" %(mydir, str(mass)))


            

    os.chdir(join(cwd,mydir))
 
    count+=1
