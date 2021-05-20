import json
import os
from pywget import wget
import requests

"""
This script allows the automatic inteaction with a ScientISST Notebook, to find, interact with and collect elements.

Examples are provided at the end of the script.
"""

def findImageTag (source=None):
    """
    Receives string, finds the img tag and retrieves the link of its source.
    
    Parameters
    ----------
    source: str
        String within which one wants to find img tags and collect image.

    Returns
    -------
    link: str
        Source of the images found, i.e. the URL link where the image is stored.

    index_end: int
        index of the last element of the link found.
    """
    len_source=len(source)
    source_ =str(source)
    index=source_.find('img src')
    link=''
    index_end=0
    if index>0:    
        index+=9
        maximo=len(source_)
        source_left=source_[index+5:maximo]
        index_end=source_left.find('"')
        index_end+=index+5
        link=source_[index:index_end]
        print(link)

    return link, index_end

def replaceImagePath (notebook=None, folder=None, segmentOld=None, segmentNew=None):
    """ 
    Receives string, finds the img tag and retrieves the link of its source. Receives a Notebook and Folder directory, and collects and save its images locally.
    
    Parameters
    ----------
    notebook: str (optional)
        Directory of a .ipynb file.
    
    folder: str (optional)
        Directory of a folder with .ipynb files, used instead of 'notebook' if one wants to make changes in the whole repository.

    segmentOld: str
        Part of the string to be removed.

    segmentNew: str
        New string to replace the string that will be removed.

    """
    if notebook is not None:
        try:
            f = open(notebook,"r")
        except:
            notebook=notebook+'.ipynb'
            f = open(notebook,"r")

        # open and read notebook (json object)
        data = f.read()
        jsonObj = json.loads(data)
        jsonObj_=str(jsonObj).replace(segmentOld, segmentNew)
        # becomes dict again
        jsonObj=eval(jsonObj_)
        f.seek(0) 


    elif folder is not None:
        dir=folder
        folders=next(os.walk(dir))[1]
        print(folders)
        for j in folders:
            #reads notebooks inside the folder j
            print(j)
            try:
                #updates the directory path to be read
                l_dir = os.listdir(dir+'/'+j+'/')
                os.walk(l_dir)
                for f_name in l_dir:                    
                    if f_name.endswith('.ipynb'):
                        try:
                            notebook=dir+'/'+j+'/'+'/'+f_name
                            f = open(notebook,"r")
                            
                            data = f.read()
                            jsonObj = json.loads(data)
                            jsonObj_=str(jsonObj).replace(segmentOld, segmentNew)
                            jsonObj=eval(jsonObj_)
                            f.seek(0) 
                            
                            print(notebook)
                            with open(notebook, 'w') as json_data:
                                json.dump(jsonObj, json_data)   
                        except:
                            print(' ')    
                            

            except:
                print(' ')

def saveNBimages (notebook=None, folder=None):
    """ 
    Receives a Notebook and Folder directory, and collects and save its images locally.
    Parameters
    ----------
    notebook: str
        Directory of a .ipynb file.
    folder: str
        Directory where images found are to be saved.
    """
    try:
        f = open(notebook,"r")
    except:
        notebook=notebook+'.ipynb'
        f = open(notebook,"r")

    # open and read notebook (json object)
    data = f.read()
    jsonObj = json.loads(data)

    keylist = jsonObj.keys()
    itemslist = jsonObj.items()

    f.seek(0)        

    # walks through the cells of the notebook
    length=len(jsonObj['cells'])

    for i in range(1,length-3):
        dict_=dict(jsonObj['cells'][i])
        dict_keys=dict_.keys()
        index=0
        if dict_['cell_type']=='markdown': 
            # finds all image links in this cell
            source_ =str(dict_['source']).replace(',', '')
            nr_img=source_.count('img')
            index_end=0
            for c in range(0, nr_img):
                link, index_end = findImageTag(source=source_[index_end:-1])
                try:
                    wget.download(link, folder)    
                except:
                    print('ALERT', notebook)       
                          
def saveNBimagesRepository (dir=None):
    """
    This function can be used to collect images from the notebooks inside a repository. 
    Firstly, it identifies de directory structure, i.e. which folders there are inside it. Then it creates folders with the same names (+'_IMG') and saves the respective images accordingly. 

    Parameters
    ----------
    dir: str
        Directory of a notebooks's repository folder.
    """

    folders=next(os.walk(dir))[1]
    print(folders)

    for j in folders:
        #reads notebooks inside the folder j
        try:
            #updates the directory path to be read
            l_dir = os.listdir(dir+'/'+j+'/')
            os.walk(l_dir)
            try:
                img_folder=j+str('_IMG')
                os.mkdir(img_folder)
            except:
                print('The folder ' + img_folder + ' already existed and will be update.' )

            for f_name in l_dir:
                try:
                    if f_name.endswith('.ipynb'):
                        path=dir+'/'+j+'/'+ f_name
                        print(path)
                        saveNBimages(notebook=path, folder='./'+str(img_folder))
                except:
                    print('')   

        except:
            print('This folder ' + j + ' does not have .ipynb files.')

