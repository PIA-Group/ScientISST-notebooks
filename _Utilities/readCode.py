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


# EXAMPLE
collectPythonCode(notebook="F001 Swimming.ipynb",folder="../F.Applications/")
