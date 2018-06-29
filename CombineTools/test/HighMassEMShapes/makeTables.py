import json 
from pprint import pprint
import os 

dirs = ['shapes_em_LowMass', 'shapes_em_HighMass']

filenames = ['limits1_BrXsec.json', 'limits2_BrXsec.json','limits_BrXsec.json']



for filename in filenames:
    labels=[]
    limits={}
    for mydir in dirs: 
        labels.append(mydir.replace('shapes_', ''))
        data = json.load(open(os.path.join(mydir,filename)))
        pprint(data)

        for key, values in data.iteritems():
            if int(float(key)) in limits:
                limits[int(float(key))].append(data[key]['exp0'])
            else:
                limits[int(float(key))]= [data[key]['exp0']]
    
 
        print limits
        print[ (k, limits[k]) for k in  sorted(limits)]


    outfile=open(filename.replace('json', 'tex'), 'w')

    #for label in labels:
    #    outfile.write(' & %s' %label)
    #outfile.write('\\\\\hline\n')
    for key in sorted(limits):
     
        for value in limits[key] :
            outfile.write('%s ' %str(key))
            outfile.write('& %.4f'%value)
            outfile.write('\\\\\n')
    outfile.write('\hline')

    outfile.close()


