import os
import sys
from mdutils.mdutils import MdUtils


mdFile = MdUtils(file_name='README',title='Global Documentation - ScientISST Utilities ')

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
        i2 = s.find("(", i+1)
        function_name=data[i1:i2]
        txt=function_name[3:]
        mdFile.new_header(level=3, title=txt)
        if function_name[3:] != '':
            p_='"""'
            i1_=s.find(p_, i2)
            i2_ = s.find('"""', i1_+3)
            global_description=data[i1_:i2_]
            txt=global_description[3:]
            mdFile.new_header(level=4, title=txt)

        while i1 != -1:
            i1 = s.find(p, i2+1)
            i2 = s.find("(", i1+1)
            function_name=data[i1:i2]
            txt=function_name[3:]

            if len(txt) != 0: # cope with functions that use """ within the code (yet not for commenting)
                if function_name[3]!='"':
                    mdFile.new_header(level=3, title=txt)
            if txt != '' and txt != ' ':
                # finds description of the function
                p_='"""'
                i1_=s.find(p_, i2)
                i2_ = s.find('"""', i1_+3)
                global_description=data[i1_:i2_]
                txt=global_description[3:]
                if global_description[3]!="'": # cope with functions that use """ within the code (yet not for commenting)
                    mdFile.new_header(level=4, title=txt)

mdFile.create_md_file()