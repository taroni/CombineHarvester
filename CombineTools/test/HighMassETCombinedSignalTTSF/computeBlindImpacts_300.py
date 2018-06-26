import os 

mydir='shapes_LowMass'
mass='300'

startdir = os.path.abspath(os.getcwd())
print startdir, os.getcwd()

os.chdir(startdir+'/'+mydir)
os.chdir(startdir+'/'+mydir+'/'+mass)
print 'in working dir', os.getcwd()
cmd0="combineTool.py -M Impacts -d lfv_13TeV.root -m "+mass+" --doInitialFit --robustFit 1  --rMax 5 --rMin -5  -t -1  --expectSignal 1 --task-name combined -n combined"
os.system(cmd0)

cmd1="combineTool.py -M Impacts -d lfv_13TeV.root -m "+mass+" --robustFit 1 --doFits  --rMax 5 --rMin -5  -t -1  --expectSignal 1 --parallel 30 --task-name combined -n combined"
os.system(cmd1)

cmd2="combineTool.py -M Impacts -d  lfv_13TeV.root -m "+mass+" -o \"impacts_m"+mass+"_combined.json\" -n combined"
os.system(cmd2)
    
cmd3="plotImpacts.py -i \"impacts_m"+mass+"_combined.json\" -o impacts_m"+mass+"_combined --transparent"
os.system(cmd3)

### 0jet cat
cmd0="combineTool.py -M Impacts -d lfv_1_13TeV_"+mass+".root -m "+mass+" --doInitialFit --robustFit 1  --rMax 5 --rMin -5   --expectSignal 1 -t -1 --task-name 0jet -n 0jet"
os.system(cmd0)

cmd1="combineTool.py -M Impacts -d lfv_1_13TeV_"+mass+".root -m "+mass+" --robustFit 1 --doFits  --rMax 5 --rMin -5   --expectSignal 1 -t -1 --parallel 30 --task-name 0jet -n 0jet"
os.system(cmd1)
    
cmd2="combineTool.py -M Impacts -d  lfv_1_13TeV_"+mass+".root -m "+mass+" -o \"impacts_m"+mass+"_0jet.json\" -n 0jet"
os.system(cmd2)
    
cmd3="plotImpacts.py -i \"impacts_m"+mass+"_0jet.json\" -o impacts_m"+mass+"_0jet  --transparent"
os.system(cmd3)
    
### 1jet cat
cmd0="combineTool.py -M Impacts -d lfv_2_13TeV_"+mass+".root -m "+mass+" --doInitialFit --robustFit 1  --rMax 5 --rMin -5  --expectSignal 1 -t -1 --task-name 1jet -n 1jet"
os.system(cmd0)
    
cmd1="combineTool.py -M Impacts -d lfv_2_13TeV_"+mass+".root -m "+mass+" --robustFit 1 --doFits  --rMax 5 --rMin -5  -t -1  --expectSignal 1 --parallel 30 --task-name 1jet -n 1jet"
os.system(cmd1)

cmd2="combineTool.py -M Impacts -d  lfv_2_13TeV_"+mass+".root -m "+mass+" -o \"impacts_m"+mass+"_1jet.json\" -n 1jet"
os.system(cmd2)
        
cmd3="plotImpacts.py -i \"impacts_m"+mass+"_1jet.json\" -o impacts_m"+mass+"_1jet  --transparent"
os.system(cmd3)

