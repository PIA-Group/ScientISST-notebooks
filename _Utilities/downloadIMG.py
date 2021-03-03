import json
import os
from pywget import wget
import requests

"""
This script allows the automatic collection of python code from formatted notebooks.

An example is provided at the end of the script.
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


def savesNBimages (notebook=None, folder=None):
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
                    
            
def savesNBimagesFolder (dir=None):
    """
    This function can be used to collect images from the notebooks inside a repository. Firstly, it identifies de directory structure, i.e. which folders there are inside it. Then it creates folders with the same names (+'_IMG') and saves the respective images accordingly. 

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
                        savesNBimages(notebook=path, folder='./'+str(img_folder))
                except:
                    print('')   

        except:
            print('This folder ' + j + ' does not have .ipynb files.')




# EXAMPLE

#savesNBimages(notebook="A001 Open Signals.ipynb", folder="./AllImages")

#savesNBimagesFolder(dir='ScientIST-notebooks')

#replaceImagePath(notebook="../A.Signal_Acquisition/teste.ipynb", segmentOld='/X.Example_Files/', segmentNew='/_Resources/')

#replaceImagePath(folder="../", segmentOld='/X.Example_Files/', segmentNew='/_Resources/')
