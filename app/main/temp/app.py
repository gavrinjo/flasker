import os

basedir = os.path.abspath(os.path.dirname(__file__))
source = basedir+"\\source"
target = basedir+"\\target"

#print(basedir, source, target)

for root, dirs, files in os.walk(target, topdown=True):
    for name in files:
        with open(os.path.join(root, name), "r") as f:
            for i in f:
                print(i.strip())
        
        #print(os.path.join(root, name))
    #for name in dirs:
        #print(os.path.join(target, name))


"""
def read_file(src):
    with open(src, "r") as f:
        for i in f:
            print(i.strip)"""