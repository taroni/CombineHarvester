import ROOT

ROOT.gROOT.SetBatch(1)

samples = ['EWKDiboson', 'TT', 'ST', 'SMH', 'DY', 'DYTT', 'LFV200', 'W']
files = ['lfv_em_1_13TeV_200.input.root', 'lfv_em_2_13TeV_200.input.root']


canvas=ROOT.TCanvas("d","c", 600, 600)
canvas.Draw()
channel='em'
category = '1'
for f in files:
    if 'et' in f: channel='et'
    if '_2_' in f: category='2'
    f0=ROOT.TFile.Open(f, 'READ')
    
    mydir = f0.Get(f.replace('_200.input.root', ''))
    
    for sample in samples:
        h0=mydir.Get(sample)
       
        histolist=[x.GetName() for x in mydir.GetListOfKeys() if sample in x.GetName() and 'Down' in x.GetName() and x.GetName().startswith(sample)]
        for histo in histolist:
            leg=ROOT.TLegend(0.45, 0.85, 0.85, 0.7)

            canvas.Clear()
            pad0=ROOT.TPad("pad0", "pad0", 0, 0.32, 1, 1)
            pad1=ROOT.TPad("pad1", "pad1", 0., 0.,1, 0.3)
            pad0.Draw()
            pad1.Draw()
            pad0.cd()
            print histo, sample, f
            h0.Draw('HIST')
            h0.SetFillColor(0)
            h0.SetLineColor(1)
            h0.SetLineWidth(2)
            h1=mydir.Get(histo)
            h1.Draw("HISTSAMES")
            h1.SetFillColor(0)
            h1.SetLineColor(2)
            h1.SetLineWidth(2)
            h2=mydir.Get(histo.replace( 'Down', 'Up'))
            h2.Draw("HISTSAMES")
            h2.SetFillColor(0)
            h2.SetLineColor(4)
            h2.SetLineStyle(2)
            h2.SetLineWidth(2)
            print h0.GetName(), h1.GetName(), h2.GetName()
            max0=h0.GetBinContent(h0.GetMaximumBin())
            max1=h1.GetBinContent(h1.GetMaximumBin())
            max2=h2.GetBinContent(h2.GetMaximumBin())
            
            h0.GetYaxis().SetRangeUser(0,1.2*max(max0, max1, max2))
            canvas.Update()
            leg.AddEntry(h0, h0.GetName(), "lp")
            leg.AddEntry(h1, h1.GetName(), "lp")
            leg.AddEntry(h2, h2.GetName().replace("Down", "Up"), "lp")

            leg.Draw()
            

            #pad1.Draw()
            pad1.cd()
            h0.Sumw2()
            h1.Sumw2()
            h2.Sumw2()
            hratioUp=h2.Clone()
            hratioUp.Divide(h0.Clone())
            hratioDown=h1.Clone()
            hratioDown.Divide(h0.Clone())
            hratioUp.Draw("HISTP")
            hratioUp.SetMarkerStyle(20)
            hratioUp.SetMarkerColor(4)
            hratioDown.Draw("HISTSAMEP") 
            hratioDown.SetMarkerColor(2)
            hratioDown.SetMarkerStyle(20)
            hratioUp.GetYaxis().SetRangeUser(0., 2)
            line = ROOT.TLine(0, 1, 1500, 1) 
            line.Draw()
            line.SetLineStyle(2)
            line.SetLineColor(1)

            canvas.Update()

            canvas.SaveAs("plots/"+channel+"_"+category+"_"+histo.replace("Down", "")+".png")
            canvas.SaveAs("plots/"+channel+"_"+category+"_"+histo.replace("Down", "")+".pdf")
            canvas.SaveAs("plots/"+channel+"_"+category+"_"+histo.replace("Down", "")+".root")
            
