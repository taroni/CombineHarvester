#include <string>
#include <map>
#include <vector>
#include "boost/algorithm/string/predicate.hpp"
#include "boost/program_options.hpp"
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/TFileIO.h"
#include "CombineHarvester/CombineTools/interface/HttSystematics.h"
#include "CombineHarvester/CombinePdfs/interface/MorphFunctions.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"

#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "TH2.h"

using namespace std;
using boost::starts_with;
namespace po = boost::program_options;
using ch::JoinStr;
using ch::syst::SystMap;


int main(int argc, char** argv) {
  string SM125= "";
  string mass = "mA";
  po::variables_map vm;
  po::options_description config("configuration");
  config.add_options()
    ("mass,m", po::value<string>(&mass)->default_value(mass))
    ("SM125,h", po::value<string>(&SM125)->default_value(SM125));
  po::store(po::command_line_parser(argc, argv).options(config).run(), vm);
  po::notify(vm);
  
  typedef vector<pair<int, string>> Categories;
  typedef vector<string> VString;

  // We will need to source some inputs from the "auxiliaries" repo
  //string SM125        = "";
  //if(argc>1) SM125    = string(argv[1]);
  string auxiliaries  = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/";
  string aux_shapes   = auxiliaries +"shapesForLimit/";
  string aux_pruning  = auxiliaries +"pruning/";
  string input_dir    = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/CombineTools/input";

  VString massRanges =
    {"shapes_et_LowMass","shapes_et_HighMass"};

  //lm==lowmass, hm=highmass
  // map<string, string> input_folders = {
  //     {"lm", "shapes_em_LowMass"},
  //     {"hm", "shapes_em_HighMass"}
  // };

  // RooFit will be quite noisy if we don't set this
  // RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);

  RooRealVar mA(mass.c_str(), mass.c_str(), 90., 1000.);
  RooRealVar mH("mH", "mH", 90., 1000.);
  //RooRealVar mh("mh", "mh", 90., 1000.);
  
  //map<string, VString> bkg_procs;
  //bkg_procs["mt"] = {"ZTT", "QCD", "W", "ZJ", "ZL", "TT", "VV"};
  //bkg_procs["et"] = {"ZTT", "QCD", "W", "ZJ", "ZL", "TT", "VV"};
  //bkg_procs["tt"] = {"ZTT", "QCD", "W", "ZJ", "ZL", "TT", "VV"};
  // bkg_procs["em"] = {"Ztt", "ttbar", "EWK", "Fakes"};
  // bkg_procs["mm"] = {"ZTT", "ZMM", "QCD", "TTJ", "WJets", "Dibosons"};

  VString bkg_procs =  {"SMH", "DY", "DYTT", "ttbar", "singlet","EWKDiboson", "fakes"};
  
  
  
  TH1::AddDirectory(false);
  ch::CombineHarvester cb;

  //VString SM_procs = {"ggH_SM125", "qqH_SM125", "VH_SM125"};

  VString sig_procs = {"LFV"};

  //  map<string, Categories> cats;

  Categories cats = {{0, "0jet"}, {1,"1jet"}};


  // cats["mt_8TeV"] = {
  //   {10, "muTau_nobtag_low"}, {11, "muTau_nobtag_medium"}, {12, "muTau_nobtag_high"}, {13, "muTau_btag_low"}, {14, "muTau_btag_high"}};
  // cats["et_8TeV"] = {
  //   {10, "eleTau_nobtag_low"}, {11, "eleTau_nobtag_medium"}, {12, "eleTau_nobtag_high"}, {13, "eleTau_btag_low"}, {14, "eleTau_btag_high"}};
  // cats["tt_8TeV"] = {
  //   {10, "tauTau_nobtag_low"}, {11, "tauTau_nobtag_medium"}, {12, "tauTau_nobtag_high"}, {13, "tauTau_btag_low"}, {14, "tauTau_btag_high"}};
  // cats["em_8TeV"] = {
  //   {8, "emu_nobtag"}, {9, "emu_btag"}};
  // cats["mm_8TeV"] = {
  //  {8, "mumu_nobtag"}, {9, "mumu_btag"}};

  // auto masses = ch::MassesFromRange(
  //     "90,100,120-140:10,140-200:20,200-500:50,600-1000:100");
  
  auto masses =ch::MassesFromRange("200,300,450,600,750,900");


  cout << "Adding observations and backgrounds...";
  cb.AddObservations({"*"}, {"lfv"}, {"13TeV"}, {"et"}, cats);
  cb.AddProcesses({"*"}, {"lfv"}, {"13TeV"}, {"et"}, bkg_procs, cats, false);
    

  // for (auto chn : chns) {
  //   cb.AddObservations({"*"}, {"htt"}, {"8TeV"}, {chn}, cats[chn+"_8TeV"]);
  //   cb.AddProcesses({"*"}, {"htt"}, {"8TeV"}, {chn}, bkg_procs[chn], cats[chn+"_8TeV"], false);
  //   if(SM125==string("signal_SM125")) cb.AddProcesses({"*"}, {"htt"}, {"8TeV"}, {chn}, SM_procs, cats[chn+"_8TeV"], true);  
  //   else if(SM125==string("bkg_SM125")) cb.AddProcesses({"*"}, {"htt"}, {"8TeV"}, {chn}, SM_procs, cats[chn+"_8TeV"], false);  
  // }
  cout << " done\n";
  
  cout << "Adding signal processes...";
  cb.AddProcesses(masses, {"lfv"}, {"13TeV"}, {"et"}, sig_procs, cats, true);
  //! [part1]
  // Unlike in previous MSSM H->tautau analyses we will create a separate
  // process for each Higgs in the datacards
  // map<string, VString> signal_types = {
  //   {"ggH", {"ggh_htautau", "ggH_Htautau", "ggA_Atautau"}},
  //   {"bbH", {"bbh_htautau", "bbH_Htautau", "bbA_Atautau"}}
  // };
  // //! [part1]
  // if(mass=="MH"){
  //   signal_types = {
  //     {"ggH", {"ggH"}},
  //     {"bbH", {"bbH"}}
  //   };
  // }
  // //! [part2]
  // for (auto chn : chns) {
  //   cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {chn}, signal_types["ggH"], cats[chn+"_8TeV"], true);
  //   cb.AddProcesses(masses, {"htt"}, {"8TeV"}, {chn}, signal_types["bbH"], cats[chn+"_8TeV"], true);
  // }
  //! [part2]
  cout << " done\n";



  cout << "Adding systematic uncertainties...";
  // ch::AddMSSMUpdateSystematics_et_mt(cb);
  // ch::AddMSSMUpdateSystematics_em(cb);
  // ch::AddMSSMUpdateSystematics_mm(cb);
  // ch::AddMSSMUpdateSystematics_tt(cb);
  
  auto signal = ch::Set2Vec(cb.cp().signals().process_set());
  auto backgrounds = ch::Set2Vec(cb.cp().backgrounds().process_set());


  cb.cp().process(JoinStr({signal,{"SMH", "DY","DYTT", "ttbar", "singlet","EWKDiboson"}})).AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));
  cb.cp().process(JoinStr({signal,{"SMH", "DY", "DYTT","ttbar", "singlet","EWKDiboson"}})).AddSyst(cb, "CMS_eff_tau", "lnN", SystMap<>::init(1.05));
  cb.cp().process(JoinStr({signal,{"SMH", "DY", "DYTT","ttbar", "singlet","EWKDiboson"}})).AddSyst(cb, "CMS_lumi_13TeV", "lnN", SystMap<>::init(1.025));
  cb.cp().bin({"1jet"}).process({"ttbar", "singlet"}).AddSyst(cb, "btagVeto", "lnN", SystMap<>::init(1.025));
  cb.cp().process({"LFV"}).AddSyst(cb,"TheoH", "lnN", SystMap<ch::syst::mass>::init({"200","300"}, 1.018)({"450"},1.02)({"600","750"}, 1.021)({"900"},1.022) );
  cb.cp().process({"LFV"}).AddSyst(cb,"TheoHPDF", "lnN", SystMap<ch::syst::mass>::init({"200","300"}, 1.03)({"450"},1.031)({"600"}, 1.035)({"750"}, 1.04)({"900"},1.046) );
  cb.cp().process({"fakes"}).AddSyst(cb, "norm_taufakes_etauhad", "lnN", SystMap<>::init(1.30));
  cb.cp().process({"fakes"}).AddSyst(cb,"norm_taufakes_etauhad_uncor_$BIN", "lnN", SystMap<>::init(1.1));
  cb.cp().process({"DY", "DYTT"}).AddSyst(cb, "norm_z", "lnN", SystMap<>::init(1.1));
  cb.cp().process({"DY", "DYTT"}).AddSyst(cb,"norm_z_$BIN", "lnN", SystMap<>::init(1.05));
  cb.cp().process({"Diboson"}).AddSyst(cb, "norm_Diboson ", "lnN", SystMap<>::init(1.05));
  cb.cp().process({"Diboson"}).AddSyst(cb,"norm_Diboson_$BIN", "lnN", SystMap<>::init(1.05));
  cb.cp().process({"singlet"}).AddSyst(cb, "norm_TT ", "lnN", SystMap<>::init(1.10));
  cb.cp().process({"ttbar"}).AddSyst(cb,"norm_TT_$BIN", "lnN", SystMap<>::init(1.05));
  cb.cp().process({"singlet"}).AddSyst(cb, "norm_T ", "lnN", SystMap<>::init(1.05));
  cb.cp().process({"singlet"}).AddSyst(cb,"norm_T_$BIN", "lnN", SystMap<>::init(1.05));
  cb.cp().process({"SMH"}).AddSyst(cb,"TheoSMH", "lnN", SystMap<>::init(1.039));
  cb.cp().process({"SMH"}).AddSyst(cb,"TheoSMHPDF", "lnN", SystMap<>::init(1.032));
  cb.cp().process({"SMH"}).AddSyst(cb,"BR_htt_THU", "lnN", SystMap<>::init(1.017));
  cb.cp().process({"SMH"}).AddSyst(cb,"BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
  cb.cp().process({"SMH"}).AddSyst(cb,"BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "PU_Uncertainty", "shape", SystMap<>::init(1.0));    
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesAbsoluteFlavMap", "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesAbsoluteMPFBias", "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesAbsoluteScale",   "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesAbsoluteStat",    "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesFlavorQCD",       "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesFragmentation",   "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesPileUpDataMC",    "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesPileUpPtBB",      "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesPileUpPtEC1",     "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesPileUpPtEC2",     "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesPileUpPtHF",      "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesPileUpPtRef",     "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativeBal",     "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativeFSR",     "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativeJEREC1",  "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativeJEREC2",  "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativeJERHF",   "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativePtBB",    "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativePtEC1",   "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativePtEC2",   "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativePtHF",    "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativeStatEC",  "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativeStatFSR", "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesRelativeStatHF",  "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesSinglePionECAL",  "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesSinglePionHCAL",  "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "jesTimePtEta"     ,  "shape", SystMap<>::init(1.0));    
  cb.cp().process(JoinStr({signal , {"SMH","DYTT","EWKDiboson"}})).AddSyst(cb, "highPtTau", "shape", SystMap<>::init(1.0));
  cb.cp().process({"fakes"}).AddSyst(cb, "shape_FAKES", "shape", SystMap<>::init(1.0));
  cb.cp().process({"DY"}).AddSyst(cb, "etfakeES", "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "EES", "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal , {"SMH", "EWKDiboson", "DYTT"}})).AddSyst(cb, "TES3p", "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal , {"SMH", "EWKDiboson", "DYTT"}})).AddSyst(cb, "TES1p", "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal , {"SMH", "EWKDiboson", "DYTT"}})).AddSyst(cb, "TES1p10", "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "uesHcal", "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "uesEcal", "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "uesCharged", "shape", SystMap<>::init(1.0));
  cb.cp().process(JoinStr({signal ,  {"DY", "DYTT", "ttbar", "singlet","EWKDiboson", "SMH"}} )).AddSyst(cb, "uesHF", "shape", SystMap<>::init(1.0));




  cout << " done\n";

  cout << "Extracting histograms from input root files...";
  //for (string chn : chns) {
  
  string file = aux_shapes + "shapes_et_LowMass.root";
  cb.cp().backgrounds().ExtractShapes(file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");   
  //   if(SM125==string("signal_SM125")) cb.cp().channel({chn}).era({"8TeV"}).process(SM_procs).ExtractShapes(file, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
  //   // We have to map each Higgs signal process to the same histogram, i.e:
  //   // {ggh, ggH, ggA} --> ggH
  //   // {bbh, bbH, bbA} --> bbH
  // //! [part3]
  cb.cp().process(sig_procs).ExtractShapes
    (file, "$BIN/LFV$MASS", "$BIN/LFV$MASS_$SYSTEMATIC");
    // cb.cp().channel({chn}).era({"8TeV"}).process(signal_types["bbH"]).ExtractShapes
    //   (file, "$CHANNEL/bbH$MASS", "$CHANNEL/bbH$MASS_$SYSTEMATIC");
  //! [part3]
  //};
  cout << " done\n";


  ///we don't need it, the processed masses are already correctly scaled
  // cout << "Scaling signal process rates for acceptance...\n";
  // //for (string e : {"8TeV"}) {
  // //  for (string p : {"ggH", "bbH"}) {
  // for (string p : {"LFV"}){
  //     cout << "Scaling for process " << p << "\n";
  //     auto gr = ch::TGraphFromTable(
  //         input_dir+"/xsecs_brs/mssm_" + p + "_" + e + "_accept.txt", "mPhi",
  //         "accept");
  //     cb.cp().process(signal_types[p]).era({e}).ForEachProc([&](ch::Process *proc) {
  //       double m = boost::lexical_cast<double>(proc->mass());
  //       proc->set_rate(proc->rate() * gr.Eval(m));
  //     });
  //   }
  //   //  }
  // cout << "done\n";

  cout << "Generating bbb uncertainties...";
  auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(0.05)
    .SetFixNorm(true);
  bbb.AddBinByBin(cb.cp().backgrounds(), cb); 
  cout << " done\n";
  
  cout << "Setting standardised bin names...";
  ch::SetStandardBinNames(cb);
  cout << " done\n";

  // we don't use pruning for the moment
  // cout << "Pruning bbb uncertainties...\n";
  // VString droplist = ch::ParseFileLines(aux_pruning + "uncertainty-pruning-drop-150602-mssm-taupt-CH.txt");
  // cout << ">> Droplist contains " << droplist.size() << " entries\n";

  // set<string> to_drop;
  // for (auto x : droplist) to_drop.insert(x);
  // auto pre_drop = cb.syst_name_set();
  // cb.syst_name(droplist, false);
  // auto post_drop = cb.syst_name_set();
  // cout << ">> Systematics dropped: " << pre_drop.size() - post_drop.size() << "\n";
  // cout << "done\n";

  cout << "Creating workspace...\n";
  RooWorkspace ws("lfv", "lfv");

  TFile demo("lfv_et_demo.root", "RECREATE");

  //! [part4]
  bool do_morphing = true;
  map<string, RooAbsReal *> mass_var = {
    {"LFV", &mH}
  };
  // if(mass=="MH"){
  //   mass_var = {
  //     {"ggH", &mA},
  //     {"bbH", &mA}
  //   };
  // }
  if (do_morphing) {
    auto bins = cb.bin_set();
    for (auto b : bins) {
      auto procs = cb.cp().bin({b}).process({"LFV"}).process_set();
      for (auto p : procs) {
        ch::BuildRooMorphing(ws, cb, b, p, *(mass_var[p]),"norm", true, true, false, &demo);
      }
    }
  }
  demo.Close();
  cb.AddWorkspace(ws);
  cb.cp().process({"LFV"}).ExtractPdfs(cb, "LFV", "$BIN_$PROCESS_morph");
  cb.PrintAll();
  cout << "done\n";
  //! [part4]

  string folder = "output/LFV_nomodel";
  boost::filesystem::create_directories(folder);

  cout << "Writing datacards ...";
  TFile output((folder + "/LFV_input.root").c_str(), "RECREATE");
  //for (string chn : chns) {
  auto bins = cb.cp().bin_set();
  for (auto b : bins) {
    cb.cp().bin({b}).mass({"*"}).WriteDatacard(folder + "/" + b + ".txt", output);
  }
  //}
  cb.cp().mass({"*"}).WriteDatacard(folder + "/LFV.txt", output);
  output.Close();
  cout << " done\n";
}
