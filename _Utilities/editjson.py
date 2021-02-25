import json
import os
"""
This script allows the automatic formatting of non-formatted notebooks, using the 
scientIST version template, and to make plain notebooks from formatted notebooks.

An example is provided at the end of the script, using an empty NB (emptyNB.ipynb).
"""

def openTemplateDict (document="dictNB.txt"):
    """
    This .txt file is a dictionary that includes the styling information of the scientIST template version.
    Note: the .txt file must be updated in case the scientIST template version is changed.

    
    Parameters
    ----------
    document: .txt file
        Dictionary that one wants to read.

    Returns
    -------
    jsonObjNB: .json 
        .json object containing the dictionary's information.
    """
    teste=open(document,"r")
    dataNB = teste.read()
    jsonObjNB = json.loads(dataNB)
    keylist = jsonObjNB.keys()
    return jsonObjNB

def makePlain (notebook="testeNB.ipynb"):
    """
    Open FORMATTED scientIST version and retrieves a PLAIN notebook.
    
    Parameters
    ----------
    notebook: .ipynb file
        Notebook that one wants to make plain.

    Returns
    -------
    jsonObjNB: .json 
        .json object containing the updated dictionary's information.
    """

    try:
        f = open(notebook,"r")
        print('i')
    except:
        notebook=notebook+'.ipynb'
        f = open(notebook,"r")

    jsonObjNB=openTemplateDict()
    data = f.read()
    jsonObj = json.loads(data)

    keylist = jsonObj.keys()
    itemslist = jsonObj.items()

    # retira cabecalho
    dict_=dict(jsonObj['cells'][0])
    if str(dict_['source'][0]).startswith("# <div  style=\"color:"):
        dict_['source'][0]=dict_['source'][0][401:]
        if str(dict_['source'][0]).endswith("</span> </div>"):
            dict_['source'][0]=dict_['source'][0][:-14]
                
    # retira rodape
    dict_=dict(jsonObj['cells'][-3])
    if str(dict_['source'][0]).startswith("<div style=\"height:100px;"):
        jsonObj['cells'].pop(-3)
    dict_=dict(jsonObj['cells'][-2])
    if str(dict_['source'][0]).startswith("<div style=\"width: 100%;"):
        jsonObj['cells'].pop(-2)
    dict_=dict(jsonObj['cells'][-1])
    if str(dict_['source'][0]).startswith("```Contributors"):
        jsonObj['cells'].pop(-1)

    # percorre cells ao longo do nb
    length=len(jsonObj['cells'])
    for i in range(0,length):
        dict_=dict(jsonObj['cells'][i])
        dict_keys=dict_.keys()
        
        if dict_['cell_type']=='markdown':
            # sections
            if '# I. ' in str(dict_['source']) or '# II. ' in str(dict_['source']) or '# III. ' in str(dict_['source']):
                l_=len(dict_['source'])
                if l_>1:
                    for i in range(2,l_+1):
                        dict_['source'].remove(dict_['source'][-1])
            
            # subsections
            elif '##' in str(dict_['source']) or '###' in str(dict_['source']): #or '## 2.' in str(dict_['source']) or '## 3.' in str(dict_['source']) or '## 4.' in str(dict_['source']) or '## 5.' in str(dict_['source']) or '## 6.' in str(dict_['source']) or '## 7.' in str(dict_['source']) or '## 8.' in str(dict_['source']) or '## 9.' in str(dict_['source']) or '## 10.' in str(dict_['source']):
                b=0
                if jsonObjNB['subsection'] in str(dict_['source']):
                    b=len(jsonObjNB['subsection'] )
                elif jsonObjNB['subsection_'] in str(dict_['source']):
                    b=len(jsonObjNB['subsection_'])
                if b>0:
                    e=len(jsonObjNB['subsection2'] )
                    t=len(dict_['source'][0])
                    if '###' in str(dict_['source']): 
                        dict_['source'][0]='###' + dict_['source'][0][b+1:t-e]
                    elif '##' in str(dict_['source']):
                        dict_['source'][0]='##' + dict_['source'][0][b:t-e]

    f.seek(0)        
    with open(notebook, 'w') as json_data:
            json.dump(jsonObj, json_data)

    return jsonObjNB


def makeFormatted (notebook="emptyNB"):
    """
    Open PLAIN notebook and retrieves its FORMATTED scientIST version.
    
    Parameters
    ----------
    notebook: .ipynb file
        Plain notebook to which one wants to apply the scientIST notebook's styling.

    Returns
    -------
    jsonObjNB: .json 
        .json object containing the updated dictionary's information.
    """

    try:
        f = open(notebook,"r")
    except:
        notebook=notebook+'.ipynb'
        f = open(notebook,"r")
    
    jsonObjNB =openTemplateDict()
        
    data = f.read()
    jsonObj = json.loads(data)

    keylist = jsonObj.keys()
    print(keylist)

    itemslist = jsonObj.items()
    length=len(jsonObj['cells'])
    for i in range(0,length):
        dict_=dict(jsonObj['cells'][i])
        dict_keys=dict_.keys()

        if dict_['cell_type']=='markdown':
            # adiciona cabecalho
            if i == 0:
                if "color:#303030;font-family:'arial blACK'," not in str(dict_['source'][0]):
                    title=dict_['source'][0]
                    dict_['source'][0]=jsonObjNB['title'] + title + jsonObjNB['title2']

            # adiciona rodape
            if i ==length-2:
                if "<div style=\"height:115px; " not in str(dict_['source'][0]):
                    jsonObj['cells'].append(jsonObjNB['subfooter'])
                    jsonObj['cells'].append(jsonObjNB['footer'])
                    jsonObj['cells'].append(jsonObjNB['authors'])

            # sections
            elif '# I. ' in str(dict_['source']) or '# II. ' in str(dict_['source']) or '# III. ' in str(dict_['source']):
                if '<div style="' not in str(dict_['source']):
                    dict_['source'].append(jsonObjNB['section'])
                    dict_['source'].append(jsonObjNB['section2'])
            
            # subsections
            elif '##' in str(dict_['source']) or '###' in str(dict_['source']) :
                if '<div style="' not in str(dict_['source']):
                    if '###' in str(dict_['source']):
                        subsection=dict_['source'][0][3:]
                    elif '##' in str(dict_['source']):
                        subsection=dict_['source'][0][2:]
                    dict_['source'][0]=jsonObjNB['subsection'] + subsection + jsonObjNB['subsection2']


    f.seek(0) 
    with open(notebook, 'w') as json_data:
        json.dump(jsonObj, json_data)


# EXAMPLE
makeFormatted(notebook="emptyNB")
#makePlain(notebook="emptyNB")

def formatAll(dir='ScientIST-notebooks/folder_name/'):
    """
    This function can be used to format several notebooks inside a folder.
    
    Parameters
    ----------
    dir: string
        Directory path of the folder containing the notebooks to format.
    """
    
    l_dir = os.listdir(dir)
    for f_name in l_dir:
        if f_name not in ['Autoencoders_Resp.ipynb']:
            if f_name.endswith('.ipynb'):
                path=dir + f_name
                print(f_name)
                makePlain(notebook=path)
                makeFormatted(notebook=path)

#dirFiles()