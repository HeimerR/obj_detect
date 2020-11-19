import os 
import glob 

def delete_files(path="static/images/upload/"):
    files = glob.glob(path + '*')
    for f in files: 
        os.remove(f) 