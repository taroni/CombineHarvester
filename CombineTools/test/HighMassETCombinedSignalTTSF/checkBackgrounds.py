import ROOT
import argparse
parser = argparse.ArgumentParser() 
parser.add_argument('--ch', dest='ch')
args = parser.parse_args()
ch=args.ch


massRanges = ['LowMass', 'HighMass']

cats=[1, 2]

for mass in massRanges:
    massValues=[]
    massValues.extend(['200', '300', '450']) if 'LowMass' in mass  else  massValues.extend(['450', '600', '750', '900'])
    for value in massValues:
        for cat in cats:
            filename='lfv_%s_%s_13TeV_%s.input.root' %(ch, cat, value)
            print filename
            dirpath='shapes_%s/%s/' %(mass, value)
            print dirpath
            infile = ROOT.TFile.Open(dirpath+filename, "READ")
            dirname='lfv_%s_%s_13TeV' %(ch, cat)
            print dirname
            mydir=infile.Get(dirname)
            histolist=[f.GetName() for f in mydir.GetListOfKeys() if '_' not in f.GetName()  and 'data' not in f.GetName()]
            
            histo=mydir.Get(histolist[0]).Clone()
            print histo
            for n,h in enumerate( histolist):
                if n==0:
                    continue
                histo.Sumw2()
                histo.Add(mydir.Get(h).Clone())
            for ibin in range(histo.GetXaxis().GetNbins()):
                content=histo.GetBinContent(ibin)
                if content<=0 :
                    xbin=histo.GetBinCenter(ibin)
                    print 'empty bin:', ibin, xbin, dirpath+filename
                    
                
            outfile=ROOT.TFile.Open(dirpath+filename.replace('input', 'output'), "RECREATE")
            outfile.cd()
            histo.Write()
            outfile.Close()
