import json
import os
from pywget import wget
import requests

"""
This script allows the automatic collection of python code from formatted notebooks.

An example is provided.

"""

def findImageTag(source=None):
    """
    Receives string and finds the img tag and retrieves the link of its source.
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

def savesNBimages (notebook=None, folder=None):
    """ 
    Receives a Notebook and Folder directory, and collects and save its images locally.
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
    print('OOOO')

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

                # save image locally
                #if link not in ['attachment:sciencejournal.png','attachment:google-play-app-store-badges-5926dec63df78cbe7eaf4f9e.jpg','attachment:Screen%20Shot%202020-02-26%20at%2016.21.45.png','attachment:Screenshot_20200226_162843_com.google.android.apps.forscience.whistlepunk.jpg','attachment:Screenshot_20200226_185831_com.google.android.apps.forscience.whistlepunk.jpg','attachment:Screenshot_20200226_185903_com.google.android.apps.forscience.whistlepunk.jpg','attachment:Screenshot_20200226_185933_com.google.android.apps.forscience.whistlepunk.jpg','attachment:Screenshot_20200226_190125_com.google.android.apps.forscience.whistlepunk.jpg','attachment:Screenshot_20200227_000702_com.google.android.apps.forscience.whistlepunk.jpg','attachment:Screenshot_20200227_000805_com.google.android.apps.forscience.whistlepunk%202.jpg','attachment:ArduinoIDE.png','attachment:ArduinoIDEexplained.png','attachment:ComputerUSB.png','attachment:ArduinoUSB.png',
                #'attachment:ArduinoBoard.png','attachment:ArduinoPort.png','attachment:ErrorSketch.png','attachment:ArduinoLED.png',
                #'attachment:Blink.png','attachment:MultiBlink.png','attachment:Button.png']:
                try:
                    wget.download(link, folder)    
                except:
                    print('ALERT', notebook)       
                    
            
def savesNBimagesFolder(dir=None):
    """

    This function can be used to collect images from the notebooks inside a repository.
    It receives the directory path of the repository (folder) from whose notebook the images should be extracted.
    
    Firstly, it identifies de directory structure inside the father directory, i.e. which folders there are inside it. 
    Then it creates folders with the same names (+'_IMG') and saves the respective images inside them. 

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

#savesNBimages(notebook="F001 Swimming.ipynb", folder="./AllImages")

savesNBimagesFolder(dir='ScientIST-notebooks')

