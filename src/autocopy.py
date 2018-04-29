import os,shutil
"""
Automatally copies all files in user1 to user2 and user3
"""

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if 'server_files' not in s:
                shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def emptyFolder(dir):
        
    for the_file in os.listdir(dir):
        file_path = os.path.join(dir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def replaceFolder(src,dst):
        emptyFolder(dst)
        copytree(src,dst)

        
src =  os.path.dirname(os.path.realpath(__file__)) + '\\user1'
dst =  os.path.dirname(os.path.realpath(__file__)) + '\\user2'
replaceFolder(src,dst)
dst =  os.path.dirname(os.path.realpath(__file__)) + '\\user3'
replaceFolder(src,dst)
dst =  os.path.dirname(os.path.realpath(__file__)) + '\\user4'
replaceFolder(src,dst)


