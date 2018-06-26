python createMassDirs.py
python mergeTwoLimits_range.py -d shapes_et_LowMass shapes_et_HighMass -j 1
python mergeTwoLimits_range.py -d shapes_et_LowMass shapes_et_HighMass -j 2
python mergeTwoLimits_range.py -d shapes_et_LowMass shapes_et_HighMass -j ''
python writeJsonBrXsec.py  -d shapes_et_LowMass -j ''
python writeJsonBrXsec.py  -d shapes_et_LowMass -j 1
python writeJsonBrXsec.py  -d shapes_et_LowMass -j 2
python writeJsonBrXsec.py  -d shapes_et_HighMass -j ''
python writeJsonBrXsec.py  -d shapes_et_HighMass -j 1
python writeJsonBrXsec.py  -d shapes_et_HighMass -j 2
python makeTables.py
