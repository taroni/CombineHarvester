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
#onlydirs = ['shapes_pzeta_bveto','shapes_pzeta_noBBB_bveto','shapes_pzeta_nobveto','shapes_pzeta_noBBB_nobveto']
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
            os.system("combineCards.py lfv_em_1_13TeV_%s.txt lfv_em_2_13TeV_%s.txt > lfv_em_13TeV.txt" %(str(mass), str(mass)))
            os.system("combineTool.py -M T2W -i lfv_em_13TeV.txt  -o lfv_em_13TeV.root --parallel 4 -m %s" %(str(mass)))
            os.system("combineTool.py -M T2W -i lfv_em_2_13TeV_%s.txt  -o lfv_em_2_13TeV.root --parallel 4 -m %s" %(str(mass), str(mass)))
            os.system("combineTool.py -M T2W -i lfv_em_1_13TeV_%s.txt  -o lfv_em_1_13TeV.root --parallel 4 -m %s" %(str(mass), str(mass)))
    #os.chdir(join(cwd,mydir))
        
        if 'le1' in mydir:
            os.system("combineTool.py -M AsymptoticLimits -d */lfv_em_1_13TeV_%.root --there -n .limit --parallel 4  --noFitAsimov")
            os.system("combineTool.py -M CollectLimits */*.limit.* --use-dirs -o limits.json")
        else:
            print 'current dir', os.getcwd()
            os.system("combineTool.py -M AsymptoticLimits -d lfv_em_13TeV.root --there  -n .limit --run expected -C 0.95 -t -1  -m %s --parallel 4" %(str(mass) ))
            os.system("combineTool.py -M AsymptoticLimits -d lfv_em_1_13TeV.root --there  -n .limit1 --run expected -C 0.95 -t -1  -m %s --parallel 4" %(str(mass) ))
            os.system("combineTool.py -M AsymptoticLimits -d lfv_em_2_13TeV.root --there  -n .limit2 --run expected -C 0.95 -t -1  -m %s --parallel 4" %(str(mass) ))
           #os.system("combineTool.py -M AsymptoticLimits -d */lfv_em_13TeV.root --there -n .limit --parallel 4  --noFitAsimov --bypassFrequentistFit")
    os.chdir(join(cwd,mydir))

    os.system("combineTool.py -M CollectLimits */*.limit.* --use-dirs -o limits.json")
    os.system("combineTool.py -M CollectLimits */*.limit2.* --use-dirs -o limits2.json")
    os.system("combineTool.py -M CollectLimits */*.limit1.* --use-dirs -o limits1.json")
        #os.systet("combineTool.py -M AsymptoticLimits -d */lfv_em_2_13TeV.root --there -n .limit --parallel 4  --noFitAsimov")
        #os.system("combineTool.py -M CollectLimits */*.limit.* --use-dirs -o limits.json")

    os.chdir(join(cwd,mydir))
    ModTDRStyle()
    canv = ROOT.TCanvas('limit', 'limit')
    pads = OnePad()
   
    # Get limit TGraphs as a dictionary
    graphs = StandardLimitsFromJSONFile('limits_default.json', ['exp0', 'exp1', 'exp2'])
    
    # Create an empty TH1 from the first TGraph to serve as the pad axis and frame
    
    axis = CreateAxisHist(graphs.values()[0])
    axis.GetXaxis().SetTitle('m_{H} (GeV)')
    axis.GetXaxis().SetRangeUser(0, 1000)

    axis.GetYaxis().SetTitle('95% CL limit on #sigma(gg#rightarrowH) x B(h#rightarrowe#tau_{#mu}) [pb]')
    pads[0].cd()
    axis.Draw('axis')
   
    # Create a legend in the top left
    legend = PositionedLegend(0.3, 0.2, 3, 0.015)
    
    # Set the standard green and yellow colors and draw
    StyleLimitBand(graphs)
    DrawLimitBand(pads[0], graphs, legend=legend)
    legend.Draw()
    
    # Re-draw the frame and tick marks
    pads[0].RedrawAxis()
    pads[0].GetFrame().Draw()
    
    # Adjust the y-axis range such that the maximum graph value sits 25% below
    # the top of the frame. Fix the minimum to zero.
    FixBothRanges(pads[0], 0, 0, GetPadYMax(pads[0]), 0.25)
    
    # Standard CMS logo
    DrawCMSLogo(pads[0], 'CMS', 'Internal', 11, 0.045, 0.035, 1.2, '', 0.8)

    canv.Print('.pdf')
    canv.Print('.png')
    canv.Print('.root')


    count+=1
