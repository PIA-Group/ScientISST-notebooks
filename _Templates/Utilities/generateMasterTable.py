import os
from datetime import datetime
import json
import numpy as np



def dirFiles(dir=''):
    l_dir = sorted(os.listdir(dir))
    
    for f_name in l_dir:
        if f_name.endswith('.ipynb') and f_name not in ['A002 Science Journal.ipynb']:
            path=dir + f_name
            
            f_name=f_name[:-6]
            print(f_name)

            statbuf = os.stat(path)
            timestamp=statbuf.st_mtime
            datetime_ = datetime.fromtimestamp(timestamp)
            print("datetime =", datetime_)
            f=open(path,"r")
            data = f.read()
            jsonObj = json.loads(data)

            keylist = jsonObj.keys()
            itemslist = jsonObj.items()
            
            for i in range(0,len(jsonObj['cells'])):
                source=str(jsonObj['cells'][i]['source'][0])
                if i==len(jsonObj['cells'])-1:
                    if source.startswith('```'):
                        author=source[17:-3]
                    else:
                        author='Prof. Hugo Silva, Joana Pinto'
                elif i==2:
                    tags=''
                    if source.startswith('```'):
                        mylist = source.split(',')
                        nb_tags=len(mylist)
                        for e in range(0,nb_tags):
                            elem=mylist[e]
                            if elem[3]=='`':
                                elem=elem[4:-3]
                            else:
                                elem=elem[3:-3]
                            tags+=str(elem)+', '
                        print (tags)
                        
            if f_name[0]=='A':
                chapter='A. Signal Acquisition'
            elif f_name[0]=='B':
                chapter='B. Graphical User Interface'
            elif f_name[0]=='C':
                chapter='C. Signal Processing'
            elif f_name[0]=='D':
                chapter='D. Feature Extraction'
            elif f_name[0]=='E':
                chapter='E. Classification'
            elif f_name[0]=='F':
                chapter='F. Applications'

            md_file.write(f_name[0:4] +' | ')
            md_file.write(f_name[4:] +' | ')
            md_file.write(chapter +' | ')
            md_file.write(str(tags[:-1])+'|')
            #md_file.write('1hour'+'|')
            md_file.write(author +'|')
            md_file.write(str(datetime_)[0:10]+'|'+'\n')
        print('i')

file_name="MasterTable"
with open(os.path.join('../../','{}.md'.format(file_name)), mode='w') as md_file:
    md_file.write("# ScientIST Notebooks \n This Table provides an overview to the complete set of notebooks made available in this repository. \n \n These are independent and can be selected independently and organized as most suits the purpose of the course.  \n\n ## Detailed Repository:  \n")
    md_file.write("ID | Name | Chapter | Tags | Authors | Last update \n")
    md_file.write("--- | --- | --- | --- | --- | --- \n")
    dirFiles(dir='../../A.Signal_Acquisition/')
    dirFiles(dir='../../B.Graphical_User_Interface/')
    dirFiles(dir='../../C.Signal_Processing/')
    dirFiles(dir='../../D.Feature_Extraction/')
    dirFiles(dir='../../E.Classification/')
    dirFiles(dir='../../F.Applications/')