import json
import os

"""
This script allows the automatic collection of python code from ScientIST notebooks.

An example is provided.
"""

def collectPythonCode (notebook=".ipynb",folder=""):
    """
    Open formatted scientIST notebook and retrieves a python script.

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

def creatNB(NBskeleton='NBskeleton.txt', nameNB="test"):
    """
    Opens python script and retrieves a notebook file containing the code collected.

    Parameters
    ----------
    NBskeleton: .txt
        .txt file containing the styling used in a ScientIST Notebook.

    nameNB: str
        Name to be given to a new .ipynb file.
    
    Returns
    -------
    NB: str
        .ipynb file in accordance with the ScientIST Notebook styling.
    """

    f=open(nameNB + '.ipynb', "w")
    NBskeleton=open(NBskeleton,"r")
    dataNB = NBskeleton.read()
    f.write(dataNB)
    nameNB+='.ipynb'

    f.close()
    NB = nameNB

    return NB



def createNBfromScript (nameNB="test", script="../../ECG.py"):
    """
    Opens python script and retrieves a notebook file containing the code collected.

    Parameters
    ----------
    nameNB: str
        Name to be given to a new .ipynb file.

    script: str
        Python script to collect code from.
    
    Returns
    -------
    ipynb_file: 
        Notebook file containing the code collected in the original python script.
    """
    
    if nameNB.endswith('.ipynb'):
        name_=nameNB[:-6]
    else:
        name_=nameNB
        
    name_=name_+'notebook'
    creatNB(nameNB=name_)  

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
#collectPythonCode(notebook="F001 Swimming.ipynb",folder="../F.Applications/")

#creatNB()    
createNBfromScript(nameNB="ECG", script="../../ECG.py")