import os
import sys
from os import listdir
from os.path import isfile, join, isdir
import ROOT
import json
from CombineHarvester.CombineTools.plotting import *


ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

#directories=['shapes_HighMass_noBBB_bveto','shapes_HighMass_bveto', 'shapes_HighMass_noBveto', 'shapes_HighMass_noBBB_noBveto']
directories=['shapes_LowMass_noBBB_bveto','shapes_LowMass_bveto', 'shapes_LowMass_noBveto', 'shapes_LowMass_noBBB_noBveto']
#directories=['shapes_pzeta_noBBB_bveto','shapes_pzeta_bveto', 'shapes_pzeta_nobveto', 'shapes_pzeta_noBBB_nobveto']##, 'shapes_LowMass_wSyst_noMt']

def graphFromJson(js, label):
    xvals=[]
    yvals=[]
    for key in js:
        xvals.append(float(key))
        yvals.append(js[key][label])

    graph = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals))
    graph.Sort()
    return graph

def graphBandFromJson(js, central, lo, hi):
    xvals = []
    yvals = []
    yvals_lo = []
    yvals_hi = []
    for key in js:
        xvals.append(float(key))
        yvals.append(js[key][central])
        yvals_lo.append(js[key][central] - js[key][lo])
        yvals_hi.append(js[key][hi] - js[key][central])
    graph = ROOT.TGraphAsymmErrors(len(xvals), array('d', xvals), array('d', yvals), array(
            'd', [0]), array('d', [0]), array('d', yvals_lo), array('d', yvals_hi))


    graph.Sort()
    return graph

graphs = {}
myGraph={}
ModTDRStyle()
canv = ROOT.TCanvas('limitComparison', 'limitComparison')
pads = OnePad()

axis = ROOT.TH1F("axis", "", 8, 150, 950)
axis.GetXaxis().SetTitle('m_{H} (GeV)')
axis.GetYaxis().SetTitle('95% CL limit on #sigma(gg#rightarrowH) x B(H#rightarrowe#tau) [pb]')
axis.GetYaxis().SetRangeUser(0.0001, 0.5)

pads[0].cd()
axis.Draw('axis')

legend = ROOT.TLegend(0.65, 0.85, 0.85, 0.7) 

for n, mydir in enumerate(directories):

    jsfile = os.path.join(mydir+'/limits_BrXsec.json')
    with open(jsfile) as jsonfile:
        js = json.load(jsonfile)

        graphs[mydir] = graphBandFromJson(js, 'exp0', 'exp-1', 'exp+1')
        npoints=graphs[mydir].GetN()        
        myGraph[mydir]=ROOT.TGraphAsymmErrors(npoints)

        for i in range(0, npoints):
            myGraph[mydir].SetPoint(i, graphs[mydir].GetX()[i], graphs[mydir].GetY()[i])
            myGraph[mydir].SetPointError(i, 0,0, graphs[mydir].GetEYhigh()[i],graphs[mydir].GetEYlow()[i])


        if n==0: 
            myGraph[mydir].Draw("P")
            
        else:
            myGraph[mydir].Draw("P")
            myGraph[mydir].SetLineColor(n+1)
            myGraph[mydir].SetMarkerColor(n+1)
            myGraph[mydir].SetMarkerStyle(20)
        legend.AddEntry(myGraph[mydir], mydir[mydir.find('_')+1:], 'lp')
            
pads[0].SetLogy(1)
legend.Draw()
canv.Update()
canv.SaveAs('comparison_LowMass.root')
canv.SaveAs('comparison_LowMass.png')
canv.SaveAs('comparison_LowMass.pdf')
#canv.SaveAs('comparison_pzeta.root')
#canv.SaveAs('comparison_pzeta.png')
#canv.SaveAs('comparison_pzeta.pdf')