def collectPythonCode (notebook=None,folder=None):
    """
    Opens formatted ScientISST notebook and retrieves a Python script.

    Parameters
    ----------
    notebook: str
        Name of a .ipynb file.

    folder: str
        Directory of the folder where the notebook is located.
    
    Returns
    -------
    python_file: 
        Python file containing the code collected in the notebook.
    """
    try:
        f = open(folder+notebook,"r")
        print('i')
    except:
        notebook=notebook+'.ipynb'
        f = open(folder+notebook,"r")

    # open and read notebook (json object)
    data = f.read()
    jsonObj = json.loads(data)

    keylist = jsonObj.keys()
    itemslist = jsonObj.items()
    f.seek(0)        
    python_file=open("script_"+str(notebook[0:-6])+".py","w")

    # walks through the cells of the notebook
    length=len(jsonObj['cells'])
    for i in range(0,length):
        dict_=dict(jsonObj['cells'][i])
        dict_keys=dict_.keys()
        if dict_['cell_type']=='code':    
            python_file.write("\n")        
            len_cell=len(dict_['source'])
            for j in range(0,len_cell):

                if str(dict_['source'][j]).startswith('!pip install') or str(dict_['source'][j]).startswith('%matplotlib notebook') or str(dict_['source'][j]).startswith('mpld3.enable_notebook()'):
                    python_file.write('#'+str(dict_['source'][j]))
                else:
                    python_file.write(str(dict_['source'][j]))

    python_file.close()

    return python_file

def createNB(skeletonNB=None, nameNB=None):
    """
    Opens Python script and retrieves a notebook file containing the code collected.

    Parameters
    ----------
    skeletonNB: .txt
        .txt file containing the styling used in a ScientISST Notebook.

    nameNB: str
        Name to be given to a new .ipynb file.
    
    Returns
    -------
    NB: str
        .ipynb file in accordance with the ScientISST Notebook styling.
    """

    f=open(nameNB + '.ipynb', "w")
    skeletonNB=open(skeletonNB,"r")
    dataNB = skeletonNB.read()
    f.write(dataNB)
    nameNB+='.ipynb'

    f.close()
    NB = nameNB

    return NB

def createNBfromScript (nameNB=None, script=None):
    """
    Opens Python script and retrieves a notebook file containing the code collected.

    Parameters
    ----------
    nameNB: str
        Name to be given to a new .ipynb file.

    script: str
        Python script to collect code from.
    
    Returns
    -------
    ipynb_file: 
        Notebook file containing the code collected in the original Python script.
    """
    
    if nameNB.endswith('.ipynb'):
        name_=nameNB[:-6]
    else:
        name_=nameNB
        
    name_=name_+'notebook'
    createNB(nameNB=name_)  

    # opens NB
    name_nb=name_+'.ipynb'
    f = open(name_nb,"r")
    fr = f.read()
    
    jsonNB = json.loads(fr)
    lastCells = jsonNB['cells'][-7:]
    jsonNB['cells']=jsonNB['cells'][:-7]
    length=len(jsonNB['cells'])

    f_name=script
    if f_name.endswith('.py'):
        fileObj = open(f_name, 'r')
        data=fileObj.read()
        s=data

        # find global script description
        p='"""'
        i=s.find(p)
        i2_ = s.find('"""', i+3)
        global_description=data[i:i2_]
        jsonNB['cells'].append({"cell_type": "markdown", "metadata": {}, "source": [ global_description[3:]]})

        
        # find functions
        p="def"
        i1 = s.find(p,0)
        i2 = s.find("(", i1+1)
        i3= s.find("def", i1+1)
        function_name=s[i1:i2]
        function=s[i1:i3]
        jsonNB['cells'].append({"cell_type": "markdown", "metadata": {}, "source": [ function_name[3:]]})
        jsonNB['cells'].append({"cell_type": "code", "execution_count": 1, "metadata": {}, "outputs": [], "source": [function] })
        
        while i1 != -1:
            i1 = s.find(p, i2+1)
            i2 = s.find("(", i1+1)
            function_name=s[i1:i2]
            
            if function_name[3:] != '':
                # finds description of the function
                p_='"""'
                i1_=s.find(p_, i2)
                i2_ = s.find('"""', i1_+3)
                global_description=s[i1_:i2_]
                i3= s.find(p, i1+1)
                function=s[i1:i3]
                jsonNB['cells'].append({"cell_type": "code", "execution_count": 1, "metadata": {}, "outputs": [], "source": [function] })

    for cell in lastCells:
        jsonNB['cells'].append(cell)

    f.seek(0) 
    with open(name_nb, 'w') as json_data:
        json.dump(jsonNB, json_data)

    ipynb_file= jsonNB

    return ipynb_file



# EXAMPLE

#saveNBimages(notebook="A001 Open Signals.ipynb", folder="./AllImages")

#saveNBimagesRepository(dir='ScientISST-notebooks')

#replaceImagePath(notebook="../A.Signal_Acquisition/teste.ipynb", segmentOld='/X.Example_Files/', segmentNew='/_Resources/')

#replaceImagePath(folder="../", segmentOld='/X.Example_Files/', segmentNew='/_Resources/')


# EXAMPLE
#collectPythonCode(notebook="F001 Swimming.ipynb",folder="../F.Applications/")
#createNB(skeletonNB='skeletonNB.txt', nameNB="test")    
#createNBfromScript(nameNB="ECG", script="../../ECG.py")