
Global Documentation - ScientISST Utilities 
============================================

#  

## readCode.py



This script allows the automatic collection of python code from ScientIST notebooks.

An example is provided.


This script contains the following functions.
###  collectPythonCode 
Open formatted scientIST notebook and retrieves a python script.

    

*def collectPythonCode (notebook=".ipynb",folder="")*

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
    
###  creatNB
Opens python script and retrieves a notebook file containing the code collected.

    

*def creatNB(NBskeleton='NBskeleton.txt', nameNB="test")*

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
    
###  createNBfromScript 
Opens python script and retrieves a notebook file containing the code collected.

    

*def createNBfromScript (nameNB="test", script="../../ECG.py")*

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
    
#  

## globalDocumentationMD.py



This script allows the automatic documentation of the _Utilities folder in the ScientISST notebooks repository.


This script contains the following functions.
###  globalDocumentationMD 
Generates the documentation of the _Utilities folder in a Markdown file (.MD).

    

*def globalDocumentationMD (file_name='README')*

    Parameters
    ----------
    file_name: str
        Name of the .MD file.
    
    Returns
    -------
    md_file: 
        Markdown file containing the documentation collected in the folder.
                 p1_='

*def"
            i1 = s.find(p,0)
            i2 = s.find("(", i1+1)
            i3 = s.find("*

1_='Parameters'
                i1_=s.find(p_, i1+3)
                i2_ = s.find(p_, i1_+3)
                i3_ = s.find(p1_, i1_+3)
                global_description=data[i1_+5:i3_]
                par_ret=data[i3_-4:i2_]
                mdFile.write(global_description[3:])
                mdFile.new_paragraph(function_def,bold_italics_code='i')
                mdFile.new_paragraph(par_ret)

            while i1 != -1 and i3_ != -1:
                i1 = s.find(p, i2+1)
                i2 = s.find("(", i1+1)
                i3 = s.find(":", i2+1)
                function_name=data[i1:i2]
                function_def=data[i1:i3]
                txt=function_name[3:]
                

                if len(txt) != 0: # cope with functions that use 
### =data[i1:i3]
            txt=function_name[3:]
            mdFile.new_header
             p1_='

*def=data[i1:i3]
            txt=function_name[3:]
            mdFile.new_header(level=3, title=txt)
            #mdFile.new_paragraph(function_def,bold_italics_code='i')

            if function_name[3*

1_='Parameters'
                i1_=s.find(p_, i1+3)
                i2_ = s.find(p_, i1_+3)
                i3_ = s.find(p1_, i1_+3)
                global_description=data[i1_+5:i3_]
                par_ret=data[i3_-4:i2_]
                mdFile.write(global_description[3:])
                mdFile.new_paragraph(function_def,bold_italics_code='i')
                mdFile.new_paragraph(par_ret)

            while i1 != -1 and i3_ != -1:
                i1 = s.find(p, i2+1)
                i2 = s.find("(", i1+1)
                i3 = s.find(":", i2+1)
                function_name=data[i1:i2]
                function_def=data[i1:i3]
                txt=function_name[3:]
                

                if len(txt) != 0: # cope with functions that use 
### ,bold_italics_code='i')

            if function_name[3:] != '':
                p_='"""'
                p1_='Parameters'
                i1_=s.find
in the code (yet not for commenting)
                    if function_name[3]!='"':
                        mdFile.new_header(level=3, title=txt)

                if txt != '' and txt != ' ':
                    # finds description of the function
                    p_='"""'
                    p1_='

*def,bold_italics_code='i')

            if function_name[3:] != '':
                p_='"""'
                p1_='Parameters'
                i1_=s.find(p_, i1+3)
                i2_ = s.find(p_, i1_+3)
                i3_ = s.find(p1_, i1_+3)
                global_description=data[i1_+5*


#  

## editjson.py



This script allows the automatic formatting of non-formatted notebooks, using the 
scientIST version template, and to make plain notebooks from formatted notebooks.

An example is provided at the end of the script, using an empty NB (emptyNB.ipynb).


This script contains the following functions.
###  openTemplateDict 
This .txt file is a dictionary that includes the styling information of the scientIST template version.
    Note: the .txt file must be updated in case the scientIST template version is changed.

    
    

*def openTemplateDict (document="dictNB.txt")*

    Parameters
    ----------
    document: .txt file
        Dictionary that one wants to read.

    Returns
    -------
    jsonObjNB: .json 
        .json object containing the dictionary's information.
    
###  makePlain 
Open FORMATTED scientIST version and retrieves a PLAIN notebook.
    
    

*def makePlain (notebook="testeNB.ipynb")*

    Parameters
    ----------
    notebook: .ipynb file
        Notebook that one wants to make plain.

    Returns
    -------
    jsonObjNB: .json 
        .json object containing the updated dictionary's information.
    
###  makeFormatted 
Open PLAIN notebook and retrieves its FORMATTED scientIST version.
    
    

*def makeFormatted (notebook="emptyNB")*

    Parameters
    ----------
    notebook: .ipynb file
        Plain notebook to which one wants to apply the scientIST notebook's styling.

    Returns
    -------
    jsonObjNB: .json 
        .json object containing the updated dictionary's information.
    
###  formatAll
This function can be used to format several notebooks inside a folder.
    
    

*def formatAll(dir='ScientIST-notebooks/folder_name/')*

    Parameters
    ----------
    dir: string
        Directory path of the folder containing the notebooks to format.
    
#  

## downloadIMG.py



This script allows the automatic collection of python code from formatted notebooks.

An example is provided at the end of the script.


This script contains the following functions.
###  findImageTag 
Receives string, finds the img tag and retrieves the link of its source.
    
    

*def findImageTag (source=None)*

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
    
###  replaceImagePath 
 Receives string, finds the img tag and retrieves the link of its source. Receives a Notebook and Folder directory, and collects and save its images locally.
    
    

*def replaceImagePath (notebook=None, folder=None, segmentOld=None, segmentNew=None)*

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

    
###  savesNBimages 
 Receives a Notebook and Folder directory, and collects and save its images locally.
    

*def savesNBimages (notebook=None, folder=None)*

    Parameters
    ----------
    notebook: str
        Directory of a .ipynb file.
    folder: str
        Directory where images found are to be saved.
    
###  savesNBimagesFolder 
This function can be used to collect images from the notebooks inside a repository. Firstly, it identifies de directory structure, i.e. which folders there are inside it. Then it creates folders with the same names (+'_IMG') and saves the respective images accordingly. 

    

*def savesNBimagesFolder (dir=None)*

    Parameters
    ----------
    dir: str
        Directory of a notebooks's repository folder.
    
#  

## generateMasterTable.py



This script is used to go through the whole repository directory and build a .md file containing a comprehensive table of contents and information regarding all notebooks found.


This script contains the following functions.
###  dirFiles
Finds notebooks in a directory and collects relevant information from each.
    
    

*def dirFiles(dir='')*

    Parameters
    ----------
    dir: string
        Directory path of the repository.
    