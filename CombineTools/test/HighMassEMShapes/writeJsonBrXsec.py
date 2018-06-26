import os
import sys
from os import listdir
from os.path import isfile, join, isdir
import ROOT
import json
from argparse import ArgumentParser
parser = ArgumentParser(description=__doc__)
parser.add_argument('-j','--jetdir', dest='jetDir', type=str, action='append', help='jet directory', required=True)
parser.add_argument('-d','--dir', dest='MassDir', type=str, action='append', help='jet directory', required=True)
args = parser.parse_args()
jet = args.jetDir[0]

mydir=args.MassDir[0]

from CombineHarvester.CombineTools.plotting import *



ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

xsec={
    200. : 0.01*16.94,
    300. : 0.01*6.590,
    450. : 0.01*2.300,
    600. : 0.01*1.001, 
    750. : 0.01*0.4969, 
    900. : 0.01*0.2685
}

def graphFromJson(js, label):
    xvals=[]
    yvals=[]
    for key in js:
        xvals.append(float(key))
        yvals.append(xsec[float(key)]*js[key][label])

    graph = ROOT.TGraph(len(xvals), array('d', xvals), array('d', yvals))
    graph.Sort()
    graph.SetLineColor(1)
    graph.SetMarkerColor(1)
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(0.8)
    return graph

def graphBandFromJson(js, central, lo, hi):
    xvals = []
    yvals = []
    yvals_lo = []
    yvals_hi = []
    for key in js:
        xvals.append(float(key))
        yvals.append(xsec[float(key)]*js[key][central])
        yvals_lo.append(xsec[float(key)]*js[key][central] - xsec[float(key)]*js[key][lo])
        yvals_hi.append(xsec[float(key)]*js[key][hi] - xsec[float(key)]*js[key][central])
    graph = ROOT.TGraphAsymmErrors(len(xvals), array('d', xvals), array('d', yvals), array(
            'd', [0]), array('d', [0]), array('d', yvals_lo), array('d', yvals_hi))
    graph.Sort()
    return graph


def jsonLimitsBrXsec(js):
    newjs = {}
    for key in js:
        xval = float(key)
        mydic = {}
        for label, value in js[key].iteritems():
            mydic[label]= value*xsec[float(key)]
        newjs[key]=mydic
            
        #print 'obs', float(key), js[key]['obs'],   xsec[float(key)]*js[key]['obs'], newjs[key]['obs'] 
        #print 'exp0', float(key), js[key]['exp0'], xsec[float(key)]*js[key]['exp0'],  newjs[key]['exp0'] 
        #print 'exp+1', float(key), js[key]['exp+1'],  xsec[float(key)]*js[key]['exp+1'], newjs[key]['exp+1'] 
        #print 'exp-1', float(key), js[key]['exp-1'],  xsec[float(key)]*js[key]['exp-1'], newjs[key]['exp-1']
        #print 'exp+2', float(key), js[key]['exp+2'],  xsec[float(key)]*js[key]['exp+2'], newjs[key]['exp+2']
        #print 'exp-2', float(key), js[key]['exp-2'],  xsec[float(key)]*js[key]['exp-2'], newjs[key]['exp-2']
    return newjs

cwd = os.getcwd()
jsfile = os.path.join( mydir, 'limits%s_default.json' %jet)
with open(jsfile) as jsonfile:
    js = json.load(jsonfile)

graphs = {}

graphs['exp0'] = graphFromJson(js, 'exp0')

graphs['exp1'] = graphBandFromJson(js, 'exp0', 'exp-1', 'exp+1')

graphs['exp2'] = graphBandFromJson(js, 'exp0', 'exp-2', 'exp+2')

ModTDRStyle()
canv = ROOT.TCanvas('limit%sBrXsec' %jet, 'limit%sBrXsec' %jet)
pads = OnePad()



#axis = CreateAxisHist(graphs.values()[0])
axis = ROOT.TH1F("axis", "", 8, 150, 950)
axis.GetXaxis().SetTitle('m_{H} (GeV)')
axis.GetYaxis().SetTitle('95% CL limit on #sigma(gg#rightarrowH) x B(H#rightarrowe#tau) [pb]')
axis.GetYaxis().SetRangeUser(0.0005, 0.5)

pads[0].cd()
axis.Draw('axis')
   
# Create a legend in the top left
legend = PositionedLegend(0.3, 0.2, 3, 0.015)
style_dict = {
             'exp0' : { 'LineWidth' : 2, 'LineColor' : 1, 'MarkerStyle' : 20},
             'exp1' : { 'FillColor' : ROOT.kGreen},
             'exp2' : { 'FillColor' : ROOT.kYellow}
             }
legend_dict = {
         #'obs' : { 'Label' : 'Observed', 'LegendStyle' : 'LP', 'DrawStyle' : 'PLSAME'},
         'exp0' : { 'Label' : 'Expected', 'LegendStyle' : 'LP', 'DrawStyle' : 'PLSAME'},
         'exp1' : { 'Label' : '#pm1#sigma Expected', 'LegendStyle' : 'F', 'DrawStyle' : '3SAME'},
         'exp2' : { 'Label' : '#pm2#sigma Expected', 'LegendStyle' : 'F', 'DrawStyle' : '3SAME'}
     }
# Set the standard green and yellow colors and draw
StyleLimitBand(graphs, overwrite_style_dict = style_dict)
DrawLimitBand(pads[0], graphs, legend=legend, legend_overwrite=legend_dict)
#graphs['exp0'].SetLineColor(1)
#graphs['exp0'].SetMarkerColor(1)
#graphs['exp0'].SetMarkerStyle(20)
#graphs['exp0'].SetMarkerSize(1.)
legend.Draw()
    
# Re-draw the frame and tick marks
pads[0].RedrawAxis()
pads[0].GetFrame().Draw()
pads[0].SetLogy(1)

# Adjust the y-axis range such that the maximum graph value sits 25% below
# the top of the frame. Fix the minimum to zero.
FixBothRanges(pads[0], 0, 0, GetPadYMax(pads[0]), 0.25)

# Standard CMS logo
DrawCMSLogo(pads[0], 'CMS', 'Internal', 11, 0.045, 0.035, 1.2, '', 0.8)

canv.Print( os.path.join( mydir, canv.GetName()+'.pdf'))
canv.Print( os.path.join( mydir, canv.GetName()+'.png'))
canv.Print( os.path.join( mydir, canv.GetName()+'.root'))

newjson=jsonLimitsBrXsec(js)

with open(os.path.join( mydir, 'limits%s_BrXsec.json' %jet), 'w') as fp:
    json.dump(newjson, fp)
