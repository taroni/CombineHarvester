import CombineHarvester.CombineTools.ch as ch
import argparse
import sys
import os
import ROOT
import ast
from os import listdir
from os.path import isfile, join
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--b", type=str,
                    help="compute the binbybin")


args = parser.parse_args()
print args
binbybin=ast.literal_eval(args.b) if args.b else False

shapedir= os.environ["CMSSW_BASE"] + "/src/auxiliaries/shapesForLimit/"
#onlyfiles = [f for f in listdir(shapedir) if isfile(join(shapedir, f))]
#onlyfiles = ['shapes_HighMass_bveto.root', 'shapes_LowMass_bveto.root']
onlyfiles=['shapes_et_LowMass.root','shapes_et_HighMass.root']
#onlyfiles = ['shapes_pzeta_nobveto.root']

for infile in onlyfiles:


    inputFile=infile
    
    dirname = inputFile.replace('.le', '_le').replace('.root', '')
    print inputFile, binbybin, dirname
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    aux_shapes = os.environ["CMSSW_BASE"] + "/src/auxiliaries/shapesForLimit/"
    shutil.copy2(aux_shapes+inputFile, dirname)
    cb=ch.CombineHarvester()
    cats=[]
    if 'le1' in infile:
        cats=[(1, "le1")]
    else:
        cats=[
            (1, "0jet"),
            (2, "1jet")
        ]
    print cats
    masses = ["200", "300", "450", "600", "750", "900"];#ch::MassesFromRange("120");//120-135:5");
    cb.AddObservations(["*"], ["lfv"], ["13TeV"], ["et"], cats)

    bkg_procs = ["SMH", "DY", "DYTT", "ttbar", "singlet","EWKDiboson", "fakes"]
    mcbkg_procs = ["SMH", "DY", "DYTT", "ttbar", "singlet","EWKDiboson"]
    cb.AddProcesses(["*"], ["lfv"], ["13TeV"], ["et"], bkg_procs, cats, signal=False)

    sig_procs = ["LFV"]
    cb.AddProcesses(masses, ["lfv"], ["13TeV"], ["et"], sig_procs, cats, signal=True)

    cb.cp().process(sig_procs+["SMH", "DY","DYTT", "ttbar", "singlet","EWKDiboson"]).AddSyst(cb, "CMS_eff_e", "lnN", ch.SystMap()(1.02))

    cb.cp().process(sig_procs+["SMH", "DY", "DYTT","ttbar", "singlet","EWKDiboson"]).AddSyst(cb, "CMS_eff_tau", "lnN", ch.SystMap()(1.05))

    cb.cp().process(sig_procs+["SMH", "DY", "DYTT","ttbar", "singlet","EWKDiboson"]).AddSyst(cb, "CMS_lumi_13TeV", "lnN", ch.SystMap()(1.025))
    
    cb.cp().bin(["1jet"]).process(["ttbar", "singlet"]).AddSyst(cb, "btagVeto", "lnN", ch.SystMap()(1.025))
    
    #cb.cp().process(["SMH","LFV"]).AddSyst(cb,"TheoH", "lnN", ch.SystMap()(1.10))
    cb.cp().process(["LFV"]).AddSyst(cb,"TheoH_$MASS", "lnN", ch.SystMap('mass')(["200","300"], 1.018)(["450"],1.02)(["600","750"], 1.021)(["900"],1.022) )
    cb.cp().process(["LFV"]).AddSyst(cb,"TheoHPDF_$MASS", "lnN", ch.SystMap('mass')(["200","300"], 1.03)(["450"],1.031)(["600"], 1.035)(["750"], 1.04)(["900"],1.046) )


    cb.cp().process(["fakes"]).AddSyst(cb, "norm_taufakes_etauhad", "lnN", ch.SystMap()(1.30))
 
    cb.cp().process(["fakes"]).AddSyst(cb,"norm_taufakes_etauhad_uncor_$BIN", "lnN", ch.SystMap()(1.1))
 
    cb.cp().process(["DY", "DYTT"]).AddSyst(cb, "norm_z", "lnN", ch.SystMap()(1.1))
    
    cb.cp().process(["DY", "DYTT"]).AddSyst(cb,"norm_z_$BIN", "lnN", ch.SystMap()(1.05))

    cb.cp().process(["Diboson"]).AddSyst(cb, "norm_Diboson ", "lnN", ch.SystMap()(1.05))

    cb.cp().process(["Diboson"]).AddSyst(cb,"norm_Diboson_$BIN", "lnN", ch.SystMap()(1.05))
    
    cb.cp().process(["singlet"]).AddSyst(cb, "norm_TT ", "lnN", ch.SystMap()(1.10))
    
    cb.cp().process(["ttbar"]).AddSyst(cb,"norm_TT_$BIN", "lnN", ch.SystMap()(1.05))
    
    cb.cp().process(["singlet"]).AddSyst(cb, "norm_T ", "lnN", ch.SystMap()(1.05))
    
    cb.cp().process(["singlet"]).AddSyst(cb,"norm_T_$BIN", "lnN", ch.SystMap()(1.05))

    cb.cp().process(["SMH"]).AddSyst(cb,"TheoSMH", "lnN", ch.SystMap()(1.039))
    cb.cp().process(["SMH"]).AddSyst(cb,"TheoSMHPDF", "lnN", ch.SystMap()(1.032))
    cb.cp().process(["SMH"]).AddSyst(cb,"BR_htt_THU", "lnN", ch.SystMap()(1.017));
    cb.cp().process(["SMH"]).AddSyst(cb,"BR_htt_PU_mq", "lnN", ch.SystMap()(1.0099));
    cb.cp().process(["SMH"]).AddSyst(cb,"BR_htt_PU_alphas", "lnN", ch.SystMap()(1.0062));

    #Systematics
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, "PU_Uncertainty", "shape", ch.SystMap()(1.0))
    
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesAbsoluteFlavMap', "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesAbsoluteMPFBias', "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesAbsoluteScale',   "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesAbsoluteStat',    "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesFlavorQCD',       "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesFragmentation',   "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesPileUpDataMC',      "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesPileUpPtBB',        "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesPileUpPtEC1',       "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesPileUpPtEC2',       "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesPileUpPtHF',        "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesPileUpPtRef',       "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativeBal',     "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativeFSR',     "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativeJEREC1',  "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativeJEREC2',  "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativeJERHF',   "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativePtBB',    "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativePtEC1',   "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativePtEC2',   "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativePtHF',    "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativeStatEC',  "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativeStatFSR', "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesRelativeStatHF',  "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesSinglePionECAL',  "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesSinglePionHCAL',  "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, 'jesTimePtEta'     ,  "shape", ch.SystMap()(1.0))
    
    cb.cp().process(sig_procs+ ["SMH","DYTT","EWKDiboson"]).AddSyst(cb, "highPtTau", "shape", ch.SystMap()(1.0))

    cb.cp().process(["fakes"]).AddSyst(cb, "shape_FAKES", "shape", ch.SystMap()(1.0))
    cb.cp().process(["DY"]).AddSyst(cb, "etfakeES", "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, "EES", "shape", ch.SystMap()(1.0))
    ###cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, "EESRho", "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ ['SMH', 'EWKDiboson', 'DYTT']).AddSyst(cb, "TES3p", "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ ['SMH', 'EWKDiboson', 'DYTT']).AddSyst(cb, "TES1p", "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ ['SMH', 'EWKDiboson', 'DYTT']).AddSyst(cb, "TES1p10", "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, "uesHcal", "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, "uesEcal", "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, "uesCharged", "shape", ch.SystMap()(1.0))
    cb.cp().process(sig_procs+ mcbkg_procs).AddSyst(cb, "uesHF", "shape", ch.SystMap()(1.0))

   # print cb.cp().backgrounds()

    myfile=aux_shapes+inputFile
    cb.cp().backgrounds().ExtractShapes(myfile,"$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
    cb.cp().signals().ExtractShapes(myfile, "$BIN/$PROCESS$MASS","$BIN/$PROCESS$MASS_$SYSTEMATIC");
    

    if(binbybin):
        bbb = ch.BinByBinFactory()
        bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(False)
        bbb.MergeBinErrors(cb.cp().backgrounds())
        bbb.AddBinByBin(cb.cp().backgrounds(), cb)
    
    cb.PrintSysts()
    ch.SetStandardBinNames(cb);
    bins = cb.bin_set();
   
 
    for b in  bins:
        for  m in masses:
            output=ROOT.TFile(dirname+"/%s_%s.input.root"%(b,m), "RECREATE");

            print ">> Writing datacard for bin: ",  b , " and mass: " , m
            cb.cp().bin([b]).mass([m, "*"]).WriteDatacard(dirname+'/'+ b + "_" + m + ".txt", output.GetName())
    
    print cb.PrintAll()
