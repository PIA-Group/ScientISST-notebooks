import os
import sys
from mdutils.mdutils import MdUtils

"""
This script allows the automatic documentation of the _Utilities folder in the ScientISST notebooks repository.
"""

def globalDocumentationMD (file_name='README'):
    """
    Generates the documentation of the _Utilities folder in a Markdown file (.MD).

    Parameters
    ----------
    file_name: str
        Name of the .MD file.
    
    Returns
    -------
    md_file: 
        Markdown file containing the documentation collected in the folder.
    """
    
    title='Global Documentation - ScientISST Utilities '

    mdFile = MdUtils(file_name=file_name,title=title)

    # body of the document
    dir='.'
    l_dir = os.listdir(dir)

    for f_name in l_dir:
        if f_name.endswith('.py'):

            mdFile.new_header(level=1, title= ' ')
            mdFile.new_header(level=2, title=f_name)

            fileObj = open(f_name, 'r')
            data=fileObj.read()
            s=data

            # find global script description
            p='"""'
            i=s.find(p)
            i2_ = s.find('"""', i+3)
            global_description=data[i:i2_]
            txt=global_description[3:]
            mdFile.new_paragraph(txt)


            mdFile.new_paragraph('This script contains the following functions.')
            
            # find functions
            p="def"
            i1 = s.find(p,0)
            i2 = s.find("(", i1+1)
            i3 = s.find(":", i1+1)
            function_name=data[i1:i2]
            function_def=data[i1:i3]
            txt=function_name[3:]
            mdFile.new_header(level=3, title=txt)
            #mdFile.new_paragraph(function_def,bold_italics_code='i')

            if function_name[3:] != '':
                p_='"""'
                p1_='Parameters'
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
                

                if len(txt) != 0: # cope with functions that use """ within the code (yet not for commenting)
                    if function_name[3]!='"':
                        mdFile.new_header(level=3, title=txt)

                if txt != '' and txt != ' ':
                    # finds description of the function
                    p_='"""'
                    p1_='Parameters'
                    i1_=s.find(p_, i2)
                    i2_ = s.find(p_, i1_+3)
                    i3_ = s.find(p1_, i1_+3)
                    global_description=data[i1_:i3_]
                    if len(global_description) != 0 and global_description[3]!='"': # cope with functions that use """ within the code (yet not for commenting)
                        global_description=data[i1_+5:i3_]
                        par_ret=data[i3_-4:i2_]
                        mdFile.write(global_description[3:])
                        mdFile.new_paragraph(function_def,bold_italics_code='i')
                        mdFile.new_paragraph(par_ret)

                i3_ = s.find(p1_, i3_+10)

    mdFile.create_md_file()

globalDocumentationMD()